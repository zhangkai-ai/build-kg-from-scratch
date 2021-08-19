#!/usr/bin/env bash
# cmd_extractor  process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id
# {"dependencies_":["process/grounding/weight_id_partition"],"style":"cmd_extractor","cmd":"\n            : ${DEEPDIVE_GROUNDING_DIR:=\"$DEEPDIVE_APP\"/run/model/grounding}\n\n            cd \"$DEEPDIVE_GROUNDING_DIR\"/factor/'inf_imply_has_relation_has_relation'\n            baseId=$(cat weights_id_begin)\n            inc=1\n            \n\n            # assign weight ids according to the partition\n            deepdive db assign_sequential_id 'dd_weights_inf_imply_has_relation_has_relation' id $baseId $inc\n\n            \n        ","name":"process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id'

            : ${DEEPDIVE_GROUNDING_DIR:="$DEEPDIVE_APP"/run/model/grounding}

            cd "$DEEPDIVE_GROUNDING_DIR"/factor/'inf_imply_has_relation_has_relation'
            baseId=$(cat weights_id_begin)
            inc=1
            

            # assign weight ids according to the partition
            deepdive db assign_sequential_id 'dd_weights_inf_imply_has_relation_has_relation' id $baseId $inc

            
        



