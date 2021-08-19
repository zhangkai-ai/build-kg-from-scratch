#!/usr/bin/env bash
# cmd_extractor  process/grounding/factor/inf_istrue_has_relation/materialize
# {"dependencies_":["process/grounding/variable/has_relation/assign_id"],"input_":["data/supplier_candidate","data/supplier_feature"],"style":"cmd_extractor","cmd":"\n            : ${DEEPDIVE_GROUNDING_DIR:=\"$DEEPDIVE_APP\"/run/model/grounding}\n\n            # materialize factors using user input_query that pulls in assigned ids to involved variables\n            deepdive create table 'dd_factors_inf_istrue_has_relation' as '\n          SELECT R0.id AS \"has_relation.R0.id\" , R2.feature AS \"dd_weight_column_0\" \n          FROM has_relation R0, supplier_candidate R1, supplier_feature R2\n        WHERE R1.p1_id = R0.p1_id  AND R1.p2_id = R0.p2_id  AND R2.p1_id = R0.p1_id  AND R2.p2_id = R0.p2_id '\n\n            # find distinct weights for the factors into a separate table\n            deepdive create table 'dd_weights_inf_istrue_has_relation' as 'SELECT \"dd_weight_column_0\"\n     , false AS \"isfixed\"\n     , 0 AS \"initvalue\"\n     , -1 AS \"id\"\nFROM \"dd_factors_inf_istrue_has_relation\"\n\n\nGROUP BY \"dd_weight_column_0\"'\n        ","name":"process/grounding/factor/inf_istrue_has_relation/materialize"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/grounding/factor/inf_istrue_has_relation/materialize'

            : ${DEEPDIVE_GROUNDING_DIR:="$DEEPDIVE_APP"/run/model/grounding}

            # materialize factors using user input_query that pulls in assigned ids to involved variables
            deepdive create table 'dd_factors_inf_istrue_has_relation' as '
          SELECT R0.id AS "has_relation.R0.id" , R2.feature AS "dd_weight_column_0" 
          FROM has_relation R0, supplier_candidate R1, supplier_feature R2
        WHERE R1.p1_id = R0.p1_id  AND R1.p2_id = R0.p2_id  AND R2.p1_id = R0.p1_id  AND R2.p2_id = R0.p2_id '

            # find distinct weights for the factors into a separate table
            deepdive create table 'dd_weights_inf_istrue_has_relation' as 'SELECT "dd_weight_column_0"
     , false AS "isfixed"
     , 0 AS "initvalue"
     , -1 AS "id"
FROM "dd_factors_inf_istrue_has_relation"


GROUP BY "dd_weight_column_0"'
        



