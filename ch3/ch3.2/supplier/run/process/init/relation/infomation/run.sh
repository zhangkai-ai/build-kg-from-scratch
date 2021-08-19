#!/usr/bin/env bash
# cmd_extractor  process/init/relation/infomation
# {"style":"cmd_extractor","cmd":"deepdive create table 'infomation' && deepdive load 'infomation'","dependencies_":["process/init/app"],"output_relation":"infomation","output_":"data/infomation","name":"process/init/relation/infomation"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/init/relation/infomation'
deepdive create table 'infomation' && deepdive load 'infomation'



