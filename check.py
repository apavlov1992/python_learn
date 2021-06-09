#!/usr/bin/env python

"""This script purpose for check was is changes file in the directory or not."""

import sys
import argparse
import os
import hashlib
import logging
from logging import StreamHandler, Formatter
import atexit  # закрывать файл через этот модуль
import requests


class File:

    def __init__(self, path):
        self.path = path

    def md5sum(self, blocksize: int = 4096):
        hasher_fn = hashlib.md5()
        with open(self.path, 'rb') as afile:
            buf = afile.read(blocksize)
            hasher_fn.update(buf)
            files_md5sum = hasher_fn.hexdigest()
            return files_md5sum

    def check(self, sha):
        return self.md5sum() == sha


def print_usage():
    print('Usage: python dir_check.py -d '
          '<dir_to_check> or python dir_check.py -c -d <dir_to_check> to check diff')


# задефайнить коды возврата
BAD_ARGUMENTS_ERROR = 1


def walk_directory(dir_to_check):
    for root, directories, files in os.walk(dir_to_check, topdown=False):
        for name in files:
            file = File(os.path.join(root, name))
            yield file


def __main__(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
                        help='Recursive check md5sum file and write to file')
    parser.add_argument('-c', '--check', action='store_true',
                        help="Check previously file for diff")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output to console")
    parser.add_argument('-o', '--outputfile', action='store',
                        dest='outputfile', default='output_without_check')
    parser.add_argument('-l', '--logging', action='store', default='INFO')  # заменить на verbose
    # parser.add_argument(action=) # action counter - сколько раз передали флаг -v
    args = parser.parse_args(args)
    output_file = args.outputfile

    logger = logging.getLogger(__name__)
    logger.setLevel(args.logging)
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(handler)

    if args.check:
        get_file = requests.get("http://ci-artifacts.spb.yadro.com/"
                                "ci-artifacts/deploy-info/a.pavlov/{}"
                         .format(output_file)).text.splitlines()
        dict_to_compare = dict(x.rstrip().split(None, 1) for x in get_file)

    with open(output_file, "w") as file_to_write:
        for file in walk_directory(str(args.directory)):
            if args.check:
                is_file_changed = file.check(dict_to_compare[file.path])
                if is_file_changed:
                    logger.debug("%s is not changed", file.path)
                else:
                    logger.info("%s is changed", file.path)
            else:
                try:
                    md5 = file.md5sum()
                    file_to_write.write(f"{file.path} {md5}\n")
                except IOError as error:
                    logger.critical("Error:%s", error)
        file_to_write.close()


if __name__ == '__main__':
    sys.exit(__main__())
