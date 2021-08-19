
# default commands
define CMD_data
# no-op
endef
define CMD_pipeline
# no-op
endef
define CMD_process
# no-op
endef
define CMD_factor
# no-op
endef
define TOUCH
endef
define RESET
rm -f
endef

.DEFAULT: help
help:
	@echo make list
	@echo make list-targets
	@echo make all
	@echo make reset
list:
	@printf "%s\n" 'data/company_mention' 'data/has_relation' 'data/information' 'data/model/probabilities' 'data/model/weights' 'data/relation_label' 'data/relation_label__0' 'data/relation_label_resolved' 'data/sentences' 'data/supplier_candidate' 'data/supplier_dbdata' 'data/supplier_dbdata_2' 'data/supplier_feature' 'model/calibration-plots' 'model/factorgraph' 'model/probabilities' 'model/weights' 'process/ext_company_mention_by_map_company_mention' 'process/ext_has_relation' 'process/ext_relation_label' 'process/ext_relation_label__0_by_supervise' 'process/ext_relation_label_resolved' 'process/ext_sentences_by_nlp_markup' 'process/ext_supplier_candidate_by_map_supplier_candidate' 'process/ext_supplier_feature_by_extract_features' 'process/grounding/combine_factorgraph' 'process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id' 'process/grounding/factor/inf_imply_has_relation_has_relation/dump' 'process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights' 'process/grounding/factor/inf_imply_has_relation_has_relation/materialize' 'process/grounding/factor/inf_istrue_has_relation/assign_weight_id' 'process/grounding/factor/inf_istrue_has_relation/dump' 'process/grounding/factor/inf_istrue_has_relation/dump_weights' 'process/grounding/factor/inf_istrue_has_relation/materialize' 'process/grounding/global_weight_table' 'process/grounding/variable/has_relation/assign_id' 'process/grounding/variable/has_relation/dump' 'process/grounding/variable_holdout' 'process/grounding/variable_id_partition' 'process/grounding/weight_id_partition' 'process/init/app' 'process/init/relation/information' 'process/init/relation/supplier_dbdata' 'process/init/relation/supplier_dbdata_2' 'process/model/calibration' 'process/model/inference' 'process/model/learning' 'process/model/load_probabilities' 'process/model/load_weights'
list-targets:
	@printf "make %s\n" 'data/company_mention.done' 'data/has_relation.done' 'data/information.done' 'data/model/probabilities.done' 'data/model/weights.done' 'data/relation_label.done' 'data/relation_label__0.done' 'data/relation_label_resolved.done' 'data/sentences.done' 'data/supplier_candidate.done' 'data/supplier_dbdata.done' 'data/supplier_dbdata_2.done' 'data/supplier_feature.done' 'model/calibration-plots.done' 'model/factorgraph.done' 'model/probabilities.done' 'model/weights.done' 'process/ext_company_mention_by_map_company_mention.done' 'process/ext_has_relation.done' 'process/ext_relation_label.done' 'process/ext_relation_label__0_by_supervise.done' 'process/ext_relation_label_resolved.done' 'process/ext_sentences_by_nlp_markup.done' 'process/ext_supplier_candidate_by_map_supplier_candidate.done' 'process/ext_supplier_feature_by_extract_features.done' 'process/grounding/combine_factorgraph.done' 'process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.done' 'process/grounding/factor/inf_imply_has_relation_has_relation/dump.done' 'process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.done' 'process/grounding/factor/inf_imply_has_relation_has_relation/materialize.done' 'process/grounding/factor/inf_istrue_has_relation/assign_weight_id.done' 'process/grounding/factor/inf_istrue_has_relation/dump.done' 'process/grounding/factor/inf_istrue_has_relation/dump_weights.done' 'process/grounding/factor/inf_istrue_has_relation/materialize.done' 'process/grounding/global_weight_table.done' 'process/grounding/variable/has_relation/assign_id.done' 'process/grounding/variable/has_relation/dump.done' 'process/grounding/variable_holdout.done' 'process/grounding/variable_id_partition.done' 'process/grounding/weight_id_partition.done' 'process/init/app.done' 'process/init/relation/information.done' 'process/init/relation/supplier_dbdata.done' 'process/init/relation/supplier_dbdata_2.done' 'process/model/calibration.done' 'process/model/inference.done' 'process/model/learning.done' 'process/model/load_probabilities.done' 'process/model/load_weights.done'
	@echo "make     FOO.reset       # resets  FOO.done"
	@echo "make -tB FOO.done        # assumes FOO.done"
	@echo "make TOUCH=    FOO.done  # shows what still needs to run to get FOO.done"
	@echo "make TOUCH= -B FOO.done  # shows everything that needs to run to get FOO.done"
