# encoding=utf-8
import pymysql
import datetime

host = "nftscan-source-db-instance-1.cjotu4lyzmfi.ap-southeast-1.rds.amazonaws.com"
user = ""
passwd = ""


def get_data():
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db='eth_source', charset='utf8')
    cursor = conn.cursor()
    sql = """
        select block_number,create_time from eth_source_block order by block_number desc limit 1
    """
    info = {
        "block_number": 0,
        "create_time": 0
    }
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        block_number = result[0]
        create_time = result[1]
        info['block_number'] = block_number
        info['create_time'] = create_time
    except Exception as e:
        print(e)
    conn.close()
    return info


def main():
    info = get_data()
    now = datetime.datetime.now()
    record_time = info.get("create_time")
    diff = now - record_time
    seconds = diff.seconds
    min = seconds // 60
    print(min)


if __name__ == "__main__":
    main()
    # print(get_data())
    