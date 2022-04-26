from argparse import ArgumentParser
import sys
from functools import partial
from heapq import merge
from tempfile import TemporaryFile

# sorting criteria
def key_func(line):
    try:
        return int(line.split(" ")[1]) 
    except (IndexError, ValueError):
        return None 


def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("count", default=2)
    return parser.parse_args()

def main():
    args = _parse_args()
    sorted_files = []
    nbytes = 1 << 20 
    for lines in iter(partial(sys.stdin.readlines, nbytes), []):
        lines.sort(key=key_func, reverse=True) 
        f = TemporaryFile("w+")
        f.writelines(lines)
        f.seek(0)
        sorted_files.append(f)

    merged_list =  list(merge(*sorted_files, key=key_func, reverse=True))

    sys.stdout.writelines([f'{x.split(" ")[0]}\n' for x in merged_list[0:int(args.count)]])

    # clean up
    for f in sorted_files:
        f.close()

main()