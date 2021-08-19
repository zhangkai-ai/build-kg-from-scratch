#!/usr/bin/env bash
# tsv_extractor  process/ext_player_mention_by_map_player_mention
# {"dependencies":["ext_sentences_by_nlp_markup"],"input":" SELECT R0.doc_id AS \"sentences.R0.doc_id\", R0.sentence_index AS \"sentences.R0.sentence_index\", R0.tokens AS \"sentences.R0.tokens\", R0.ner_tags AS \"sentences.R0.ner_tags\"\nFROM sentences R0\n        \n          ","input_batch_size":"100000","input_relations":["sentences"],"output_relation":"player_mention","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/map_player_mention.py","dependencies_":["process/ext_sentences_by_nlp_markup"],"input_":["data/sentences"],"output_":"data/player_mention","name":"process/ext_player_mention_by_map_player_mention"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_player_mention_by_map_player_mention'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R0.doc_id AS "sentences.R0.doc_id", R0.sentence_index AS "sentences.R0.sentence_index", R0.tokens AS "sentences.R0.tokens", R0.ner_tags AS "sentences.R0.ner_tags"
FROM sentences R0
        
          ' \
    command='"$DEEPDIVE_APP"/udf/map_player_mention.py' \
    output_relation='player_mention' \
    #



