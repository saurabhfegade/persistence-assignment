"""
This script is reading the input from the file input.txt and writing the output to the file output.txt. 
It reads the input file in chunks of 1MB, sorts each chunk in memory, writes the sorted chunk to a temporary file, 
then merges the sorted chunks using the heapq.merge function.
    
:param line: The line to be sorted
:return: The "COUNT" largest elements

Usage: 
From the command line - python assignment.py 5 < input.txt > output.txt
Here 5 is the count to return 5 largest numbers

Time complexity: nlog(n)
Space complexity: O(n) 
"""
from argparse import ArgumentParser
import sys
from functools import partial
from heapq import merge
from tempfile import TemporaryFile
# import cProfile
# from memory_profiler import profile

# sorting criteria
def key_func(line):
    try:
        return int(line.split(" ")[1]) # e.g. for (1426828011 9) it will select second element to sort with
    except (IndexError, ValueError):
        return None 

# take count by parsing arguments
def _parse_args():
    """
    It parses the command line arguments and returns them as a dictionary
    :return: The number of arguments passed in.
    """
    parser = ArgumentParser()
    parser.add_argument("count", default=2)
    return parser.parse_args()

# Sorting function based on count to be returned and chunk size in bytes
def sort_file(count, nbytes):
    sorted_files = []
    for lines in iter(partial(sys.stdin.readlines, nbytes), []):
        lines.sort(key=key_func, reverse=True) 
        f = TemporaryFile("w+")
        f.writelines(lines)
        f.seek(0)
        sorted_files.append(f)

    merged_list =  list(merge(*sorted_files, key=key_func, reverse=True))   # merge the sorted temporary files based on key function

    sys.stdout.writelines([f'{x.split(" ")[0]}\n' for x in merged_list[0:int(count)]])     # write into stdout the "COUNT" largest elements  

    # clean up
    for f in sorted_files:
        f.close()

# @profile 
def main():
    args = _parse_args() 
    count = int(args.count)
    nbytes = 1 << 20 
    if count >= 0:
        sort_file(count, nbytes)           # 1048576 bytes at a time to be used in memory
    else:
        raise ValueError("Negative count not allowed.")
    
main()

# cProfile.run("main()")