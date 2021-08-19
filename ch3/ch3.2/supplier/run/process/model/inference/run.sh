#!/usr/bin/env bash
# cmd_extractor  process/model/inference
# {"dependencies_":["model/factorgraph","model/weights"],"output_":"model/probabilities","style":"cmd_extractor","cmd":"mkdir -p ../../../model && cd ../../../model\n            [ -d factorgraph ] || error \"No factorgraph found\"\n            if [[ factorgraph/weights -nt probabilities/inference_result.out.text ]]; then\n                # no need to run inference unless the weights are fresher\n                # XXX this skipping may cause confusion\n                # run sampler for performing inference with given weights without learning\n                flatten() { find -L \"$@\" -type f -exec pbzip2 -c -d -k {} +; }\n                sampler-dw \\\n                    gibbs \\\n                    -w <(flatten factorgraph/weights) \\\n                    -v <(flatten factorgraph/variables) \\\n                    -f <(flatten factorgraph/factors) \\\n                    -m factorgraph/meta \\\n                    -o weights \\\n                    -l 1000 -s 1 -i 1000 --alpha 0.01 --sample_evidence \\\n                    -l 0 \\\n                    #\n                mkdir -p probabilities\n                mv -f weights/inference_result.out.text probabilities/\n            fi\n        ","name":"process/model/inference"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/model/inference'
mkdir -p ../../../model && cd ../../../model
            [ -d factorgraph ] || error "No factorgraph found"
            if [[ factorgraph/weights -nt probabilities/inference_result.out.text ]]; then
                # no need to run inference unless the weights are fresher
                # XXX this skipping may cause confusion
                # run sampler for performing inference with given weights without learning
                flatten() { find -L "$@" -type f -exec pbzip2 -c -d -k {} +; }
                sampler-dw \
                    gibbs \
                    -w <(flatten factorgraph/weights) \
                    -v <(flatten factorgraph/variables) \
                    -f <(flatten factorgraph/factors) \
                    -m factorgraph/meta \
                    -o weights \
                    -l 1000 -s 1 -i 1000 --alpha 0.01 --sample_evidence \
                    -l 0 \
                    #
                mkdir -p probabilities
                mv -f weights/inference_result.out.text probabilities/
            fi
        



