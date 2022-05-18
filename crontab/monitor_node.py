# encoding=utf-8
from utils import rpc


node_list = {
    "moonbeam-node": {"ip": "172.31.23.220", "port": 30335},
    "Arbitrum-node": {"ip": "172.31.27.235", "port": 8547},
    "Optimism-node": {"ip": "172.31.18.109", "port": 9991},
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
            content = f"{node}: {ip} \n最新高度: {block_height}\n时间: {block_time}"""
        except Exception as e:
            content = str(e)
        print(content)
        rpc.send_news(content)


if __name__ == '__main__':
    main()
