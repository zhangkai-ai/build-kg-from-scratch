#!/usr/bin/env bash
# tsv_extractor  process/ext_sentences_by_nlp_markup
# {"input":" SELECT R0.id AS \"information.R0.id\", R0.content AS \"information.R0.content\"\nFROM information R0\n        \n          ","input_batch_size":"100000","input_relations":["information"],"output_relation":"sentences","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/nlp_markup.sh","dependencies_":[],"input_":["data/information"],"output_":"data/sentences","name":"process/ext_sentences_by_nlp_markup"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_sentences_by_nlp_markup'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R0.id AS "information.R0.id", R0.content AS "information.R0.content"
FROM information R0
        
          ' \
    command='"$DEEPDIVE_APP"/udf/nlp_markup.sh' \
    output_relation='sentences' \
    #