all: data/company_mention.done data/has_relation.done data/information.done data/model/probabilities.done data/model/weights.done data/relation_label.done data/relation_label__0.done data/relation_label_resolved.done data/sentences.done data/supplier_candidate.done data/supplier_dbdata.done data/supplier_dbdata_2.done data/supplier_feature.done model/calibration-plots.done model/factorgraph.done model/probabilities.done model/weights.done process/ext_company_mention_by_map_company_mention.done process/ext_has_relation.done process/ext_relation_label.done process/ext_relation_label__0_by_supervise.done process/ext_relation_label_resolved.done process/ext_sentences_by_nlp_markup.done process/ext_supplier_candidate_by_map_supplier_candidate.done process/ext_supplier_feature_by_extract_features.done process/grounding/combine_factorgraph.done process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.done process/grounding/factor/inf_imply_has_relation_has_relation/dump.done process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.done process/grounding/factor/inf_imply_has_relation_has_relation/materialize.done process/grounding/factor/inf_istrue_has_relation/assign_weight_id.done process/grounding/factor/inf_istrue_has_relation/dump.done process/grounding/factor/inf_istrue_has_relation/dump_weights.done process/grounding/factor/inf_istrue_has_relation/materialize.done process/grounding/global_weight_table.done process/grounding/variable/has_relation/assign_id.done process/grounding/variable/has_relation/dump.done process/grounding/variable_holdout.done process/grounding/variable_id_partition.done process/grounding/weight_id_partition.done process/init/app.done process/init/relation/information.done process/init/relation/supplier_dbdata.done process/init/relation/supplier_dbdata_2.done process/model/calibration.done process/model/inference.done process/model/learning.done process/model/load_probabilities.done process/model/load_weights.done
reset: data/company_mention.reset data/has_relation.reset data/information.reset data/model/probabilities.reset data/model/weights.reset data/relation_label.reset data/relation_label__0.reset data/relation_label_resolved.reset data/sentences.reset data/supplier_candidate.reset data/supplier_dbdata.reset data/supplier_dbdata_2.reset data/supplier_feature.reset model/calibration-plots.reset model/factorgraph.reset model/probabilities.reset model/weights.reset process/ext_company_mention_by_map_company_mention.reset process/ext_has_relation.reset process/ext_relation_label.reset process/ext_relation_label__0_by_supervise.reset process/ext_relation_label_resolved.reset process/ext_sentences_by_nlp_markup.reset process/ext_supplier_candidate_by_map_supplier_candidate.reset process/ext_supplier_feature_by_extract_features.reset process/grounding/combine_factorgraph.reset process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.reset process/grounding/factor/inf_imply_has_relation_has_relation/dump.reset process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.reset process/grounding/factor/inf_imply_has_relation_has_relation/materialize.reset process/grounding/factor/inf_istrue_has_relation/assign_weight_id.reset process/grounding/factor/inf_istrue_has_relation/dump.reset process/grounding/factor/inf_istrue_has_relation/dump_weights.reset process/grounding/factor/inf_istrue_has_relation/materialize.reset process/grounding/global_weight_table.reset process/grounding/variable/has_relation/assign_id.reset process/grounding/variable/has_relation/dump.reset process/grounding/variable_holdout.reset process/grounding/variable_id_partition.reset process/grounding/weight_id_partition.reset process/init/app.reset process/init/relation/information.reset process/init/relation/supplier_dbdata.reset process/init/relation/supplier_dbdata_2.reset process/model/calibration.reset process/model/inference.reset process/model/learning.reset process/model/load_probabilities.reset process/model/load_weights.reset
.PHONY: help list list-targets all reset %.reset


