import imp
from pyspark.sql import SparkSession

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row

from ExtractData import ExtractData

from transform_purpose_id import purposes_list


if __name__ == "__main__":
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

    userRecs = model.recommendForAllUsers(10)

    testUserRecs = userRecs.filter(userRecs['userId'] == 3).collect()

    spark.stop()

    ed = ExtractData()
    ed.loadData()

    for row in testUserRecs:    
        for rec in row.recommendations:
            print(ed.getpurposeName(purposes_list[rec.purposeId]))

