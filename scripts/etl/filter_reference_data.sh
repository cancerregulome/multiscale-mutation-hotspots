#!/usr/bin/env bash

DATA_ROOT=$1
DATA_SRC=$DATA_ROOT/data
DATA_TMP=$DATA_ROOT/temp
DATA_TRG=$DATA_ROOT/sqlite
LOGDIR=$DATA_ROOT/logs


# Filter UniProt reference dataset
(
echo "Filtering UniProt reference dataset..."
python ./uniprot.py $DATA_TRG/uniprot_ids.txt $DATA_ROOT/reference/uniprot_sprot.dat.gz $DATA_TRG/uniprot_db.tsv 1>$LOGDIR/uniprot.log 2>&1
) &

# Filter InterPro reference dataset
(
echo "Filtering InterPro reference dataset..."
python ./protein.py $DATA_TRG/uniprot_ids.txt $DATA_ROOT/reference/protein2ipr.dat.gz $DATA_TRG/protein2ipr_pfam.tsv 1>$LOGDIR/protein2ipr.log 2>&1
) &
