from elasticsearch import Elasticsearch
from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello world!!"

@app.route("/get_es/<query>")
def get_es(query):
    es = Elasticsearch()
    dsl = {
        "query":{
            "multi_match":{
                "query": query,
                "fields":["flat_name", "flat_id"]
            }
        }
    }

    results = es.search(index="tenement", body=dsl, size=10)
    return results

if __name__ == "__main__":
    app.run()


