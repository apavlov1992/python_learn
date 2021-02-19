#!/usr/bin/env python


import sys
import json
import argparse
import os
import hashlib
import json
import difflib

# убрать
d = difflib.Differ()
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--check', action='store_true',
                    help="Check previously file for diff")
# добавить больше директорий
parser.add_argument('-d', '--directory', nargs=1, type=str,
                    help="Recursive check md5sum file and write to file")
args = parser.parse_args()

class Walk:
    list_of_files = []
    output_file = 'output_without_check.json' #добавить в параметры, но использовать по дефолту
    output_file_check = 'output_with_check.json' #убираем, вывод теперь только в консоль и работаем с памятью

    def print_usage():
        print('Usage: python dir_check.py -d <dir_to_check> or python dir_check.py -c -d <dir_to_check> to check diff')


#переписать на итератор с использованием функции yield
    def walk_directory(self, dir_to_check, output_file):
        hasher_fn = hashlib.md5()
        for root, directories, files in os.walk(dir_to_check, topdown=False):
            for name in files:
                with open((os.path.join(root, name)), 'r') as afile:
                    buf = afile.read()
                    hasher_fn.update(buf.encode('utf-8'))
                files_md5sum = {os.path.join(root, name): hasher_fn.hexdigest()}
                Walk.list_of_files.append(files_md5sum)
            with open(output_file, 'w') as f:
                f.write(json.dumps(Walk.list_of_files, indent=2, sort_keys=True))

def try_yield(dir_to_check):
    hasher_fn = hashlib.md5()
    for root, directories, files in os.walk(dir_to_check, topdown=False):
        for name in files:
            with open((os.path.join(root, name)), 'r') as afile:
                buf = afile.read()
                hasher_fn.update(buf.encode('utf-8'))
            files_md5sum = {os.path.join(root, name): hasher_fn.hexdigest()}
            yield files_md5sum


g = try_yield(str(args.directory[0]))

print(next(g))





#проверить, как считается md5 у бинарных файлов
#до и после модуль timeit - измерять время работы скрипта для режима check ( сгенерить 1000 файлов ) суммарное время и среднее за 10к прогонов

#задефайнить коды возврата
# BAD_ARGUMENTS_ERROR = 1


# def __main__():
#     d = difflib.Differ()
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-c', '--check', action='store_true',
#                         help="Check previously file for diff")
#     # добавить больше директорий
#     parser.add_argument('-d', '--directory', nargs=1, type=str,
#                         help="Recursive check md5sum file and write to file")
#     args = parser.parse_args()
#     # убрать -d из аргументов
#     # ключ для вывода в консоль stdout
#     # ключ quiet (или silent), который убирает весь оутпут
#     if len(sys.argv) in range(2, 3):
#         Walk.print_usage()
#         return BAD_ARGUMENTS_ERROR

    # if args.check:
    #     try:
    #         with open(Walk.output_file) as json_file:
    #             output_file_json = json.load(json_file)
    #         Walk.walk_directory(None, str(args.directory[0]), Walk.output_file_check)
    #         if d.compare(Walk.list_of_files, output_file_json):
    #             Walk.list_of_files == output_file_json
    #             return 1
    #         else:
    #             return 0
    #     except KeyError:
    #         print('Error: {} '.format(KeyError))
    # else:
    #     #добавить параметр для названия файла
    #     Walk.walk_directory(None, str(args.directory[0]), Walk.output_file)




# if __name__ == '__main__':
#     sys.exit(__main__())
