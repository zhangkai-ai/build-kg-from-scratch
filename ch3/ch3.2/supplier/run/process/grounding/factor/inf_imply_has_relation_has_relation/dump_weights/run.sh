#!/usr/bin/env bash
# cmd_extractor  process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights
# {"dependencies_":["process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id"],"style":"cmd_extractor","cmd":"\n            : ${DEEPDIVE_GROUNDING_DIR:=\"$DEEPDIVE_APP\"/run/model/grounding}\n            facPath=\"$DEEPDIVE_GROUNDING_DIR\"/factor/'inf_imply_has_relation_has_relation'\n            mkdir -p \"$facPath\"\n            cd \"$facPath\"\n            find . \\( -name  'weights.part-*.bin.bz2' \\\n                   \\) -exec rm -rf {} +\n            export DEEPDIVE_LOAD_FORMAT=tsv\n            export DEEPDIVE_UNLOAD_MATERIALIZED=false\n\n            # flag that signals whether to reuse weights or not\n            reuseFlag=\"$DEEPDIVE_GROUNDING_DIR\"/factor/weights.reuse\n\n            # dump the weights (except the description column), converting into binary format for the inference engine\n            deepdive compute execute \\\n                input_sql=\"$(if [[ -e \"$reuseFlag\" ]]; then\n                    echo 'SELECT \"w\".\"id\"\n     , CASE WHEN w.isfixed THEN 1 ELSE 0 END\n     , COALESCE(reuse.weight, w.initvalue, 0)\nFROM \"dd_weights_inf_imply_has_relation_has_relation\" \"w\"\nLEFT OUTER JOIN \"dd_graph_weights_reuse\" \"reuse\" ON \"reuse\".\"description\" = '\\''inf_imply_has_relation_has_relation-'\\'''\n                else\n                    echo 'SELECT \"id\"\n     , CASE WHEN isfixed THEN 1 ELSE 0 END\n     , COALESCE(initvalue, 0)\nFROM \"dd_weights_inf_imply_has_relation_has_relation\"'\n                fi)\" \\\n                command='\n                    format_converter weight /dev/stdin >(pbzip2 >weights.part-${DEEPDIVE_CURRENT_PROCESS_INDEX}.bin.bz2)\n                ' \\\n                output_relation=\n        ","name":"process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights'

            : ${DEEPDIVE_GROUNDING_DIR:="$DEEPDIVE_APP"/run/model/grounding}
            facPath="$DEEPDIVE_GROUNDING_DIR"/factor/'inf_imply_has_relation_has_relation'
            mkdir -p "$facPath"
            cd "$facPath"
            find . \( -name  'weights.part-*.bin.bz2' \
                   \) -exec rm -rf {} +
            export DEEPDIVE_LOAD_FORMAT=tsv
            export DEEPDIVE_UNLOAD_MATERIALIZED=false

            # flag that signals whether to reuse weights or not
            reuseFlag="$DEEPDIVE_GROUNDING_DIR"/factor/weights.reuse

            # dump the weights (except the description column), converting into binary format for the inference engine
            deepdive compute execute \
                input_sql="$(if [[ -e "$reuseFlag" ]]; then
                    echo 'SELECT "w"."id"
     , CASE WHEN w.isfixed THEN 1 ELSE 0 END
     , COALESCE(reuse.weight, w.initvalue, 0)
FROM "dd_weights_inf_imply_has_relation_has_relation" "w"
LEFT OUTER JOIN "dd_graph_weights_reuse" "reuse" ON "reuse"."description" = '\''inf_imply_has_relation_has_relation-'\'''
                else
                    echo 'SELECT "id"
     , CASE WHEN isfixed THEN 1 ELSE 0 END
     , COALESCE(initvalue, 0)
FROM "dd_weights_inf_imply_has_relation_has_relation"'
                fi)" \
                command='
                    format_converter weight /dev/stdin >(pbzip2 >weights.part-${DEEPDIVE_CURRENT_PROCESS_INDEX}.bin.bz2)
                ' \
                output_relation=
        



