# coding:utf-8
from time import time
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from movie_recommend.load_data import create_spark
from movie_recommend.clean_data import screening_ratings
import pandas as pd
import matplotlib.pyplot as plt

spark = create_spark()
evaluator = RegressionEvaluator(labelCol='rating')


def comput_rmse(model, train_data):
    prediction = model.transform(train_data)
    rmse = evaluator.evaluate(prediction)
    print('RMSE:', rmse)
    return rmse


def train_model(train_data, rank=10, max_iter=10, reg_param=0.1):
    '''
    使用不同的参数训练模型
    :param train_data: 训练数据数据集DataFrame
    :param rank: 模型隐因子
    :param max_iter: 模型迭代次数
    :param reg_param: 模型正则项参数
    :return: 训练时长，RMSE结果，参数rank, max_iter, reg_param, 训练好的模型
    '''
    start_time = time()
    print('<参数：', rank, max_iter, reg_param, '>')
    als = ALS(rank=rank, maxIter=max_iter, regParam=reg_param)
    model = als.fit(train_data)
    end_time = time()
    duration = end_time - start_time
    print('用时', duration)
    rmse = comput_rmse(model, train_data)
    return duration, rmse, rank, max_iter, reg_param, model


def visible_metrics(metrics, x_label, y1_label, y2_label, x_data, y_min=0, y_max=1):
    """
    :param metrics: 模型误差结果列表
    :param x_label: X轴标签
    :param y1_label: Y轴RMSE标签
    :param y2_label: Y轴时长标签
    :param x_data: X轴数据
    :param y_min: Y轴最小值
    :param y_max: Y轴最大值
    :return: None
    """
    print('开始绘图')
    df = pd.DataFrame(metrics, index=x_data, columns=['duration', 'RMSE', 'rank', 'iterations', 'reg_param', 'model'])
    print(df)
    ax = df[y1_label].plot(kind='bar', title='RMSE vs Duration', figsize=(10, 6), legend=True, fontsize=12)
    ax.set_ylabel(y1_label, fontsize=12)
    ax.set_ylim([y_min, y_max])
    ax.set_xlabel(x_label, fontsize=12)
    # 两组数据共用X轴
    ax2 = ax.twinx()
    # 使用拆线表示时长
    ax2.plot(df[y2_label].values, '-or', linewidth=2)
    ax2.set_ylabel(y2_label, fontsize=12)
    plt.show()


def run_train_model(train_data, rank_list, iter_list, reg_param_list, param_name=None):
    '''
    以不同的参数调用train_model，获得在不同参数下，模型训练耗时，rmse误差，从中选择最优参数
    :return: 所有训练函数结果
    '''
    metrics = [
        train_model(train_data, rank, max_iter, reg_param)
        for rank in rank_list
        for max_iter in iter_list
        for reg_param in reg_param_list
    ]
    if param_name is not None:
        # 图表绘制, 三张图表，
        # 每张图表的横坐标分别是rank_list, iter_list, reg_param_list值
        param_dicts = {'rank': rank_list, 'max_iter': iter_list, 'reg_param': reg_param_list}
        visible_metrics(metrics, param_name, 'RMSE', 'duration', param_dicts[param_name])
    else:
        return metrics


def get_best_model():
    rank_list = [20, 30, 40, 50]
    max_iter_list = [15, 18, 20]
    reg_param_list = [0.1]
    rank_list = [20, 50]
    max_iter_list = [20]
    reg_param_list = [0.1]
    metrics = run_train_model(train_data, rank_list, max_iter_list, reg_param_list)
    best_params = sorted(metrics, key=lambda x: -x[0])
    best_params = best_params[0]
    print('模型性能：')
    print('duration', best_params[0])
    print('RMSE', best_params[1])
    print('调整后最佳参数：')
    print('rank', best_params[2])
    print('max_iter:', best_params[3])
    print('reg_param:', best_params[4])
    return best_params[5]  # best_model


if __name__ == '__main__':
    train_data = screening_ratings()
    # 训练参数, 调整rank值
    # rank_list = [5, 10, 15, 20, 50, 100]
    # max_iter_list = [10]
    # reg_param_list = [0.1]
    # run_train_model(train_data, rank_list, max_iter_list, reg_param_list, "rank")
    # 20-50 较佳

    # 训练参数, 调整max_iter值
    # rank_list = [10]
    # max_iter_list = [25]
    # reg_param_list = [0.1]
    # run_train_model(train_data, rank_list, max_iter_list, reg_param_list, "max_iter")
    # 无法训练4个值，或无法算到25，20较佳

    # 训练参数, 调整reg_param值
    # rank_list = [10]
    # max_iter_list = [8]
    # reg_param_list = [0.1, 0.3, 0.6, 0.9, 1.0]
    # run_train_model(train_data, rank_list, max_iter_list, reg_param_list, "reg_param")
    # 0.1较佳
    if spark.sparkContext.master=="yarn":
        # yarn 模式运行时，模型保存路径为hadoop文件系统
        path = "hdfs://192.168.3.180:9000/user/root/data/my_best_model"
    else:
        path = 'file:///Projects/python_projects/movie_recommendation/model/best_als_model'
    model = get_best_model()
    model.save(path)
    # 50, 20, 0.1