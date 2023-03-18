import csv
from PurposeRecommender.transform_purpose_id import purposes_list

def process_activities(tag, intent):
    activities = intent.get('activity_tags')
    csv_path = 'PurposeRecommender/training-data/mapping_dataset.csv'
    user_id=1
    append_to_csv(csv_path, user_id, activities)


def append_to_csv(csv_path, user_id, activities):
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

