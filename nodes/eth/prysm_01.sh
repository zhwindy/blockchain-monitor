#!/usr/bin/env sh

set -x

DATA_DIR=/data/node_data/prysm
JWT_DIR=/data/node_data/geth/geth/jwtsecret

/data/client/prysm --datadir $DATA_DIR \
        --accept-terms-of-use
	--execution-endpoint 'http://127.0.0.1:8551'
        --jwt-secret $JWT_DIR
