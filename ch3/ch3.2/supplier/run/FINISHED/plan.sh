# on userMACdeMacBook-Pro.local: deepdive do probabilities
# run/20190617/171721.401729000/plan.sh
# execution plan for data/model/probabilities

: ## process/init/app ##########################################################
: # Done: 2019-05-28T15:19:22+0800 (20d 1h 57m 59s ago)
: process/init/app/run.sh
: mark_done process/init/app
: ##############################################################################

: ## process/init/relation/information #########################################
: # Done: 2019-06-17T17:00:11+0800 (17m 10s ago)
: process/init/relation/information/run.sh
: mark_done process/init/relation/information
: ##############################################################################

: ## data/information ##########################################################
: # Done: 2019-06-17T17:00:11+0800 (17m 10s ago)
: # no-op
: mark_done data/information
: ##############################################################################

: ## process/ext_sentences_by_nlp_markup #######################################
: # Done: 2019-06-17T17:06:11+0800 (11m 10s ago)
: process/ext_sentences_by_nlp_markup/run.sh
: mark_done process/ext_sentences_by_nlp_markup
: ##############################################################################

: ## data/sentences ############################################################
: # Done: 2019-06-17T17:06:11+0800 (11m 10s ago)
: # no-op
: mark_done data/sentences
: ##############################################################################

: ## process/ext_company_mention_by_map_company_mention ########################
: # Done: 2019-06-17T17:08:33+0800 (8m 48s ago)
: process/ext_company_mention_by_map_company_mention/run.sh
: mark_done process/ext_company_mention_by_map_company_mention
: ##############################################################################

: ## data/company_mention ######################################################
: # Done: 2019-06-17T17:08:33+0800 (8m 48s ago)
: # no-op
: mark_done data/company_mention
: ##############################################################################

: ## process/ext_supplier_candidate_by_map_supplier_candidate ##################
: # Done: 2019-06-17T17:09:26+0800 (7m 55s ago)
: process/ext_supplier_candidate_by_map_supplier_candidate/run.sh
: mark_done process/ext_supplier_candidate_by_map_supplier_candidate
: ##############################################################################

: ## data/supplier_candidate ###################################################
: # Done: 2019-06-17T17:09:26+0800 (7m 55s ago)
: # no-op
: mark_done data/supplier_candidate
: ##############################################################################

: ## process/ext_relation_label__0_by_supervise ################################
: # Done: 2019-06-17T17:15:44+0800 (1m 37s ago)
: process/ext_relation_label__0_by_supervise/run.sh
: mark_done process/ext_relation_label__0_by_supervise
: ##############################################################################

: ## data/relation_label__0 ####################################################
: # Done: 2019-06-17T17:15:44+0800 (1m 37s ago)
: # no-op
: mark_done data/relation_label__0
: ##############################################################################

: ## process/init/relation/supplier_dbdata #####################################
: # Done: 2019-06-17T09:15:26+0800 (8h 1m 56s ago)
: process/init/relation/supplier_dbdata/run.sh
: mark_done process/init/relation/supplier_dbdata
: ##############################################################################

: ## data/supplier_dbdata ######################################################
: # Done: 2019-06-17T09:15:26+0800 (8h 1m 56s ago)
: # no-op
: mark_done data/supplier_dbdata
: ##############################################################################

: ## process/init/relation/supplier_dbdata_2 ###################################
: # Done: 2019-06-17T16:03:17+0800 (1h 14m 5s ago)
: process/init/relation/supplier_dbdata_2/run.sh
: mark_done process/init/relation/supplier_dbdata_2
: ##############################################################################

: ## data/supplier_dbdata_2 ####################################################
: # Done: 2019-06-17T16:03:17+0800 (1h 14m 5s ago)
: # no-op
: mark_done data/supplier_dbdata_2
: ##############################################################################

: ## process/ext_relation_label ################################################
: # Done: 2019-06-17T17:15:44+0800 (1m 38s ago)
: process/ext_relation_label/run.sh
: mark_done process/ext_relation_label
: ##############################################################################

: ## data/relation_label #######################################################
: # Done: 2019-06-17T17:15:44+0800 (1m 38s ago)
: # no-op
: mark_done data/relation_label
: ##############################################################################

