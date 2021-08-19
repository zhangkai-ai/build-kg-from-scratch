#!/usr/bin/env bash
# tsv_extractor  process/ext_player_club_feature_by_extract_features
# {"dependencies":["ext_player_mention_by_map_player_mention","ext_club_mention_by_map_club_mention","ext_sentences_by_nlp_markup"],"input":" SELECT R0.mention_id AS \"player_mention.R0.mention_id\", R1.mention_id AS \"club_mention.R1.mention_id\", R0.begin_index AS \"player_mention.R0.begin_index\", R0.end_index AS \"player_mention.R0.end_index\", R1.begin_index AS \"club_mention.R1.begin_index\", R1.end_index AS \"club_mention.R1.end_index\", R0.doc_id AS \"player_mention.R0.doc_id\", R0.sentence_index AS \"player_mention.R0.sentence_index\", R2.tokens AS \"sentences.R2.tokens\", R2.lemmas AS \"sentences.R2.lemmas\", R2.pos_tags AS \"sentences.R2.pos_tags\", R2.ner_tags AS \"sentences.R2.ner_tags\", R2.dep_types AS \"sentences.R2.dep_types\", R2.dep_tokens AS \"sentences.R2.dep_tokens\"\nFROM player_mention R0, club_mention R1, sentences R2\n        WHERE R1.doc_id = R0.doc_id  AND R1.sentence_index = R0.sentence_index  AND R2.doc_id = R0.doc_id  AND R2.sentence_index = R0.sentence_index \n          ","input_batch_size":"100000","input_relations":["player_mention","club_mention","sentences"],"output_relation":"player_club_feature","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/extract_features.py","dependencies_":["process/ext_player_mention_by_map_player_mention","process/ext_club_mention_by_map_club_mention","process/ext_sentences_by_nlp_markup"],"input_":["data/player_mention","data/club_mention","data/sentences"],"output_":"data/player_club_feature","name":"process/ext_player_club_feature_by_extract_features"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_player_club_feature_by_extract_features'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R0.mention_id AS "player_mention.R0.mention_id", R1.mention_id AS "club_mention.R1.mention_id", R0.begin_index AS "player_mention.R0.begin_index", R0.end_index AS "player_mention.R0.end_index", R1.begin_index AS "club_mention.R1.begin_index", R1.end_index AS "club_mention.R1.end_index", R0.doc_id AS "player_mention.R0.doc_id", R0.sentence_index AS "player_mention.R0.sentence_index", R2.tokens AS "sentences.R2.tokens", R2.lemmas AS "sentences.R2.lemmas", R2.pos_tags AS "sentences.R2.pos_tags", R2.ner_tags AS "sentences.R2.ner_tags", R2.dep_types AS "sentences.R2.dep_types", R2.dep_tokens AS "sentences.R2.dep_tokens"
FROM player_mention R0, club_mention R1, sentences R2
        WHERE R1.doc_id = R0.doc_id  AND R1.sentence_index = R0.sentence_index  AND R2.doc_id = R0.doc_id  AND R2.sentence_index = R0.sentence_index 
          ' \
    command='"$DEEPDIVE_APP"/udf/extract_features.py' \
    output_relation='player_club_feature' \
    #



