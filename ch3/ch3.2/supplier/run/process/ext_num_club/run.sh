#!/usr/bin/env bash
# cmd_extractor  process/ext_num_club
# {"cmd":"\n\n\tdeepdive create view num_club as 'SELECT R0.doc_id AS column_0, R0.sentence_index AS column_1, COUNT(R0.mention_id) AS column_2\nFROM club_mention R0\n        \n        GROUP BY R0.doc_id, R0.sentence_index'\n\t\n        ","dependencies":["ext_club_mention_by_map_club_mention"],"input_relations":["club_mention"],"output_relation":"num_club","style":"cmd_extractor","dependencies_":["process/ext_club_mention_by_map_club_mention"],"input_":["data/club_mention"],"output_":"data/num_club","name":"process/ext_num_club"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_num_club'


	deepdive create view num_club as 'SELECT R0.doc_id AS column_0, R0.sentence_index AS column_1, COUNT(R0.mention_id) AS column_2
FROM club_mention R0
        
        GROUP BY R0.doc_id, R0.sentence_index'
	
        



