#!/usr/bin/env sh

set -x

DATA_DIR=/data/node_data/bsc

bsc --datadir $DATA_DIR \
        --networkid 56 \
        --ipcpath 'geth.ipc' \
        --txlookuplimit 0 \
        --http \
        --http.addr '0.0.0.0' \
        --http.port 8545 \
        --http.vhosts '*' \
        --http.corsdomain '*' \
        --rpc.allow-unprotected-txs \
        --port 30311 \
        --metrics \
        --metrics.expensive \
        --metrics.influxdb \
        --metrics.influxdb.endpoint "http://172.31.23.180:8086" \
        --metrics.influxdb.database "eth" \
        --metrics.influxdb.username "eth" \
        --metrics.influxdb.password "ethmonitor" \
