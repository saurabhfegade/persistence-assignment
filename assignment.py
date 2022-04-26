"""
Usage: 
From the command line - python assignment.py 5 < input.txt > output.txt
Here 5 is the count to return 5 largest numbers
"""

from argparse import ArgumentParser
import sys
from functools import partial
from heapq import merge
from tempfile import TemporaryFile

# sorting criteria
def key_func(line):
    try:
        return int(line.split(" ")[1]) # e.g. for (1426828011 9) it will select second element to sort with
    except (IndexError, ValueError):
        return None 

# take count by parsing arguments
def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("count", default=2)
    return parser.parse_args()

def main():
    args = _parse_args()
    sorted_files = []
    nbytes = 1 << 20            # 1048576 bytes at a time to be used in memory
    for lines in iter(partial(sys.stdin.readlines, nbytes), []):
        lines.sort(key=key_func, reverse=True) 
        f = TemporaryFile("w+")
        f.writelines(lines)
        f.seek(0)
        sorted_files.append(f)

    merged_list =  list(merge(*sorted_files, key=key_func, reverse=True))   # merge the sorted temporary files based on key function

    sys.stdout.writelines([f'{x.split(" ")[0]}\n' for x in merged_list[0:int(args.count)]])     # write into stdout the "COUNT" largest elements  

    # clean up
    for f in sorted_files:
        f.close()

main()