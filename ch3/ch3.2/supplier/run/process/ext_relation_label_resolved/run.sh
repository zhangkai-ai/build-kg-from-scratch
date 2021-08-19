#!/usr/bin/env bash
# cmd_extractor  process/ext_relation_label_resolved
# {"cmd":"\n\n\tdeepdive create view relation_label_resolved as 'SELECT R0.p1_id AS column_0, R0.p2_id AS column_1, SUM(R0.label) AS column_2\nFROM relation_label R0\n        \n        GROUP BY R0.p1_id, R0.p2_id'\n\t\n        ","dependencies":["ext_relation_label"],"input_relations":["relation_label"],"output_relation":"relation_label_resolved","style":"cmd_extractor","dependencies_":["process/ext_relation_label"],"input_":["data/relation_label"],"output_":"data/relation_label_resolved","name":"process/ext_relation_label_resolved"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_relation_label_resolved'


	deepdive create view relation_label_resolved as 'SELECT R0.p1_id AS column_0, R0.p2_id AS column_1, SUM(R0.label) AS column_2
FROM relation_label R0
        
        GROUP BY R0.p1_id, R0.p2_id'
	
        



