import parsley

uniprot = parsley.makeGrammar("""
CRLF      = '\n'
entry     = 'ID' ws (letterOrDigit|'_')+:code -> ''.join(code)
ID        = entry:e ws 'Reviewed;' ws (digit)+:length ' ' 'AA.' CRLF -> (e, int(''.join(length)))
AC        = 'AC' ws (letterOrDigit)+:accession ';' CRLF -> ''.join(accession)
DT        = 'DT' anything* CRLF
DE        = 'DE' ws 'RecName:' ws 'Full=' (letterOrDigit|' ')+:name ';' CRLF -> ''.join(name)

record    =  CRLF+ ID:id AC:ac DT* DE:name anything* end -> {'accession': ac, 'entry_name': id[0], 'length': id[1], 'protein_name': name}
""", {})


