#!/usr/bin/env sh

set -x

DATA_DIR=/data/node_data/prysm
JWT_DIR=/data/node_data/geth/geth/jwtsecret

/data/client/prysm --datadir $DATA_DIR \
        --accept-terms-of-use
	--checkpoint-sync-url 'https://2EmWsLTGyrGcn94HQJEKRT9S7LS:8797478c9df2b0dfcc6367861754fef1@eth2-beacon-mainnet.infura.io' \
	--genesis-beacon-api-url 'https://2EmWsLTGyrGcn94HQJEKRT9S7LS:8797478c9df2b0dfcc6367861754fef1@eth2-beacon-mainnet.infura.io' \
	--execution-endpoint 'http://127.0.0.1:8551'
        --jwt-secret $JWT_DIR
