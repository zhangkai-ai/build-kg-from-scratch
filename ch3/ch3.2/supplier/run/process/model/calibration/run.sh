#!/usr/bin/env bash
# cmd_extractor  process/model/calibration
# {"dependencies_":["data/model/probabilities","process/model/load_probabilities"],"output_":"model/calibration-plots","style":"cmd_extractor","cmd":"\n            d=../../../model/calibration-plots && mkdir -p \"$d\" && cd \"$d\"\n            # XXX a legacy location under the current run directory for backward compatibility\n            extraOutput=\"${DEEPDIVE_OUTPUT:-../../RUNNING}\"/calibration && mkdir -p \"$extraOutput\"\n            DEEPDIVE_CALIBRATION_NUM_BUCKETS=10\n            \n            # create a view and draw a calibration plot for variable null\n            deepdive db create_calibration_view 'has_relation' 'label'\n            draw_calibration_plot      'has_relation' 'label'\n            # XXX keeping a duplicate copy under the current run directory for backward compatibility\n            cp -a 'has_relation_label'.* \"$extraOutput\"/\n            \n        ","name":"process/model/calibration"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/model/calibration'

            d=../../../model/calibration-plots && mkdir -p "$d" && cd "$d"
            # XXX a legacy location under the current run directory for backward compatibility
            extraOutput="${DEEPDIVE_OUTPUT:-../../RUNNING}"/calibration && mkdir -p "$extraOutput"
            DEEPDIVE_CALIBRATION_NUM_BUCKETS=10
            
            # create a view and draw a calibration plot for variable null
            deepdive db create_calibration_view 'has_relation' 'label'
            draw_calibration_plot      'has_relation' 'label'
            # XXX keeping a duplicate copy under the current run directory for backward compatibility
            cp -a 'has_relation_label'.* "$extraOutput"/
            
        



