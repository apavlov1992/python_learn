#!/usr/bin/env python


import sys
import json
import argparse
# убрать
from jsondiff import diff
#задефайнить класс в файл
import dir_check_class

#задефайнить коды возврата
BAD_ARGUMENTS_ERROR = 1

d = dir_check_class.Walk

#убрать в main
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--check', action='store_true',
                    help="Check previously file for diff")
#добавить больше директорий
parser.add_argument('-d', '--directory', nargs=1, type=str,
                    help="Recursive check md5sum file and write to file")
args = parser.parse_args()
#убрать -d из аргументов
#ключ для вывода в консоль stdout
#ключ quiet (или silent), который убирает весь оутпут

def __main__():
    if len(sys.argv) in range(2, 3):
        d.print_usage()
        return BAD_ARGUMENTS_ERROR

    if args.check:
        try:
            with open(d.output_file) as json_file:
                output_file_json = json.load(json_file)
            d.walk_directory(None, str(args.directory[0]), d.output_file_check)
            if diff(d.list_of_files, output_file_json):
                print(diff(output_file_json, d.list_of_files))
                return 1
            else:
                return 0
        except KeyError:
            print('Error: {} '.format(KeyError))
    else:
        #добавить параметр для названия файла
        d.walk_directory(None, str(args.directory[0]), d.output_file)




if __name__ == '__main__':
    sys.exit(__main__())
