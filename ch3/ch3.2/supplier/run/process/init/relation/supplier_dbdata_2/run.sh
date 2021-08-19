#!/usr/bin/env bash
# cmd_extractor  process/init/relation/supplier_dbdata_2
# {"style":"cmd_extractor","cmd":"deepdive create table 'supplier_dbdata_2' && deepdive load 'supplier_dbdata_2'","dependencies_":["process/init/app"],"output_relation":"supplier_dbdata_2","output_":"data/supplier_dbdata_2","name":"process/init/relation/supplier_dbdata_2"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/init/relation/supplier_dbdata_2'
deepdive create table 'supplier_dbdata_2' && deepdive load 'supplier_dbdata_2'