process/init/app.done: 
	## process/init/app ##########################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/init/app.reset:
	$(RESET) process/init/app.done

process/init/relation/information.done: process/init/app.done
	## process/init/relation/information #########################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/init/relation/information.reset:
	$(RESET) process/init/relation/information.done

process/init/relation/supplier_dbdata.done: process/init/app.done
	## process/init/relation/supplier_dbdata #####################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/init/relation/supplier_dbdata.reset:
	$(RESET) process/init/relation/supplier_dbdata.done

process/init/relation/supplier_dbdata_2.done: process/init/app.done
	## process/init/relation/supplier_dbdata_2 ###################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/init/relation/supplier_dbdata_2.reset:
	$(RESET) process/init/relation/supplier_dbdata_2.done

process/ext_company_mention_by_map_company_mention.done: data/sentences.done
	## process/ext_company_mention_by_map_company_mention ########################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_company_mention_by_map_company_mention.reset:
	$(RESET) process/ext_company_mention_by_map_company_mention.done

process/ext_has_relation.done: data/relation_label_resolved.done
	## process/ext_has_relation ##################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_has_relation.reset:
	$(RESET) process/ext_has_relation.done

process/ext_relation_label.done: data/relation_label__0.done data/supplier_candidate.done data/supplier_dbdata.done data/supplier_dbdata_2.done
	## process/ext_relation_label ################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_relation_label.reset:
	$(RESET) process/ext_relation_label.done

process/ext_relation_label__0_by_supervise.done: data/company_mention.done data/sentences.done data/supplier_candidate.done
	## process/ext_relation_label__0_by_supervise ################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_relation_label__0_by_supervise.reset:
	$(RESET) process/ext_relation_label__0_by_supervise.done

process/ext_relation_label_resolved.done: data/relation_label.done
	## process/ext_relation_label_resolved #######################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_relation_label_resolved.reset:
	$(RESET) process/ext_relation_label_resolved.done

process/ext_sentences_by_nlp_markup.done: data/information.done
	## process/ext_sentences_by_nlp_markup #######################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_sentences_by_nlp_markup.reset:
	$(RESET) process/ext_sentences_by_nlp_markup.done

process/ext_supplier_candidate_by_map_supplier_candidate.done: data/company_mention.done
	## process/ext_supplier_candidate_by_map_supplier_candidate ##################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_supplier_candidate_by_map_supplier_candidate.reset:
	$(RESET) process/ext_supplier_candidate_by_map_supplier_candidate.done

process/ext_supplier_feature_by_extract_features.done: data/company_mention.done data/sentences.done
	## process/ext_supplier_feature_by_extract_features ##########################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/ext_supplier_feature_by_extract_features.reset:
	$(RESET) process/ext_supplier_feature_by_extract_features.done

process/grounding/variable_id_partition.done: data/has_relation.done
	## process/grounding/variable_id_partition ###################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/variable_id_partition.reset:
	$(RESET) process/grounding/variable_id_partition.done

process/grounding/variable/has_relation/assign_id.done: process/grounding/variable_id_partition.done
	## process/grounding/variable/has_relation/assign_id #########################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/variable/has_relation/assign_id.reset:
	$(RESET) process/grounding/variable/has_relation/assign_id.done

process/grounding/variable_holdout.done: process/grounding/variable/has_relation/assign_id.done
	## process/grounding/variable_holdout ########################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/variable_holdout.reset:
	$(RESET) process/grounding/variable_holdout.done

