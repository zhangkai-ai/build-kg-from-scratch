#!/usr/bin/env bash
# cmd_extractor  process/ext_relation_label
# {"cmd":"\n\n\t# TODO use temporary table\n\tdeepdive create table \"relation_label\"\n\tdeepdive sql 'INSERT INTO relation_label SELECT R0.p1_id AS \"supplier_candidate.R0.p1_id\", R0.p2_id AS \"supplier_candidate.R0.p2_id\", 0 AS column_2, NULL AS column_3\nFROM supplier_candidate R0\n        \nUNION ALL\nSELECT R0.p1_id AS \"supplier_candidate.R0.p1_id\", R0.p2_id AS \"supplier_candidate.R0.p2_id\", 3 AS column_2, '\\''from_dbdata'\\'' AS column_3\nFROM supplier_candidate R0, supplier_dbdata R1\n        WHERE (lower(R1.company_a_name) = lower(R0.p1_name) AND lower(R1.company_b_name) = lower(R0.p2_name))\nUNION ALL\nSELECT R0.p1_id AS \"supplier_candidate.R0.p1_id\", R0.p2_id AS \"supplier_candidate.R0.p2_id\", -3 AS column_2, '\\''from_dbdata'\\'' AS column_3\nFROM supplier_candidate R0, supplier_dbdata_2 R1\n        WHERE (lower(R1.company_a_name) = lower(R0.p1_name) AND lower(R1.company_b_name) = lower(R0.p2_name))\nUNION ALL\nSELECT R0.p1_id AS \"relation_label__0.R0.p1_id\", R0.p2_id AS \"relation_label__0.R0.p2_id\", R0.label AS \"relation_label__0.R0.label\", R0.rule_id AS \"relation_label__0.R0.rule_id\"\nFROM relation_label__0 R0\n        '\n\t# TODO rename temporary table to replace output_relation\n\t\n        ","dependencies":["ext_supplier_candidate_by_map_supplier_candidate","ext_relation_label__0_by_supervise"],"input_relations":["supplier_candidate","supplier_dbdata","supplier_dbdata_2","relation_label__0"],"output_relation":"relation_label","style":"cmd_extractor","dependencies_":["process/ext_supplier_candidate_by_map_supplier_candidate","process/ext_relation_label__0_by_supervise"],"input_":["data/supplier_candidate","data/supplier_dbdata","data/supplier_dbdata_2","data/relation_label__0"],"output_":"data/relation_label","name":"process/ext_relation_label"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_relation_label'


	# TODO use temporary table
	deepdive create table "relation_label"
	deepdive sql 'INSERT INTO relation_label SELECT R0.p1_id AS "supplier_candidate.R0.p1_id", R0.p2_id AS "supplier_candidate.R0.p2_id", 0 AS column_2, NULL AS column_3
FROM supplier_candidate R0
        
UNION ALL
SELECT R0.p1_id AS "supplier_candidate.R0.p1_id", R0.p2_id AS "supplier_candidate.R0.p2_id", 3 AS column_2, '\''from_dbdata'\'' AS column_3
FROM supplier_candidate R0, supplier_dbdata R1
        WHERE (lower(R1.company_a_name) = lower(R0.p1_name) AND lower(R1.company_b_name) = lower(R0.p2_name))
UNION ALL
SELECT R0.p1_id AS "supplier_candidate.R0.p1_id", R0.p2_id AS "supplier_candidate.R0.p2_id", -3 AS column_2, '\''from_dbdata'\'' AS column_3
FROM supplier_candidate R0, supplier_dbdata_2 R1
        WHERE (lower(R1.company_a_name) = lower(R0.p1_name) AND lower(R1.company_b_name) = lower(R0.p2_name))
UNION ALL
SELECT R0.p1_id AS "relation_label__0.R0.p1_id", R0.p2_id AS "relation_label__0.R0.p2_id", R0.label AS "relation_label__0.R0.label", R0.rule_id AS "relation_label__0.R0.rule_id"
FROM relation_label__0 R0
        '
	# TODO rename temporary table to replace output_relation
	
        



