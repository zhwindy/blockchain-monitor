#!/usr/bin/env sh

set -x

DATA_DIR=/data/node_data/lighthouse
JWT_DIR=/data/node_data/geth/geth/jwtsecret

lighthouse beacon_node --network 'mainnet' \
        --datadir $DATA_DIR \
        --checkpoint-sync-url 'https://mainnet-checkpoint-sync.stakely.io' \
        --http \
        --http-address '0.0.0.0' \
        --http-port 8080 \
        --http-allow-origin '*' \
        --execution-endpoint 'http://127.0.0.1:8551' \
        --execution-jwt $JWT_DIR