process/grounding/variable/has_relation/dump.done: process/grounding/variable_holdout.done
	## process/grounding/variable/has_relation/dump ##############################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/variable/has_relation/dump.reset:
	$(RESET) process/grounding/variable/has_relation/dump.done

process/grounding/factor/inf_imply_has_relation_has_relation/materialize.done: data/supplier_candidate.done process/grounding/variable/has_relation/assign_id.done
	## process/grounding/factor/inf_imply_has_relation_has_relation/materialize ##
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_imply_has_relation_has_relation/materialize.reset:
	$(RESET) process/grounding/factor/inf_imply_has_relation_has_relation/materialize.done

process/grounding/factor/inf_istrue_has_relation/materialize.done: data/supplier_candidate.done data/supplier_feature.done process/grounding/variable/has_relation/assign_id.done
	## process/grounding/factor/inf_istrue_has_relation/materialize ##############
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_istrue_has_relation/materialize.reset:
	$(RESET) process/grounding/factor/inf_istrue_has_relation/materialize.done

process/grounding/weight_id_partition.done: process/grounding/factor/inf_imply_has_relation_has_relation/materialize.done process/grounding/factor/inf_istrue_has_relation/materialize.done
	## process/grounding/weight_id_partition #####################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/weight_id_partition.reset:
	$(RESET) process/grounding/weight_id_partition.done

process/grounding/global_weight_table.done: process/grounding/factor/inf_imply_has_relation_has_relation/materialize.done process/grounding/factor/inf_istrue_has_relation/materialize.done
	## process/grounding/global_weight_table #####################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/global_weight_table.reset:
	$(RESET) process/grounding/global_weight_table.done

process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.done: process/grounding/weight_id_partition.done
	## process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id null
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.reset:
	$(RESET) process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.done

process/grounding/factor/inf_istrue_has_relation/assign_weight_id.done: process/grounding/weight_id_partition.done
	## process/grounding/factor/inf_istrue_has_relation/assign_weight_id #########
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_istrue_has_relation/assign_weight_id.reset:
	$(RESET) process/grounding/factor/inf_istrue_has_relation/assign_weight_id.done

process/grounding/factor/inf_imply_has_relation_has_relation/dump.done: process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.done
	## process/grounding/factor/inf_imply_has_relation_has_relation/dump #########
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_imply_has_relation_has_relation/dump.reset:
	$(RESET) process/grounding/factor/inf_imply_has_relation_has_relation/dump.done

process/grounding/factor/inf_istrue_has_relation/dump.done: process/grounding/factor/inf_istrue_has_relation/assign_weight_id.done
	## process/grounding/factor/inf_istrue_has_relation/dump #####################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_istrue_has_relation/dump.reset:
	$(RESET) process/grounding/factor/inf_istrue_has_relation/dump.done

process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.done: process/grounding/factor/inf_imply_has_relation_has_relation/assign_weight_id.done
	## process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights #
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.reset:
	$(RESET) process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.done

process/grounding/factor/inf_istrue_has_relation/dump_weights.done: process/grounding/factor/inf_istrue_has_relation/assign_weight_id.done
	## process/grounding/factor/inf_istrue_has_relation/dump_weights #############
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/factor/inf_istrue_has_relation/dump_weights.reset:
	$(RESET) process/grounding/factor/inf_istrue_has_relation/dump_weights.done

process/grounding/combine_factorgraph.done: process/grounding/factor/inf_imply_has_relation_has_relation/dump.done process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights.done process/grounding/factor/inf_istrue_has_relation/dump.done process/grounding/factor/inf_istrue_has_relation/dump_weights.done process/grounding/global_weight_table.done process/grounding/variable/has_relation/dump.done
	## process/grounding/combine_factorgraph #####################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/grounding/combine_factorgraph.reset:
	$(RESET) process/grounding/combine_factorgraph.done

process/model/learning.done: model/factorgraph.done
	## process/model/learning ####################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/model/learning.reset:
	$(RESET) process/model/learning.done

