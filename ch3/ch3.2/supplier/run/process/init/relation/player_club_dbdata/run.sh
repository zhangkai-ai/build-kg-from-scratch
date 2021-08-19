#!/usr/bin/env bash
# cmd_extractor  process/init/relation/player_club_dbdata
# {"style":"cmd_extractor","cmd":"deepdive create table 'player_club_dbdata' && deepdive load 'player_club_dbdata'","dependencies_":["process/init/app"],"output_relation":"player_club_dbdata","output_":"data/player_club_dbdata","name":"process/init/relation/player_club_dbdata"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/init/relation/player_club_dbdata'
deepdive create table 'player_club_dbdata' && deepdive load 'player_club_dbdata'



