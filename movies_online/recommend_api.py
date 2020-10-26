# coding:utf-8
import time
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALSModel
from flask import Flask, jsonify

app = Flask(__name__)


def create_spark():
    spark = SparkSession.builder.master("local[*]").appName('movie_recommend') \
        .config("spark.executor.memory", "16g").config("spark.network.timeout", "20000s") \
        .config("spark.executor.heartbeatInterval", "10000s").config('spark.driver.memory', '16g') \
        .getOrCreate()
    return spark


@app.route('/')
def index():
    return 'hello world'


@app.route('/api/user/<int:user_id>/<int:num>', methods=['get'])
@app.route('/api/user/<int:user_id>/', methods=['get'], defaults={'num': 10})
def recommend_item(user_id, num):
    print(user_id, num)
    try:
        user = spark.createDataFrame([(user_id,)], ['user'])
        prediction = model.recommendForUserSubset(user, num)
        res = prediction.select('recommendations.item').first().item
    except Exception as e:
        print(e)
        res = []
    return jsonify(res)


if __name__ == '__main__':
    spark = create_spark()
    localtime = time.localtime(time.time())
    model = ALSModel.load(
        'file:///D:/Projects/python_projects/movie_recommendation/model/best_als_model_%s_%s_%s' % localtime[:3])
    print(model)
    app.run(host='127.0.0.1', port='8080', debug=True)
