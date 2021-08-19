#!/usr/bin/env bash
# cmd_extractor  process/init/relation/information
# {"style":"cmd_extractor","cmd":"deepdive create table 'information' && deepdive load 'information'","dependencies_":["process/init/app"],"output_relation":"information","output_":"data/information","name":"process/init/relation/information"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/init/relation/information'
deepdive create table 'information' && deepdive load 'information'



