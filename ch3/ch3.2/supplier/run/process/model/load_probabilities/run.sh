#!/usr/bin/env bash
# cmd_extractor  process/model/load_probabilities
# {"dependencies_":["model/probabilities"],"output_":"data/model/probabilities","style":"cmd_extractor","cmd":"mkdir -p ../../../model && cd ../../../model\n            # load weights to database\n            deepdive create table dd_inference_result_variables \\\n                id:BIGINT \\\n                category:BIGINT \\\n                expectation:'DOUBLE PRECISION' \\\n                #\n            cat probabilities/inference_result.out.text |\n            tr ' ' '\\t' | DEEPDIVE_LOAD_FORMAT=tsv \\\n            deepdive load dd_inference_result_variables /dev/stdin\n\n            # create a view for each app schema variable\n            \n            deepdive create view 'has_relation_label_inference' as '\n                SELECT has_relation.*, mir.category, mir.expectation FROM\n                has_relation, dd_inference_result_variables mir\n                WHERE has_relation.id = mir.id\n                ORDER BY mir.expectation DESC\n                '\n        ","name":"process/model/load_probabilities"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/model/load_probabilities'
mkdir -p ../../../model && cd ../../../model
            # load weights to database
            deepdive create table dd_inference_result_variables \
                id:BIGINT \
                category:BIGINT \
                expectation:'DOUBLE PRECISION' \
                #
            cat probabilities/inference_result.out.text |
            tr ' ' '\t' | DEEPDIVE_LOAD_FORMAT=tsv \
            deepdive load dd_inference_result_variables /dev/stdin

            # create a view for each app schema variable
            
            deepdive create view 'has_relation_label_inference' as '
                SELECT has_relation.*, mir.category, mir.expectation FROM
                has_relation, dd_inference_result_variables mir
                WHERE has_relation.id = mir.id
                ORDER BY mir.expectation DESC
                '
        



