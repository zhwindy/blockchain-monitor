# encoding=utf-8
import time
import requests

RPC_URL = "http://172.31.30.46:8545"


def get_block_by_number(block_number):
    """
    block_number十六进制区块高度
    """
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [block_number, True],
        "id": 1
    }
    try:
        res = requests.post(RPC_URL, json=param, timeout=20)
        result = res.json()
        data = result.get("result", {})
    except Exception as e:
        data = {}
    return data


def get_tx_receipt_by_hash(tx_hash):
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [str(tx_hash)],
        "id": 1
    }
    try:
        res = requests.post(RPC_URL, json=param, timeout=20)
        result = res.json()
        data = result.get("result", {})
    except Exception as e:
        data = {}
    return data


def test_getblock():
    """
    测试getblockbyNumber
    """
    highest_number = 10000
    num = 1
    while num < highest_number:
        hex_num = hex(num)
        block_info = get_block_by_number(hex_num)
        transactions = block_info.get("transactions")
        print(f"block_num: {num}, transactions: {transactions}")
        num += 1
