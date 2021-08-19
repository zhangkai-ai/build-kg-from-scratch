#!/usr/bin/env bash
# cmd_extractor  process/grounding/combine_factorgraph
# {"dependencies_":["process/grounding/variable/has_relation/dump","process/grounding/factor/inf_imply_has_relation_has_relation/dump","process/grounding/factor/inf_imply_has_relation_has_relation/dump_weights","process/grounding/factor/inf_istrue_has_relation/dump","process/grounding/factor/inf_istrue_has_relation/dump_weights","process/grounding/global_weight_table"],"output_":"model/factorgraph","style":"cmd_extractor","cmd":"\n        : ${DEEPDIVE_GROUNDING_DIR:=\"$DEEPDIVE_APP\"/run/model/grounding}\n        : ${DEEPDIVE_FACTORGRAPH_DIR:=\"$DEEPDIVE_APP\"/run/model/factorgraph}\n\n        # create a fresh empty directory for the new combined factor graph\n        rm -rf   \"$DEEPDIVE_FACTORGRAPH_DIR\"\n        mkdir -p \"$DEEPDIVE_FACTORGRAPH_DIR\"\n        cd \"$DEEPDIVE_FACTORGRAPH_DIR\"\n\n        # create symlinks to the grounded binaries by enumerating variables and factors\n        for v in 'has_relation'; do\n            mkdir -p variables/\"$v\"\n            find \"$DEEPDIVE_GROUNDING_DIR\"/variable/\"$v\" \\\n                -name 'variables.part-*.bin.bz2' -exec ln -sfnv -t variables/\"$v\"/ {} + \\\n                #\n        done\n        for f in 'inf_imply_has_relation_has_relation' 'inf_istrue_has_relation'; do\n            mkdir -p {factors,weights}/\"$f\"\n            find \"$DEEPDIVE_GROUNDING_DIR\"/factor/\"$f\" \\\n                -name 'factors.part-*.bin.bz2' -exec ln -sfnv -t factors/\"$f\"/ {} + \\\n                -o \\\n                -name 'weights.part-*.bin.bz2' -exec ln -sfnv -t weights/\"$f\"/ {} + \\\n                #\n        done\n\n        # generate the metadata for the inference engine\n        {\n            # first line with counts of variables and edges in the grounded factor graph\n            cd \"$DEEPDIVE_GROUNDING_DIR\"\n            sumup() { { tr '\\n' +; echo 0; } | bc; }\n            counts=()\n            counts+=($(cat factor/weights_count))\n            # sum up the number of factors and edges\n            counts+=($(cat variable_count))\n            cd factor\n            counts+=($(find 'inf_imply_has_relation_has_relation' 'inf_istrue_has_relation' -name 'nfactors.part-*' -exec cat {} + | sumup))\n            counts+=($(find 'inf_imply_has_relation_has_relation' 'inf_istrue_has_relation' -name 'nedges.part-*'   -exec cat {} + | sumup))\n            (IFS=,; echo \"${counts[*]}\")\n            # second line with file paths\n            paths=(\"$DEEPDIVE_FACTORGRAPH_DIR\"/{weights,variables,factors,edges})\n            (IFS=,; echo \"${paths[*]}\")\n        } >meta\n        ","name":"process/grounding/combine_factorgraph"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/grounding/combine_factorgraph'

        : ${DEEPDIVE_GROUNDING_DIR:="$DEEPDIVE_APP"/run/model/grounding}
        : ${DEEPDIVE_FACTORGRAPH_DIR:="$DEEPDIVE_APP"/run/model/factorgraph}

        # create a fresh empty directory for the new combined factor graph
        rm -rf   "$DEEPDIVE_FACTORGRAPH_DIR"
        mkdir -p "$DEEPDIVE_FACTORGRAPH_DIR"
        cd "$DEEPDIVE_FACTORGRAPH_DIR"

        # create symlinks to the grounded binaries by enumerating variables and factors
        for v in 'has_relation'; do
            mkdir -p variables/"$v"
            find "$DEEPDIVE_GROUNDING_DIR"/variable/"$v" \
                -name 'variables.part-*.bin.bz2' -exec ln -sfnv -t variables/"$v"/ {} + \
                #
        done
        for f in 'inf_imply_has_relation_has_relation' 'inf_istrue_has_relation'; do
            mkdir -p {factors,weights}/"$f"
            find "$DEEPDIVE_GROUNDING_DIR"/factor/"$f" \
                -name 'factors.part-*.bin.bz2' -exec ln -sfnv -t factors/"$f"/ {} + \
                -o \
                -name 'weights.part-*.bin.bz2' -exec ln -sfnv -t weights/"$f"/ {} + \
                #
        done

        # generate the metadata for the inference engine
        {
            # first line with counts of variables and edges in the grounded factor graph
            cd "$DEEPDIVE_GROUNDING_DIR"
            sumup() { { tr '\n' +; echo 0; } | bc; }
            counts=()
            counts+=($(cat factor/weights_count))
            # sum up the number of factors and edges
            counts+=($(cat variable_count))
            cd factor
            counts+=($(find 'inf_imply_has_relation_has_relation' 'inf_istrue_has_relation' -name 'nfactors.part-*' -exec cat {} + | sumup))
            counts+=($(find 'inf_imply_has_relation_has_relation' 'inf_istrue_has_relation' -name 'nedges.part-*'   -exec cat {} + | sumup))
            (IFS=,; echo "${counts[*]}")
            # second line with file paths
            paths=("$DEEPDIVE_FACTORGRAPH_DIR"/{weights,variables,factors,edges})
            (IFS=,; echo "${paths[*]}")
        } >meta
        



