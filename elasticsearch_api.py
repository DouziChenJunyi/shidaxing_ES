import pymysql
from elasticsearch import Elasticsearch
from models import Tenement,Recruit
from Pagination import Pagination

def query_tenement(hasMoveIn, flat_name, price, page):
    per_page = 3
    es = Elasticsearch()
    if hasMoveIn:
        hasMoveIn = 1
    else:
        hasMoveIn = 0

    if flat_name == "none":
        if price == "none":
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ]
            }
        else:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {"price": price}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {"price": price}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ]
            }

    else:
        if price == "none":
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"flat_name": flat_name}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"flat_name": flat_name}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ]
            }

        else:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"flat_name": flat_name}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            },
                            {
                                "match_phrase": {"price": price}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"flat_name": flat_name}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            },
                            {
                                "match_phrase": {"price": price}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
            }
    try:
        total = es.search(index="tenement", body=query_total)['hits']['total']['value']
        result = es.search(index="tenement", body=query)['hits']['hits']
        items = []
        for row in result:
            info = row['_source']
            tenement = Tenement(id=info['id'], create_time=info['create_time'], flat_name=info['flat_name'],
                                flat_id=info['flat_id'], room_count=info['room_count'], bathroom_count=info['bathroom_count'],
                                kitchen_count=info['kitchen_count'], livingroom_count=info['livingroom_count'], price=info['price'],
                                deposit=info['deposit'], telephone1=info['telephone1'], telephone2=info['telephone2'], address=info['address'],
                                kitchen=info['kitchen'], window=info['window'], lift=info['lift'], remark=info['remark'], hasMoveIn=info['hasMoveIn'],
                                image1=info['image1'], image2=info['image2'], image3=info['image3'],
                                image4=info['image4'], image5=info['image5'], image6=info['image6'])
            items.append(tenement)
        return Pagination(page, per_page, total, items)
    except Exception as e:   # 20220617
        return Pagination(page, per_page, [], [])





def query_recruit(hasMoveIn, recruit_unit, category, page):
    per_page = 3
    es = Elasticsearch()
    if hasMoveIn:
        hasMoveIn = 1
    else:
        hasMoveIn = 0

    if recruit_unit == "none":
        if category == "none":
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
        else:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {"category": category}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {"category": category}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
    else:
        if category == "none":
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"unit": recruit_unit}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
            }
            query_toal = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"unit": recruit_unit}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }
        else:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"unit": recruit_unit}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            },
                            {
                                "match_phrase": {"category": category}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
            }
            query_total = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {"unit": recruit_unit}
                            },
                            {
                                "term": {"hasMoveIn": hasMoveIn}
                            },
                            {
                                "match_phrase": {"category": category}
                            }
                        ]
                    }
                },
                "sort": [
                    {"create_time": "desc"}
                ],
                "from": (page - 1) * per_page,
                "size": per_page
            }

    total = es.search(index="recruit", body=query_total)['hits']['total'][
        'value']
    result = es.search(index="recruit", body=query)['hits']['hits']
    items = []
    for row in result:
        info = row['_source']
        print(info)
        recruit = Recruit(id=info['id'], create_time=info['create_time'], unit=info['unit'],
                          content=info['content'], category=info['category'], pay=info['pay'],
                          commend=info['commend'], address=info['address'], contact=info['contact'],
                          remark=info['remark'], hasMoveIn='hasMoveIn')

        items.append(recruit)
    return Pagination(page, per_page, total, items)



if __name__ == "__main__":
    hasMoveIn = True
    flat_name = "公寓"
    price = "none"
    page = 2
    # query_tenement(hasMoveIn, flat_name, price, page)


    # recruit_unit = "二十八所"
    recruit_unit = "none"
    # category = "none"
    category = "店员"
    # query_tenement(hasMoveIn, flat_name, price)
    query_recruit(hasMoveIn, recruit_unit, category,page)
