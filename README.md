This script is reading the input from the file input.txt and writing the output to the file output.txt.
It reads the input file in chunks of 1MB, sorts each chunk in memory, writes the sorted chunk to a temporary file,
then merges the sorted chunks using the heapq.merge function.

## Usage:

From the command line - python assignment.py 5 < input.txt > output.txt
Here 5 is the count to return 5 largest numbers

Note: Python3 should be installed
