#!/usr/bin/env bash
# cmd_extractor  process/model/load_weights
# {"dependencies_":["model/weights"],"output_":"data/model/weights","style":"cmd_extractor","cmd":"mkdir -p ../../../model && cd ../../../model\n            # load weights to database\n            deepdive create table dd_inference_result_weights \\\n                id:BIGINT:'PRIMARY KEY' \\\n                weight:'DOUBLE PRECISION' \\\n                #\n            cat weights/inference_result.out.weights.text |\n            tr ' ' '\\t' | DEEPDIVE_LOAD_FORMAT=tsv \\\n            deepdive load dd_inference_result_weights /dev/stdin\n\n            # create views\n            deepdive create view dd_inference_result_weights_mapping as '\n                SELECT dd_graph_weights.*, dd_inference_result_weights.weight FROM\n                dd_graph_weights JOIN dd_inference_result_weights ON dd_graph_weights.id = dd_inference_result_weights.id\n                ORDER BY abs(weight) DESC\n            '\n\n            deepdive create view dd_inference_result_variables_mapped_weights as '\n                SELECT * FROM dd_inference_result_weights_mapping\n                ORDER BY abs(weight) DESC\n            '\n        ","name":"process/model/load_weights"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/model/load_weights'
mkdir -p ../../../model && cd ../../../model
            # load weights to database
            deepdive create table dd_inference_result_weights \
                id:BIGINT:'PRIMARY KEY' \
                weight:'DOUBLE PRECISION' \
                #
            cat weights/inference_result.out.weights.text |
            tr ' ' '\t' | DEEPDIVE_LOAD_FORMAT=tsv \
            deepdive load dd_inference_result_weights /dev/stdin

            # create views
            deepdive create view dd_inference_result_weights_mapping as '
                SELECT dd_graph_weights.*, dd_inference_result_weights.weight FROM
                dd_graph_weights JOIN dd_inference_result_weights ON dd_graph_weights.id = dd_inference_result_weights.id
                ORDER BY abs(weight) DESC
            '

            deepdive create view dd_inference_result_variables_mapped_weights as '
                SELECT * FROM dd_inference_result_weights_mapping
                ORDER BY abs(weight) DESC
            '
        



