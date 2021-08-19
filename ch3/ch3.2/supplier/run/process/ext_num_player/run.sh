#!/usr/bin/env bash
# cmd_extractor  process/ext_num_player
# {"cmd":"\n\n\tdeepdive create view num_player as 'SELECT R0.doc_id AS column_0, R0.sentence_index AS column_1, COUNT(R0.mention_id) AS column_2\nFROM player_mention R0\n        \n        GROUP BY R0.doc_id, R0.sentence_index'\n\t\n        ","dependencies":["ext_player_mention_by_map_player_mention"],"input_relations":["player_mention"],"output_relation":"num_player","style":"cmd_extractor","dependencies_":["process/ext_player_mention_by_map_player_mention"],"input_":["data/player_mention"],"output_":"data/num_player","name":"process/ext_num_player"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_num_player'


	deepdive create view num_player as 'SELECT R0.doc_id AS column_0, R0.sentence_index AS column_1, COUNT(R0.mention_id) AS column_2
FROM player_mention R0
        
        GROUP BY R0.doc_id, R0.sentence_index'
	
        



