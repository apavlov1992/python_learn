#!/usr/bin/env python


import sys
import argparse
import os
import hashlib


class Walk:

    def print_usage():
        print('Usage: python dir_check.py -d <dir_to_check> or python dir_check.py -c -d <dir_to_check> to check diff')

    def compare_sha(self, walk_sha, sha):
        if walk_sha == sha:
            return True
        else:
            return False

    def walk_directory(self, dir_to_check, blocksize: int = 4096):
        for root, directories, files in os.walk(dir_to_check, topdown=False):
            for name in files:
                hasher_fn = hashlib.md5()
                with open((os.path.join(root, name)), 'rb') as afile:
                    buf = afile.read(blocksize)
                    hasher_fn.update(buf)
                    files_md5sum = os.path.join(root, name), hasher_fn.hexdigest()
                    yield files_md5sum


# задефайнить коды возврата
BAD_ARGUMENTS_ERROR = 1


def __main__(args=None):
    if args is None:
        args = sys.argv[1:]

    d = Walk

    # if len(args) not in range(1, 2, 3):
    #     d.print_usage()
    #     return BAD_ARGUMENTS_ERROR

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
                        help='Recursive check md5sum file and write to file')
    parser.add_argument('-c', '--check', action='store_true',
                        help="Check previously file for diff")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output to console")
    parser.add_argument('-o', '--outputfile', action='store', dest='outputfile', default='output_without_check')
    args = parser.parse_args(args)
    output_file = args.outputfile
    # убрать -d из аргументов
    # ключ для вывода в консоль stdout
    # ключ quiet (или silent), который убирает весь оутпут

    if args.check:
        try:
            with open(output_file) as f:
                dict_to_compare = dict(x.rstrip().split(None, 1) for x in f)
                for walk_path, walk_sha in d.walk_directory(None, str(args.directory)):
                    if d.compare_sha(None, walk_sha, dict_to_compare.get(walk_path)):
                        if args.quiet:
                            return 0 #вот тут криво, я хотел спросить как придумать, чтобы либо 1 либо 0 было не в цикле
                        else:
                            print("File: {} is not changed".format(walk_path))
                    else:
                        if args.quiet:
                            return 1 #тут тот же вопрос
                        else:
                            print("File: {} is changed".format(walk_path))
        except Exception:
            print('Error: {} '.format(Exception))
    else:
        try:
            open(output_file, "w").close()
            for path, sha in d.walk_directory(None, str(args.directory)):
                open(output_file, "a").write("{} {}\n".format(path, sha))
        except Exception as e:
            print('Error: {} '.format(e))


if __name__ == '__main__':
    sys.exit(__main__())
