#!/usr/bin/env bash
# tsv_extractor  process/ext_company_mention_by_map_company_mention
# {"dependencies":["ext_sentences_by_nlp_markup"],"input":" SELECT R0.doc_id AS \"sentences.R0.doc_id\", R0.sentence_index AS \"sentences.R0.sentence_index\", R0.tokens AS \"sentences.R0.tokens\", R0.ner_tags AS \"sentences.R0.ner_tags\"\nFROM sentences R0\n        \n          ","input_batch_size":"100000","input_relations":["sentences"],"output_relation":"company_mention","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/map_company_mention.py","dependencies_":["process/ext_sentences_by_nlp_markup"],"input_":["data/sentences"],"output_":"data/company_mention","name":"process/ext_company_mention_by_map_company_mention"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_company_mention_by_map_company_mention'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R0.doc_id AS "sentences.R0.doc_id", R0.sentence_index AS "sentences.R0.sentence_index", R0.tokens AS "sentences.R0.tokens", R0.ner_tags AS "sentences.R0.ner_tags"
FROM sentences R0
        
          ' \
    command='"$DEEPDIVE_APP"/udf/map_company_mention.py' \
    output_relation='company_mention' \
    #



