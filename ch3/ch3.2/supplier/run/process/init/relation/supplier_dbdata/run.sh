#!/usr/bin/env bash
# cmd_extractor  process/init/relation/supplier_dbdata
# {"style":"cmd_extractor","cmd":"deepdive create table 'supplier_dbdata' && deepdive load 'supplier_dbdata'","dependencies_":["process/init/app"],"output_relation":"supplier_dbdata","output_":"data/supplier_dbdata","name":"process/init/relation/supplier_dbdata"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/init/relation/supplier_dbdata'
deepdive create table 'supplier_dbdata' && deepdive load 'supplier_dbdata'



