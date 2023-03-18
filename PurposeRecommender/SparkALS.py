from pyspark.sql import SparkSession

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row

from PurposeRecommender.ExtractData import ExtractData
from PurposeRecommender.transform_purpose_id import purposes_list

from core.exceptions.app_exceptions import RecommendationException



def get_recommendations(user_id):
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

        als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="purposeId", ratingCol="rating",
                coldStartStrategy="drop")
        model = als.fit(training)

        predictions = model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                        predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        print("Root-mean-square error = " + str(rmse))

        userRecs = model.recommendForAllUsers(3)

        testUserRecs = userRecs.filter(userRecs['userId'] == user_id).collect()

        spark.stop()

        ed = ExtractData()
        ed.loadData()
        recommendations = []
        for row in testUserRecs:    
            for rec in row.recommendations:
                recommendations.append(ed.getpurposeName(purposes_list[rec.purposeId]))

        return recommendations

    except Exception as e:
        raise RecommendationException('Error while creating recommendations')
