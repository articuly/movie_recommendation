# coding:utf-8
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import col
from movie_recommend.load_data import create_spark, load_ratings

spark=create_spark()
# #####################################
# 根据用户点评数量筛选点评记录，筛选标准，参与的评价次数不少于20次
# 根据影片被点评数量筛选点评记录， 筛选标准，被点评数量不少于50次
# #####################################
def screening_ratings():
    '''
    筛选点评数在20以上的用户
    筛选被点评次数在50以上的用户
    '''
    ratings=load_ratings(spark)
    print('影评总数：', ratings.count())
    # 筛选用户
    recommend_users=ratings.select('user_id').groupby('user_id').count()  # 600337用户
    print(recommend_users.show())
    # 使用filter进行筛选，count结果>=20的用户
    recommend_users=recommend_users.filter('count>=20')  # 33765用户
    # 使用内联，从ratings中筛选只包含点评次数达到20以上的用户点评记录
    recommend_users_ratings=ratings.join(recommend_users.select('user_id'), on='user_id')
    recommend_users_ratings.cache()
    # 在筛选点评数20以上的点评记录数
    print('user rating count >=20:', recommend_users_ratings.count())  # 2604840 rows

    # 筛选影片
    # 在用户筛选的基础上再筛选被点评数超过50的影片点评记录
    recommend_movies=recommend_users_ratings.select('m_id').groupby('m_id').count()
    recommend_movies.cache()
    recommend_movies=recommend_movies.filter('count>=50')  # 66208 movies
    # 使用内联方法筛选记录，只包含被点评数在50以上的影片点评记录
    recommend_ratings=recommend_users_ratings.join(recommend_movies.select('m_id'), on='m_id')
    recommend_ratings.cache()
    # 最终进入训练模型的影评记录数量
    print('movie rating count >= 50', recommend_ratings.count())  # 2061057 rows

    # 最终返回的是用户点评数在20以上，并且每部影片的被点评数都在50以上
    # 模型训练字段要求(user, item, rating)
    fields={'user_id':'user', 'm_id':'item', 'rating':'rating'}
    res=recommend_ratings.select([col(c).alias(fields.get(c)) for c in ('user_id', 'm_id', 'rating')])
    return res


if __name__ == '__main__':
    res=screening_ratings()

    # fit model
    als=ALS(rank=10, seed=42)
    model=als.fit(res)

    # predict
    users=res.select('user').limit(10)
    recommend_items=model.recommendForUserSubset(users, 10)
    print(recommend_items.show())

    # save
    model.save('file:///Projects/python_projects/movie_recommendation/model/first_als_model')

    print(model.userFactors.first().features)  # 10 rank
    print(model.userFactors.count())  # 33729 userFactors
    print(model.itemFactors.first().features)  # 10 rank
    print(model.itemFactors.count())  # 17732 itemFactors