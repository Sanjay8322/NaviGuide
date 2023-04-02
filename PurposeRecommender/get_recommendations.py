from PurposeRecommender.ExtractData import ExtractData
from PurposeRecommender.transform_purpose_id import purposes_list

from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession

from core.exceptions.app_exceptions import GetRecommendationException


def get_recommendations(user_id):
    try:
        spark = SparkSession\
                .builder\
                .appName("PurposeRecommender")\
                .getOrCreate()

        model = ALSModel.load("PurposeRecommender/trained_als_model")

        all_user_recs = model.recommendForAllUsers(3)

        all_user_recs.collect()

        user_recs = all_user_recs.filter(all_user_recs['userId'] == user_id).collect()

        ed = ExtractData()
        ed.loadData()
        recommendations = []
        for row in user_recs:    
            for rec in row.recommendations:
                recommendations.append(ed.getpurposeName(purposes_list[rec.purposeId]))

        spark.stop()

        return recommendations
    except Exception as e:
        raise GetRecommendationException(str(e))
