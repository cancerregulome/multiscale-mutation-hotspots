"""
Normalizes the tumor type indicator to abbreviation only, eg. "ACC-TP" to "ACC".
"""

from csv import reader, writer
from sys import stdin, stdout

infile = reader(stdin, delimiter='\t')
outfile = writer(stdout, delimiter='\t')

for row in infile:
    tumor_type = row[0].split('-')[0]
    outfile.writerow([tumor_type] + row[1:])

