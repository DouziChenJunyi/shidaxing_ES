import pymysql
from elasticsearch import Elasticsearch

#读取数据库
def get_db():
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="chenjunyi1998", database="mysql_for_shidaxing")
    cursor = conn.cursor()
    sql = "select * from tenement"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def write_elasticsearch():
    es = Elasticsearch()
    try:
        results = get_db()
        for row in results:
            res = {
                "id" : row[0],
                "create_time": row[1],
                "flat_name": row[2],
                "flat_id": row[3],
                "room_count": row[4]
            }
            es.index(index="tenement", body=res, id=row[0])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    write_elasticsearch()



