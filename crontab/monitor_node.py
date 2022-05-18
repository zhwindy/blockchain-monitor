# encoding=utf-8
from utils import rpc


node_list = {
    "polygon-node-01": "172.31.28.220",
    "polygon-node-02": "172.31.30.198",
}


def main():
    for key, ip in node_list.items():
        try:
            url = f"http://{ip}:8545"
            node_data = rpc.get_newest_block(url)
            block_height = rpc.get_block_height(node_data)
            block_time = rpc.get_block_time(node_data)
            content = f"{key}: {ip} \n最新高度: {block_height}\n出块时间: {block_time}"""
        except Exception as e:
            content = str(e)
        print(content)
        rpc.send_news(content)


if __name__ == '__main__':
    main()
