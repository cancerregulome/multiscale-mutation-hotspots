from csv import DictReader, DictWriter
from parsley import makeGrammar
from StringIO import StringIO
from sys import argv as sys_argv

from gzip import open as gzip_open
from re import compile as re_compile

UNIPROT_GRAMMAR = makeGrammar("""
CRLF      = '\n'
entry     = 'ID' ws <(letterOrDigit|'_')+>:code -> code
ID        = entry:e ws ('Reviewed'|'Unreviewed') ';' ws <digit+>:length ws 'AA.' CRLF -> (e, int(length))
accession = <letterOrDigit+>:code ';' -> code
AC        = 'AC' ws accession:code -> code
DT        = 'DT' (~CRLF anything)* CRLF
DE        = 'DE' ws 'RecName:' ws 'Full=' <(letterOrDigit|' ')+>:name ';' CRLF -> name
REST      = anything*
record    = CRLF* ID:id AC:ac DT* DE:name REST -> {'accession': ac, 'entry_name': id[0], 'length': id[1], 'protein_name': name}
""", {})

UNIPROT_RECORD_TERMINATOR = re_compile('^//')
FIELDNAMES = ['accession', 'entry_name', 'length', 'protein_name']
PRINT_LIMIT = 10000

# Generator
def read_file(input_file_path):
    infile = None
    if input_file_path.endswith('.gz'):
        infile = gzip_open(input_file_path)
    else:
        infile = open(input_file_path, 'r+b')

    count = 0
    total_records = 0
    chunk = StringIO()
    for line in infile:
        if len(UNIPROT_RECORD_TERMINATOR.findall(line)) == 0:
            chunk.write(line)
        else:
            count += 1
            if count >= PRINT_LIMIT:
                total_records += count
                count = 0
                print("Processed " + str(total_records))

            uniprot_record = chunk.getvalue()
            parsed = None
            try:
                parsed = UNIPROT_GRAMMAR(uniprot_record).record()
            except Exception as e:
                pass

            chunk = StringIO()
            if parsed is None:
                continue

            yield parsed

    infile.close()

def load_uniprot_id_list_tsv(file_path):
    field = 'protein_ID'
    result = []
    reader = DictReader(open(file_path, "rb"), fieldnames=[field])
    for row in reader:
        result.append(row[field])

    return result

def build_uniprot_id_whitelist_from_tsv(file_path):
    whitelist = load_uniprot_id_list_tsv(file_path)
    return frozenset(whitelist)

def main():
    whitelist_tsv_path = sys_argv[1]
    uniprot_sprot_dat_path = sys_argv[2]
    outfile_path = sys_argv[3]

    writer = DictWriter(open(outfile_path, 'w'), fieldnames=FIELDNAMES)

    whitelist = build_uniprot_id_whitelist_from_tsv(whitelist_tsv_path)
    print("Whitelist size: " + str(len(whitelist)))

    for item in read_file(uniprot_sprot_dat_path):
        if item['accession'] not in whitelist:
            continue
        writer.writerow(item)

    writer.close()

if __name__ == '__main__':
    main()