: ## process/ext_relation_label_resolved #######################################
: # Done: 2019-06-17T17:15:44+0800 (1m 38s ago)
: process/ext_relation_label_resolved/run.sh
: mark_done process/ext_relation_label_resolved
: ##############################################################################

: ## data/relation_label_resolved ##############################################
: # Done: 2019-06-17T17:15:44+0800 (1m 38s ago)
: # no-op
: mark_done data/relation_label_resolved
: ##############################################################################

: ## process/ext_has_relation ##################################################
: # Done: 2019-06-17T17:16:53+0800 (29s ago)
: process/ext_has_relation/run.sh
: mark_done process/ext_has_relation
: ##############################################################################

: ## data/has_relation #########################################################
: # Done: 2019-06-17T17:16:53+0800 (29s ago)
: # no-op
: mark_done data/has_relation
: ##############################################################################

## process/grounding/variable_id_partition ###################################
: # Done: 2019-06-17T16:13:14+0800 (1h 4m 8s ago)
# Done: 2019-06-17T16:13:14+0800 (1h 4m 7s ago)
process/grounding/variable_id_partition/run.sh
mark_done process/grounding/variable_id_partition
##############################################################################

## process/grounding/variable/has_relation/assign_id #########################
: # Done: 2019-06-17T16:13:14+0800 (1h 4m 8s ago)
# Done: 2019-06-17T16:13:14+0800 (1h 4m 7s ago)
process/grounding/variable/has_relation/assign_id/run.sh
mark_done process/grounding/variable/has_relation/assign_id
##############################################################################

## process/grounding/factor/inf_imply_has_relation_has_relation/materialize ##
: # Done: 2019-06-17T16:13:15+0800 (1h 4m 7s ago)
# Done: 2019-06-17T16:13:15+0800 (1h 4m 6s ago)
process/grounding/factor/inf_imply_has_relation_has_relation/materialize/run.sh
mark_done process/grounding/factor/inf_imply_has_relation_has_relation/materialize
##############################################################################

: ## process/ext_supplier_feature_by_extract_features ##########################
: # Done: 2019-06-17T17:14:48+0800 (2m 34s ago)
: process/ext_supplier_feature_by_extract_features/run.sh
: mark_done process/ext_supplier_feature_by_extract_features
: ##############################################################################

: ## data/supplier_feature #####################################################
: # Done: 2019-06-17T17:14:48+0800 (2m 34s ago)
: # no-op
: mark_done data/supplier_feature
: ##############################################################################

## process/grounding/factor/inf_istrue_has_relation/materialize ##############
: # Done: 2019-06-17T16:13:15+0800 (1h 4m 7s ago)
# Done: 2019-06-17T16:13:15+0800 (1h 4m 6s ago)
process/grounding/factor/inf_istrue_has_relation/materialize/run.sh
mark_done process/grounding/factor/inf_istrue_has_relation/materialize
##############################################################################

## process/grounding/weight_id_partition #####################################
: # Done: 2019-06-17T16:13:15+0800 (1h 4m 7s ago)
# Done: 2019-06-17T16:13:15+0800 (1h 4m 6s ago)
process/grounding/weight_id_partition/run.sh
mark_done process/grounding/weight_id_partition
##############################################################################

## process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id null
: # Done: 2019-06-17T16:13:15+0800 (1h 4m 7s ago)
# Done: 2019-06-17T16:13:15+0800 (1h 4m 6s ago)
process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id/run.sh
mark_done process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id
##############################################################################

## process/grounding/factor/inf_imply_has_relation_has_relation/dump #########
: # Done: 2019-06-17T16:13:17+0800 (1h 4m 5s ago)
# Done: 2019-06-17T16:13:17+0800 (1h 4m 4s ago)
process/grounding/factor/inf_imply_has_relation_has_relation/dump/run.sh
mark_done process/grounding/factor/inf_imply_has_relation_has_relation/dump
##############################################################################

## process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights #
: # Done: 2019-06-17T16:13:17+0800 (1h 4m 5s ago)
# Done: 2019-06-17T16:13:17+0800 (1h 4m 4s ago)
process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights/run.sh
mark_done process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights
##############################################################################

