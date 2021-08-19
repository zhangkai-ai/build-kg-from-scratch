#!/usr/bin/env bash
# cmd_extractor  process/init/app
# {"style":"cmd_extractor","cmd":"\n        deepdive db init\n\n        cd \"$DEEPDIVE_APP\"\n        # run legacy schema.sql\n        if [[ -r schema.sql ]]; then\n            deepdive db prompt <schema.sql\n        fi\n        # run legacy init script\n        if [[ -x input/init.sh ]]; then\n            input/init.sh\n        fi\n        ","name":"process/init/app"}
set -xeuo pipefail
cd "$(dirname "$0")"



export DEEPDIVE_CURRENT_PROCESS_NAME='process/init/app'

        deepdive db init

        cd "$DEEPDIVE_APP"
        # run legacy schema.sql
        if [[ -r schema.sql ]]; then
            deepdive db prompt <schema.sql
        fi
        # run legacy init script
        if [[ -x input/init.sh ]]; then
            input/init.sh
        fi
        



