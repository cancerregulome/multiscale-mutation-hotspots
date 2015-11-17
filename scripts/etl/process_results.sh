#!/usr/bin/env bash

DATA_ROOT=$1
DATA_SRC=$DATA_ROOT/data
DATA_TMP=$DATA_ROOT/temp
DATA_TRG=$DATA_ROOT/sqlite

# Remove header from cluster definitions file
echo "Cluster definitions..."
cat $DATA_SRC/sup_tbl_1_cluster_definitions_with_domains.tsv | tail -n+2 > $DATA_TRG/clusters_definitions.tsv

# Remove header from cluster tumor type assignment file
echo "Cluster/tumor type assignments..."
cat $DATA_SRC/sup_tbl_2_clusters_tumor_type_assignment.tsv | tail -n+2 > $DATA_TRG/clusters_tumor_type_assignment.tsv

# Remove header from pathway associations file
echo "Pathway associations..."
cat $DATA_SRC/sup_tbl_5_pathway_gexp_associations.tsv | tail -n+2 > $DATA_TRG/pathway_associations.tsv

# Remove UNIPROT_FAIL lines from the mutation summary
echo "Filtering mutation summary..."
cat $DATA_SRC/mutation_summary.tsv | grep -v UNIPROT_FAIL > $DATA_TRG/mutation_summary.tsv

# Find unique UniProt accession codes from the mutation summary
echo "Finding UniProt accession codes..."
cat $DATA_TRG/mutation_summary.tsv | cut -f 7 | awk '!array[$1]++' > $DATA_TRG/uniprot_ids.txt

# Find unique genes from the mutation summary
echo "Generating gene list for Python..."
echo "gene_list = [" > $DATA_TRG/gene_list.py
cat $DATA_TRG/mutation_summary.tsv | cut -f 2| awk '!array[$1]++' | awk '{printf("    \"%s\"\n", $0);}' >> $DATA_TRG/gene_list.py
echo "]" >> $DATA_TRG/gene_list.py