process/model/inference.done: model/factorgraph.done model/weights.done
	## process/model/inference ###################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/model/inference.reset:
	$(RESET) process/model/inference.done

process/model/load_weights.done: model/weights.done
	## process/model/load_weights ################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/model/load_weights.reset:
	$(RESET) process/model/load_weights.done

process/model/load_probabilities.done: model/probabilities.done
	## process/model/load_probabilities ##########################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/model/load_probabilities.reset:
	$(RESET) process/model/load_probabilities.done

process/model/calibration.done: data/model/probabilities.done
	## process/model/calibration #################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_process)
	$(TOUCH)
	##############################################################################

process/model/calibration.reset:
	$(RESET) process/model/calibration.done

data/company_mention.done: process/ext_company_mention_by_map_company_mention.done
	## data/company_mention ######################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/company_mention.reset:
	$(RESET) data/company_mention.done

data/has_relation.done: process/ext_has_relation.done
	## data/has_relation #########################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/has_relation.reset:
	$(RESET) data/has_relation.done

data/information.done: process/init/relation/information.done
	## data/information ##########################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/information.reset:
	$(RESET) data/information.done

data/model/probabilities.done: process/model/load_probabilities.done
	## data/model/probabilities ##################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/model/probabilities.reset:
	$(RESET) data/model/probabilities.done

data/model/weights.done: process/model/load_weights.done
	## data/model/weights ########################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/model/weights.reset:
	$(RESET) data/model/weights.done

data/relation_label.done: process/ext_relation_label.done
	## data/relation_label #######################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/relation_label.reset:
	$(RESET) data/relation_label.done

data/relation_label__0.done: process/ext_relation_label__0_by_supervise.done
	## data/relation_label__0 ####################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/relation_label__0.reset:
	$(RESET) data/relation_label__0.done

data/relation_label_resolved.done: process/ext_relation_label_resolved.done
	## data/relation_label_resolved ##############################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/relation_label_resolved.reset:
	$(RESET) data/relation_label_resolved.done

data/sentences.done: process/ext_sentences_by_nlp_markup.done
	## data/sentences ############################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/sentences.reset:
	$(RESET) data/sentences.done

data/supplier_candidate.done: process/ext_supplier_candidate_by_map_supplier_candidate.done
	## data/supplier_candidate ###################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/supplier_candidate.reset:
	$(RESET) data/supplier_candidate.done

data/supplier_dbdata.done: process/init/relation/supplier_dbdata.done
	## data/supplier_dbdata ######################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/supplier_dbdata.reset:
	$(RESET) data/supplier_dbdata.done

data/supplier_dbdata_2.done: process/init/relation/supplier_dbdata_2.done
	## data/supplier_dbdata_2 ####################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/supplier_dbdata_2.reset:
	$(RESET) data/supplier_dbdata_2.done

data/supplier_feature.done: process/ext_supplier_feature_by_extract_features.done
	## data/supplier_feature #####################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_data)
	$(TOUCH)
	##############################################################################

data/supplier_feature.reset:
	$(RESET) data/supplier_feature.done

model/calibration-plots.done: process/model/calibration.done
	## model/calibration-plots ###################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_model)
	$(TOUCH)
	##############################################################################

model/calibration-plots.reset:
	$(RESET) model/calibration-plots.done

model/factorgraph.done: process/grounding/combine_factorgraph.done
	## model/factorgraph #########################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_model)
	$(TOUCH)
	##############################################################################

model/factorgraph.reset:
	$(RESET) model/factorgraph.done

model/probabilities.done: process/model/inference.done
	## model/probabilities #######################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_model)
	$(TOUCH)
	##############################################################################

model/probabilities.reset:
	$(RESET) model/probabilities.done

model/weights.done: process/model/learning.done
	## model/weights #############################################################
	# Done: $(shell format_timestamp $@ $@~ 2>/dev/null)
	$(CMD_model)
	$(TOUCH)
	##############################################################################

model/weights.reset:
	$(RESET) model/weights.done

