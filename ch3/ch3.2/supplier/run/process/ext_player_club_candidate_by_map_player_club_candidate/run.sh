#!/usr/bin/env bash
# tsv_extractor  process/ext_player_club_candidate_by_map_player_club_candidate
# {"dependencies":["ext_num_player","ext_num_club","ext_player_mention_by_map_player_mention","ext_club_mention_by_map_club_mention"],"input":" SELECT R2.mention_id AS \"player_mention.R2.mention_id\", R2.mention_text AS \"player_mention.R2.mention_text\", R3.mention_id AS \"club_mention.R3.mention_id\", R3.mention_text AS \"club_mention.R3.mention_text\"\nFROM num_player R0, num_club R1, player_mention R2, club_mention R3\n        WHERE R1.column_0 = R0.column_0  AND R1.column_1 = R0.column_1  AND R1.column_2 = R0.column_2  AND R2.doc_id = R0.column_0  AND R2.sentence_index = R0.column_1  AND R3.doc_id = R0.column_0  AND R3.sentence_index = R0.column_1  AND R0.column_2 < 5 AND R2.mention_text != R3.mention_text AND R2.begin_index != R3.begin_index\n          ","input_batch_size":"100000","input_relations":["num_player","num_club","player_mention","club_mention"],"output_relation":"player_club_candidate","parallelism":"1","style":"tsv_extractor","udf":"\"$DEEPDIVE_APP\"/udf/map_player_club_candidate.py","dependencies_":["process/ext_num_player","process/ext_num_club","process/ext_player_mention_by_map_player_mention","process/ext_club_mention_by_map_club_mention"],"input_":["data/num_player","data/num_club","data/player_mention","data/club_mention"],"output_":"data/player_club_candidate","name":"process/ext_player_club_candidate_by_map_player_club_candidate"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/ext_player_club_candidate_by_map_player_club_candidate'
export DEEPDIVE_LOAD_FORMAT=tsv

deepdive compute execute \
    input_sql=' SELECT R2.mention_id AS "player_mention.R2.mention_id", R2.mention_text AS "player_mention.R2.mention_text", R3.mention_id AS "club_mention.R3.mention_id", R3.mention_text AS "club_mention.R3.mention_text"
FROM num_player R0, num_club R1, player_mention R2, club_mention R3
        WHERE R1.column_0 = R0.column_0  AND R1.column_1 = R0.column_1  AND R1.column_2 = R0.column_2  AND R2.doc_id = R0.column_0  AND R2.sentence_index = R0.column_1  AND R3.doc_id = R0.column_0  AND R3.sentence_index = R0.column_1  AND R0.column_2 < 5 AND R2.mention_text != R3.mention_text AND R2.begin_index != R3.begin_index
          ' \
    command='"$DEEPDIVE_APP"/udf/map_player_club_candidate.py' \
    output_relation='player_club_candidate' \
    #



