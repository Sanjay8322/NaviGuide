import csv
from PurposeRecommender.transform_purpose_id import purposes_list
from core.exceptions.app_exceptions import LogActivitiesException

def log_activities(tag, intent):
    try:
        activities = intent.get('activity_tags')
        if activities is None:
            return
        csv_path = 'PurposeRecommender/training-data/mapping_dataset.csv'
        user_id=1
        append_to_csv(csv_path, user_id, activities)
    except Exception as e:
        raise LogActivitiesException('Error during logging activities')


def append_to_csv(csv_path, user_id, activities):
    try:
        fieldnames = ['Userid', 'Purposeid', 'Visit-frequency']
        with open(csv_path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            for activity in activities:
                row = {
                    "Userid": user_id,
                    "Purposeid": activity,
                    "Visit-frequency": 1
                }
                writer.writerow(row)
    except:
        raise LogActivitiesException('Error during appending activities to CSV')

