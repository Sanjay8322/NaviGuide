from operator import mod
from pyspark.sql import SparkSession

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row

from PurposeRecommender.transform_purpose_id import purposes_list

from core.exceptions.app_exceptions import RecommendationTrainException


def train_recommendations():
    try:
        spark = SparkSession\
            .builder\
            .appName("PurposeRecommender")\
            .getOrCreate()

        lines = spark.read.option("header", "true").csv(
            "PurposeRecommender/training-data/mapping_dataset.csv").rdd

        dataRDD = lines.map(lambda p: Row(userId=int(p[0]), purposeId=purposes_list.index(p[1]),
                                            rating=float(p[2])/20))

        data = spark.createDataFrame(dataRDD)

        (training, test) = data.randomSplit([0.8, 0.2])

        # TODO change this to an incremental model with seed param
        als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="purposeId", ratingCol="rating",
                coldStartStrategy="drop")
        model = als.fit(training)

        # Save ALS model
        model.write().overwrite().save("PurposeRecommender/trained_als_model")
        spark.stop()

        # Measuring accuracy
        # predictions = model.transform(test)
        # evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
        #                                 predictionCol="prediction")
        # rmse = evaluator.evaluate(predictions)
        # print("Root-mean-square error = " + str(rmse))
    except Exception as e:
        raise RecommendationTrainException(str(e))

if __name__ == '__main__':
    train_recommendations()
