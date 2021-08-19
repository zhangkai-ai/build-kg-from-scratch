#!/usr/bin/env bash
# cmd_extractor  process/ext_has_relation
# {"cmd":"\n\n\t# TODO use temporary table\n\tdeepdive create table \"has_relation\"\n\tdeepdive sql 'INSERT INTO has_relation SELECT DISTINCT R0.column_0, R0.column_1, 0 AS id, \nCASE WHEN R0.column_2 > 0 THEN true\n     WHEN R0.column_2 < 0 THEN false\n     ELSE NULL\nEND AS label\n          FROM relation_label_resolved R0\n        \n          '\n\t# TODO rename temporary table to replace output_relation\n\t\n        ","dependencies":["ext_relation_label_resolved"],"input_relations":["relation_label_resolved"],"output_relation":"has_relation","style":"cmd_extractor","dependencies_":["process/ext_relation_label_resolved"],"input_":["data/relation_label_resolved"],"output_":"data/has_relation","name":"process/ext_has_relation"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_has_relation'


	# TODO use temporary table
	deepdive create table "has_relation"
	deepdive sql 'INSERT INTO has_relation SELECT DISTINCT R0.column_0, R0.column_1, 0 AS id, 
CASE WHEN R0.column_2 > 0 THEN true
     WHEN R0.column_2 < 0 THEN false
     ELSE NULL
END AS label
          FROM relation_label_resolved R0
        
          '
	# TODO rename temporary table to replace output_relation
	
        



