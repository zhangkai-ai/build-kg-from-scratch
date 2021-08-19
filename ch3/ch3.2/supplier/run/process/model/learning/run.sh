#!/usr/bin/env bash
# cmd_extractor  process/model/learning
# {"dependencies_":["model/factorgraph"],"output_":"model/weights","style":"cmd_extractor","cmd":"mkdir -p ../../../model && cd ../../../model\n            mkdir -p weights\n            [ -d factorgraph ] || error \"No factorgraph found\"\n            # run inference engine for learning and inference\n            flatten() { find -L \"$@\" -type f -exec pbzip2 -c -d -k {} +; }\n            sampler-dw \\\n                gibbs \\\n                -w <(flatten factorgraph/weights) \\\n                -v <(flatten factorgraph/variables) \\\n                -f <(flatten factorgraph/factors) \\\n                -m factorgraph/meta \\\n                -o weights \\\n                -l 1000 -s 1 -i 1000 --alpha 0.01 --sample_evidence\n            mkdir -p probabilities\n            mv -f weights/inference_result.out.text probabilities/\n        ","name":"process/model/learning"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/model/learning'
mkdir -p ../../../model && cd ../../../model
            mkdir -p weights
            [ -d factorgraph ] || error "No factorgraph found"
            # run inference engine for learning and inference
            flatten() { find -L "$@" -type f -exec pbzip2 -c -d -k {} +; }
            sampler-dw \
                gibbs \
                -w <(flatten factorgraph/weights) \
                -v <(flatten factorgraph/variables) \
                -f <(flatten factorgraph/factors) \
                -m factorgraph/meta \
                -o weights \
                -l 1000 -s 1 -i 1000 --alpha 0.01 --sample_evidence
            mkdir -p probabilities
            mv -f weights/inference_result.out.text probabilities/
        