## process/grounding/factor/inf_istrue_has_relation/assign_weight_id #########
: # Done: 2019-06-17T16:13:17+0800 (1h 4m 5s ago)
# Done: 2019-06-17T16:13:17+0800 (1h 4m 4s ago)
process/grounding/factor/inf_istrue_has_relation/assign_weight_id/run.sh
mark_done process/grounding/factor/inf_istrue_has_relation/assign_weight_id
##############################################################################

## process/grounding/factor/inf_istrue_has_relation/dump #####################
: # Done: 2019-06-17T16:13:18+0800 (1h 4m 4s ago)
# Done: 2019-06-17T16:13:18+0800 (1h 4m 3s ago)
process/grounding/factor/inf_istrue_has_relation/dump/run.sh
mark_done process/grounding/factor/inf_istrue_has_relation/dump
##############################################################################

## process/grounding/factor/inf_istrue_has_relation/dump_weights #############
: # Done: 2019-06-17T16:13:18+0800 (1h 4m 4s ago)
# Done: 2019-06-17T16:13:18+0800 (1h 4m 3s ago)
process/grounding/factor/inf_istrue_has_relation/dump_weights/run.sh
mark_done process/grounding/factor/inf_istrue_has_relation/dump_weights
##############################################################################

## process/grounding/global_weight_table #####################################
: # Done: 2019-06-17T16:13:18+0800 (1h 4m 4s ago)
# Done: 2019-06-17T16:13:18+0800 (1h 4m 3s ago)
process/grounding/global_weight_table/run.sh
mark_done process/grounding/global_weight_table
##############################################################################

## process/grounding/variable_holdout ########################################
: # Done: 2019-06-17T16:13:19+0800 (1h 4m 3s ago)
# Done: 2019-06-17T16:13:19+0800 (1h 4m 2s ago)
process/grounding/variable_holdout/run.sh
mark_done process/grounding/variable_holdout
##############################################################################

## process/grounding/variable/has_relation/dump ##############################
: # Done: 2019-06-17T16:13:19+0800 (1h 4m 3s ago)
# Done: 2019-06-17T16:13:19+0800 (1h 4m 2s ago)
process/grounding/variable/has_relation/dump/run.sh
mark_done process/grounding/variable/has_relation/dump
##############################################################################

## process/grounding/combine_factorgraph #####################################
: # Done: 2019-06-17T16:13:19+0800 (1h 4m 3s ago)
# Done: 2019-06-17T16:13:19+0800 (1h 4m 2s ago)
process/grounding/combine_factorgraph/run.sh
mark_done process/grounding/combine_factorgraph
##############################################################################

## model/factorgraph #########################################################
: # Done: 2019-06-17T16:13:19+0800 (1h 4m 3s ago)
# Done: 2019-06-17T16:13:19+0800 (1h 4m 2s ago)
mark_done model/factorgraph
##############################################################################

## process/model/learning ####################################################
: # Done: 2019-06-17T16:13:20+0800 (1h 4m 2s ago)
# Done: 2019-06-17T16:13:20+0800 (1h 4m 1s ago)
process/model/learning/run.sh
mark_done process/model/learning
##############################################################################

## model/weights #############################################################
: # Done: 2019-06-17T16:13:20+0800 (1h 4m 2s ago)
# Done: 2019-06-17T16:13:20+0800 (1h 4m 1s ago)
mark_done model/weights
##############################################################################

## process/model/inference ###################################################
: # Done: 2019-06-17T16:13:20+0800 (1h 4m 2s ago)
# Done: 2019-06-17T16:13:20+0800 (1h 4m 1s ago)
process/model/inference/run.sh
mark_done process/model/inference
##############################################################################

## model/probabilities #######################################################
: # Done: 2019-06-17T16:13:20+0800 (1h 4m 2s ago)
# Done: 2019-06-17T16:13:20+0800 (1h 4m 1s ago)
mark_done model/probabilities
##############################################################################

## process/model/load_probabilities ##########################################
: # Done: 2019-06-17T16:13:20+0800 (1h 4m 2s ago)
# Done: 2019-06-17T16:13:20+0800 (1h 4m 1s ago)
process/model/load_probabilities/run.sh
mark_done process/model/load_probabilities
##############################################################################

## data/model/probabilities ##################################################
: # Done: 2019-06-17T16:13:20+0800 (1h 4m 2s ago)
# Done: 2019-06-17T16:13:20+0800 (1h 4m 1s ago)
# no-op
mark_done data/model/probabilities
##############################################################################

