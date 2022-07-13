import pymysql
from elasticsearch import Elasticsearch

#读取tenement数据库
def get_tenement_db():
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="Chenjunyi1998.", database="sys")
    cursor = conn.cursor()
    sql = "select * from tenement"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


#读取recruit数据库
def get_recruit_db():
    conn = pymysql.connect(host="localhost", port=3306, user="root",
                           password="Chenjunyi1998.", database="sys")
    cursor = conn.cursor()
    sql = "select * from recruit"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def write_tenement_elasticsearch():
    es = Elasticsearch()
    try:
        results = get_tenement_db()
        for row in results:
            res = {
                "id" : row[0],
                "create_time": row[1],
                "flat_name": row[2],
                "flat_id": row[3],
                "room_count": row[4],
                "bathroom_count":row[5],
                "kitchen_count": row[6],
                "livingroom_count": row[7],
                "price": row[8],
                "deposit": row[9],
                "telephone1": row[10],
                "telephone2": row[11],
                "address": row[12],
                "kitchen": row[13],
                "window": row[14],
                "lift": row[15],
                "remark": row[16],
                "hasMoveIn": row[17],
                "image1": row[18],
                "image2": row[19],
                "image3": row[20],
                "image4": row[21],
                "image5": row[22],
                "image6": row[23]
            }
            es.index(index="tenement", body=res, id=row[0])
    except Exception as e:
        print(e)


def write_recruit_elasticsearch():
    es = Elasticsearch()
    try:
        results = get_recruit_db()
        print(results)
        for row in results:
            res = {
                "id": row[0],
                "create_time": row[1],
                "unit": row[2],
                "content": row[3],
                "category": row[4],
                "pay": row[5],
                "commend": row[6],
                "address": row[7],
                "contact": row[8],
                "remark": row[9],
                "hasMoveIn": row[10]
            }
            es.index(index="recruit", body=res, id=row[0])
    except Exception as e:
        print(e)



if __name__ == "__main__":
    write_tenement_elasticsearch()
    write_recruit_elasticsearch()
    c = 1

