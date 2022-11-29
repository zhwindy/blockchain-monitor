#!/usr/bin/env sh

set -x

DATA_DIR=/data/node_data/geth
JWT_DIR=/data/node_data/geth/geth/jwtsecret

geth --datadir $DATA_DIR \
        --txlookuplimit 0 \
        --http \
        --http.addr '0.0.0.0' \
        --http.port 40000 \
        --http.vhosts '*' \
        --http.corsdomain '*' \
	--rpc.allow-unprotected-txs \
        --authrpc.jwtsecret $JWT_DIR \
        --authrpc.vhosts '*'
