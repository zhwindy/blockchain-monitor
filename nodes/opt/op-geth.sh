!/usr/bin/env sh

set -x

DATA_DIR=/data/node_data/geth
JWT_DIR=/data/node_data/geth/jwtsecret

/data/client/op-geth/build/bin/geth --datadir $DATA_DIR \
        --txlookuplimit 0 \
        --http \
        --http.addr '0.0.0.0' \
        --http.port 8545 \
        --http.vhosts '*' \
        --http.corsdomain '*' \
        --authrpc.addr=localhost \
        --authrpc.jwtsecret $JWT_DIR \
        --authrpc.port=8551 \
        --authrpc.vhosts '*' \
        --verbosity=3 \
        --rollup.disabletxpoolgossip=true \
        --rollup.sequencerhttp=https://mainnet-sequencer.optimism.io \
        --nodiscover \
        --syncmode=full \
        --maxpeers=0