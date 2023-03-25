class LogActivitiesException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class GetRecommendationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RecommendationTrainException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
