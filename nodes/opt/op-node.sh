/data/client/optimism/op-node/bin/op-node --l1=https:// \
        --l2=http://127.0.0.1:8551 \
        --l2.jwt-secret=/data/node_data/geth/jwtsecret \
        --network=mainnet \
        --rpc.addr=127.0.0.1 \
        --rpc.port=9545 \
        --p2p.priv.path=/data/node_data/op-node/opnode_p2p_priv.txt \
        --p2p.discovery.path=memory \
        --p2p.peerstore.path=memory