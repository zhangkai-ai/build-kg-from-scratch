#!/usr/bin/env bash
# tsv_extractor  process/ext_relation_label__0_by_supervise
# {"dependencies":["ext_supplier_candidate_by_map_supplier_candidate","ext_company_mention_by_map_company_mention","ext_sentences_by_nlp_markup"],"input":" SELECT R0.p1_id AS \"supplier_candidate.R0.p1_id\", R1.begin_index AS \"company_mention.R1.begin_index\", R1.end_index AS \"company_mention.R1.end_index\", R0.p2_id AS \"supplier_candidate.R0.p2_id\", R2.begin_index AS \"company_mention.R2.begin_index\", R2.end_index AS \"company_mention.R2.end_index\", R1.doc_id AS \"company_mention.R1.doc_id\", R1.sentence_index AS \"company_mention.R1.sentence_index\", R3.sentence_text AS \"sentences.R3.sentence_text\", R3.tokens AS \"sentences.R3.tokens\", R3.lemmas AS \"sentences.R3.lemmas\", R3.pos_tags AS \"sentences.R3.pos_tags\", R3.ner_tags AS \"sentences.R3.ner_tags\", R3.dep_types AS \"sentences.R3.dep_types\", R3.dep_tokens AS \"sentences.R3.dep_tokens\"\nFROM supplier_candidate R0, company_mention R1, company_mention R2, sentences R3\n        WHERE R1.mention_id = R0.p1_id  AND R2.mention_id = R0.p2_id  AND R3.doc_id = R1.doc_id  AND R3.sentence_index = R1.sentence_index \n          ","input_batch_size":"100000","input_relations":["supplier_candidate","company_mention","sentences"],"output_relation":"relation_label__0","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/supervise_relation.py","dependencies_":["process/ext_supplier_candidate_by_map_supplier_candidate","process/ext_company_mention_by_map_company_mention","process/ext_sentences_by_nlp_markup"],"input_":["data/supplier_candidate","data/company_mention","data/sentences"],"output_":"data/relation_label__0","name":"process/ext_relation_label__0_by_supervise"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_relation_label__0_by_supervise'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R0.p1_id AS "supplier_candidate.R0.p1_id", R1.begin_index AS "company_mention.R1.begin_index", R1.end_index AS "company_mention.R1.end_index", R0.p2_id AS "supplier_candidate.R0.p2_id", R2.begin_index AS "company_mention.R2.begin_index", R2.end_index AS "company_mention.R2.end_index", R1.doc_id AS "company_mention.R1.doc_id", R1.sentence_index AS "company_mention.R1.sentence_index", R3.sentence_text AS "sentences.R3.sentence_text", R3.tokens AS "sentences.R3.tokens", R3.lemmas AS "sentences.R3.lemmas", R3.pos_tags AS "sentences.R3.pos_tags", R3.ner_tags AS "sentences.R3.ner_tags", R3.dep_types AS "sentences.R3.dep_types", R3.dep_tokens AS "sentences.R3.dep_tokens"
FROM supplier_candidate R0, company_mention R1, company_mention R2, sentences R3
        WHERE R1.mention_id = R0.p1_id  AND R2.mention_id = R0.p2_id  AND R3.doc_id = R1.doc_id  AND R3.sentence_index = R1.sentence_index 
          ' \
    command='"$DEEPDIVE_APP"/udf/supervise_relation.py' \
    output_relation='relation_label__0' \
    #



