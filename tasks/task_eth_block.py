# encoding=utf-8
import requests
import redis
import json
import time

node_url = "http://172.31.23.144:40000"

redis_key = "eth_delay_0_info"

redis_client = redis.Redis(host='127.0.0.1', port=6379)


def get_newest_block(url):
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": ["latest", False],
        "id": 1
    }
    try:
        res = requests.post(url, json=param, timeout=30)
        result = res.json()
        data = result.get("result", {})
    except Exception as e:
        data = {}
    return data


def get_block_height(data):
    block_height = data.get("number", 1)
    height = int(block_height, base=16)
    return height


def get_block_hash(data):
    block_hash = data.get("hash", 1)
    return block_hash


def get_block_time(data):
    time = data.get("timestamp", "1000000000")
    timestamp = int(time, base=16)
    return timestamp


def main():
    while True:
        try:
            result = {}
            data = get_newest_block(node_url)
            height = get_block_height(data)
            hash = get_block_hash(data)
            block_time = get_block_time(data)
            result['height'] = height
            result['hash'] = hash
            result['time'] = block_time
        except Exception as e:
            result = {}
        if result:
            redis_client.lpush(redis_key, json.dumps(result))
            redis_key_len = redis_client.llen(redis_key)
            if redis_key_len > 200:
                redis_client.ltrim(redis_key, 0, 200)
        time.sleep(2)


if __name__ == '__main__':
    main()
