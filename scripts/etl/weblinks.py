"""
Removes leading and trailing whitespace from the pathway names.
"""

from csv import reader, writer
from sys import stdin, stdout

infile = reader(stdin, delimiter='\t')
outfile = writer(stdout, delimiter='\t')

# Skip header
next(infile)
for pathway_name, uri in infile:
    outfile.writerow([pathway_name.strip(), uri])

