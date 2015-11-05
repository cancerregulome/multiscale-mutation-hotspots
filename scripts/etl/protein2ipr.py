from csv import DictReader, DictWriter, reader
from sys import argv as sys_argv

from gzip import open as gzip_open


FIELDNAMES = ['uniprot_accession', 'interpro_id', 'name', 'database', 'start', 'end']
PRINT_LIMIT = 1000000


# Generator
def read_file(input_file_path):
    infile = None
    if input_file_path.endswith('.gz'):
        infile = gzip_open(input_file_path)
    else:
        infile = open(input_file_path, 'r+b')

    count = 0
    total_records = 0

    csv_reader = reader(infile, delimiter='\t')

    for line in csv_reader:
        count += 1
        if count >= PRINT_LIMIT:
            total_records += count
            count = 0
            print("Processed " + str(total_records))

        item = {}
        for index, field in enumerate(FIELDNAMES):
            item[field] = line[index]

        item['start'] = int(item['start'])
        item['end'] = int(item['end'])
        yield item

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
    protein2ipr_tsv_path = sys_argv[2]
    outfile_path = sys_argv[3]

    writer = DictWriter(open(outfile_path, 'w'), fieldnames=FIELDNAMES)
    writer.writeheader()

    whitelist = build_uniprot_id_whitelist_from_tsv(whitelist_tsv_path)
    print("Whitelist size: " + str(len(whitelist)))

    for item in read_file(protein2ipr_tsv_path):
        if item['uniprot_accession'] not in whitelist:
            continue

        writer.writerow(item)

if __name__ == '__main__':
    main()
