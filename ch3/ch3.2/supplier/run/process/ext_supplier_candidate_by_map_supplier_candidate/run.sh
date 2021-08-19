#!/usr/bin/env bash
# tsv_extractor  process/ext_supplier_candidate_by_map_supplier_candidate
# {"dependencies":["ext_company_mention_by_map_company_mention"],"input":" SELECT R0.mention_id AS \"company_mention.R0.mention_id\", R0.mention_text AS \"company_mention.R0.mention_text\", R1.mention_id AS \"company_mention.R1.mention_id\", R1.mention_text AS \"company_mention.R1.mention_text\"\nFROM company_mention R0, company_mention R1\n        WHERE R1.doc_id = R0.doc_id  AND R1.sentence_index = R0.sentence_index \n          ","input_batch_size":"100000","input_relations":["company_mention"],"output_relation":"supplier_candidate","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/map_supplier_candidate.py","dependencies_":["process/ext_company_mention_by_map_company_mention"],"input_":["data/company_mention"],"output_":"data/supplier_candidate","name":"process/ext_supplier_candidate_by_map_supplier_candidate"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_supplier_candidate_by_map_supplier_candidate'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R0.mention_id AS "company_mention.R0.mention_id", R0.mention_text AS "company_mention.R0.mention_text", R1.mention_id AS "company_mention.R1.mention_id", R1.mention_text AS "company_mention.R1.mention_text"
FROM company_mention R0, company_mention R1
        WHERE R1.doc_id = R0.doc_id  AND R1.sentence_index = R0.sentence_index 
          ' \
    command='"$DEEPDIVE_APP"/udf/map_supplier_candidate.py' \
    output_relation='supplier_candidate' \
    #



