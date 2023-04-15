import json
from confluent_kafka import Consumer, KafkaError
import csv

from csv_handler import process_csv
from SparkALS import train_recommendations

def consumer():
    # Set up the Kafka consumer configuration
    print('Starting consumer...')
    conf = {'bootstrap.servers': 'localhost:9092',
            'group.id': 'rec-sys-group',
            'auto.offset.reset': 'latest'}

    # Create a Kafka consumer instance
    consumer = Consumer(conf)

    # Subscribe to the Kafka topic from which you want to read data
    topic_name = 'user_activities'
    consumer.subscribe([topic_name])

    print(f'Subscribed to topic {topic_name}')
    print("Starting to consume data...")
    data_counter = 0
    # Continuously poll for new messages in the Kafka topic and write them to the CSV file
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                    .format(msg.topic(), msg.partition()))
            else:
                print('Error while consuming message: {0}'.format(msg.error()))
        else:
            print('Received message: {0}'.format(msg.value().decode('utf-8')))

            activity = msg.value().decode('utf-8')
            activity = json.loads(msg.value())

            # Write the message key and value to the CSV file
            process_csv(activity)
        data_counter+=1

        if data_counter>=100:
            # train_recommendations()
            data_counter=0
            print('Training recommendation engine with new dataset...')
            res = train_recommendations()
            if res:
                print('Training done')
            else:
                print('Error while training')

 
    # Close the Kafka consumer instance when finished

    consumer.close()

if __name__ == '__main__':
    consumer()
