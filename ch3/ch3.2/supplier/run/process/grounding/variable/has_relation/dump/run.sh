#!/usr/bin/env bash
# cmd_extractor  process/grounding/variable/has_relation/dump
# {"dependencies_":["process/grounding/variable_holdout"],"style":"cmd_extractor","cmd":"\n        : ${DEEPDIVE_GROUNDING_DIR:=\"$DEEPDIVE_APP\"/run/model/grounding}\n        table='has_relation'\n\n        varPath=\"$DEEPDIVE_GROUNDING_DIR\"/variable/'has_relation'\n        mkdir -p \"$varPath\"\n        cd \"$varPath\"\n        find . -name 'variables.part-*.bin.bz2' -exec rm -rf {} +\n        export DEEPDIVE_LOAD_FORMAT=tsv\n        export DEEPDIVE_UNLOAD_MATERIALIZED=false\n\n        # dump the variables, joining the holdout query to determine the type of each variable\n        deepdive compute execute \\\n            input_sql='SELECT \"id\"\n     , \"variable_role\"\n     , CASE WHEN variable_role = 0 THEN 0\n                          ELSE (CASE WHEN label THEN 1 ELSE 0 END) + 0.0\n                      END AS \"init_value\"\n     , \"variable_type\"\n     , \"cardinality\"\nFROM (SELECT \"id\" AS \"id\"\n     , CASE WHEN               observation.variable_id IS NOT NULL\n                                     AND variables.\"label\" IS NOT NULL THEN 2\n                                    WHEN               holdout.variable_id IS NOT NULL THEN 0\n                                    WHEN variables.\"label\" IS NOT NULL THEN 1\n                                                                                       ELSE 0\n                                END AS \"variable_role\"\n     , \"variables\".\"label\" AS \"label\"\n     , 0 AS \"variable_type\"\n     , 2 AS \"cardinality\"\nFROM \"has_relation\" \"variables\"\nLEFT OUTER JOIN \"dd_graph_variables_holdout\" \"holdout\" ON \"variables\".\"id\" = \"holdout\".\"variable_id\" LEFT OUTER JOIN \"dd_graph_variables_observation\" \"observation\" ON \"variables\".\"id\" = \"observation\".\"variable_id\") \"variables\"' \\\n            command='\n                format_converter variable /dev/stdin >(pbzip2 >variables.part-${DEEPDIVE_CURRENT_PROCESS_INDEX}.bin.bz2)\n            ' \\\n            output_relation=\n        ","name":"process/grounding/variable/has_relation/dump"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/grounding/variable/has_relation/dump'

        : ${DEEPDIVE_GROUNDING_DIR:="$DEEPDIVE_APP"/run/model/grounding}
        table='has_relation'

        varPath="$DEEPDIVE_GROUNDING_DIR"/variable/'has_relation'
        mkdir -p "$varPath"
        cd "$varPath"
        find . -name 'variables.part-*.bin.bz2' -exec rm -rf {} +
        export DEEPDIVE_LOAD_FORMAT=tsv
        export DEEPDIVE_UNLOAD_MATERIALIZED=false

        # dump the variables, joining the holdout query to determine the type of each variable
        deepdive compute execute \
            input_sql='SELECT "id"
     , "variable_role"
     , CASE WHEN variable_role = 0 THEN 0
                          ELSE (CASE WHEN label THEN 1 ELSE 0 END) + 0.0
                      END AS "init_value"
     , "variable_type"
     , "cardinality"
FROM (SELECT "id" AS "id"
     , CASE WHEN               observation.variable_id IS NOT NULL
                                     AND variables."label" IS NOT NULL THEN 2
                                    WHEN               holdout.variable_id IS NOT NULL THEN 0
                                    WHEN variables."label" IS NOT NULL THEN 1
                                                                                       ELSE 0
                                END AS "variable_role"
     , "variables"."label" AS "label"
     , 0 AS "variable_type"
     , 2 AS "cardinality"
FROM "has_relation" "variables"
LEFT OUTER JOIN "dd_graph_variables_holdout" "holdout" ON "variables"."id" = "holdout"."variable_id" LEFT OUTER JOIN "dd_graph_variables_observation" "observation" ON "variables"."id" = "observation"."variable_id") "variables"' \
            command='
                format_converter variable /dev/stdin >(pbzip2 >variables.part-${DEEPDIVE_CURRENT_PROCESS_INDEX}.bin.bz2)
            ' \
            output_relation=
        



