import ast
from operator import itemgetter
import re
from time import clock_getres
# from memory_profiler import profile
from argparse import ArgumentParser
from tempfile import TemporaryDirectory, mktemp
import os, sys
import heapq
from contextlib import contextmanager

def key_funct(line):
    list_line = ast.literal_eval(line)
    print("List Line", list_line)
    return [x[1] for x in list_line] 


def large_sort(input_file, output_file, reverse: bool=False):

    with TemporaryDirectory() as tmp_dir:
        lines2 = []
        for lines in _read_parts(input_file):
            dict1 = {}
            for l in lines:
                ze_tokens = l.split(' ')
                dict1[ze_tokens[0]] = int(ze_tokens[1])
            # lines1 = sorted(dict1, key=dict1.get, reverse=True)
            # print("LINES", lines1)
            lines1 = sorted(dict1.items(), key=lambda x: x[1], reverse=True)
            print("lines1", lines1)
            lines2.append(lines1)
            print("lines2", lines2)
            _write_part(lines1, tmp_dir)

        with _open_tmp_files(tmp_dir) as tmp_files:
            print("tmp1: ", tmp_files[0].read(), "tmp2:", tmp_files[1].readlines())
            print("Heap", list(heapq.merge(*tmp_files, key=key_funct, reverse=True)))
            for row in heapq.merge(*tmp_files, key=key_funct, reverse=True):
                print('Heapq \n', row)
                # output_file.write(row)
                # print(output_file)
        
    # return lines1
    # with _open_tmp_files(tmp_dir) as tmp_files:
    #     for row in heapq.merge(*tmp_files, key=key, reverse=reverse):
    #         output_file.write(row)


def _read_parts(input_file):
    lines = input_file.readlines(40)
    print(2, lines)
    while lines:
        yield lines
        lines = input_file.readlines(40)

def _write_part(lines, tmp_dir):
    print("call")
    tmp_filename = mktemp(dir=tmp_dir)
    with open(tmp_filename, "w") as tmp_file:
        # lines1 = sorted(lines, key=lines.get, reverse=True)
        # lines1 = dict(sorted(lines.items(), key=lambda x: x[1], reverse=True))
        # print("A", lines1)
        tmp_file.writelines(str(lines))
    return tmp_filename

@contextmanager
def _open_tmp_files(tmp_dir):
    filenames = os.listdir(tmp_dir)
    files = [open(os.path.join(tmp_dir, filename), "r") for filename in filenames]
    try:
        yield files
    finally:
        for file in files:
            file.close()

def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("file", nargs="?", help="入力ファイル")
    parser.add_argument("out_file", nargs="?", help="入力ファイル")
    return parser.parse_args()

# @profile(precision=4)
def main():
    args = _parse_args()
    print("args", args)
    file = open(args.file, "r")
    large_sort(file, sys.stdout)
    # print("Newlines", newLines)
    # dict1 = {}
    # ze_file = open("input.txt", 'r')
    # ze_lines = ze_file.readlines(150)
    # print("ze",ze_lines)
    # for l in ze_lines:
    #     ze_tokens = l.split(' ')
    #     dict1[ze_tokens[0]] = int(ze_tokens[1])
    # print(dict1)
    # print(sorted(dict1, key=dict1.get, reverse=True)[0:3])
    # ze_file.close()

main()