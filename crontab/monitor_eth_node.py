# encoding=utf-8
import sys
sys.path.append("..")
from utils import rpc


node_list = {
    "eth-node-01": {"ip": "172.31.23.144", "port": 40000},
    "eth-node-02": {"ip": "172.31.25.134", "port": 40000},
    "polygon-node-01": {"ip": "172.31.28.220", "port": 8545},
    "polygon-node-02": {"ip": "172.31.30.198", "port": 8545},
}


def main():
    for node, config in node_list.items():
        try:
            ip = config.get("ip")
            port = config.get("port")
            if (not ip) or (not port):
                continue
            url = f"http://{ip}:{port}"
            node_data = rpc.get_newest_block(url)
            block_height = rpc.get_block_height(node_data)
            block_time = rpc.get_block_time(node_data)
            content = f"{node}: {ip} \n最新高度: {block_height}\n出块时间: {block_time}"""
        except Exception as e:
            content = str(e)
        print(content)
        rpc.send_news(content)


if __name__ == '__main__':
    main()
