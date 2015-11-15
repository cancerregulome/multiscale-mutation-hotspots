#!/usr/bin/env bash

echo "cancer\tgene\tcluster\tmissense_mutations\tnonsense_mutation\tsilent_mutations\tincluded_in_gexp_analysis"
tail -n+2 $1
