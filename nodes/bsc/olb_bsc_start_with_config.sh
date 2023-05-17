#!/usr/bin/env sh

set -x

CONFIG_DIR=/data/client/config.toml

bsc --rpc.allow-unprotected-txs --config $CONFIG_DIR --syncmode 'full' --pruneancient
