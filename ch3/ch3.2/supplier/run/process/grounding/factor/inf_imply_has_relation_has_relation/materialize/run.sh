#!/usr/bin/env bash
# cmd_extractor  process/grounding/factor/inf_imply_has_relation_has_relation/materialize
# {"dependencies_":["process/grounding/variable/has_relation/assign_id"],"input_":["data/supplier_candidate"],"style":"cmd_extractor","cmd":"\n            : ${DEEPDIVE_GROUNDING_DIR:=\"$DEEPDIVE_APP\"/run/model/grounding}\n\n            # materialize factors using user input_query that pulls in assigned ids to involved variables\n            deepdive create table 'dd_factors_inf_imply_has_relation_has_relation' as '\n          SELECT R0.id AS \"has_relation.R0.id\" , R1.id AS \"has_relation.R1.id\" \n          FROM has_relation R0, has_relation R1, supplier_candidate R2\n        WHERE R1.p1_id = R0.p2_id  AND R1.p2_id = R0.p1_id  AND R2.p1_id = R0.p1_id  AND R2.p2_id = R0.p2_id '\n\n            # find distinct weights for the factors into a separate table\n            deepdive create table 'dd_weights_inf_imply_has_relation_has_relation' as 'SELECT true AS \"isfixed\"\n     , 3 AS \"initvalue\"\n     , -1 AS \"id\"'\n        ","name":"process/grounding/factor/inf_imply_has_relation_has_relation/materialize"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/grounding/factor/inf_imply_has_relation_has_relation/materialize'

            : ${DEEPDIVE_GROUNDING_DIR:="$DEEPDIVE_APP"/run/model/grounding}

            # materialize factors using user input_query that pulls in assigned ids to involved variables
            deepdive create table 'dd_factors_inf_imply_has_relation_has_relation' as '
          SELECT R0.id AS "has_relation.R0.id" , R1.id AS "has_relation.R1.id" 
          FROM has_relation R0, has_relation R1, supplier_candidate R2
        WHERE R1.p1_id = R0.p2_id  AND R1.p2_id = R0.p1_id  AND R2.p1_id = R0.p1_id  AND R2.p2_id = R0.p2_id '

            # find distinct weights for the factors into a separate table
            deepdive create table 'dd_weights_inf_imply_has_relation_has_relation' as 'SELECT true AS "isfixed"
     , 3 AS "initvalue"
     , -1 AS "id"'
        



