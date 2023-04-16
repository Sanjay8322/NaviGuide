from confluent_kafka import Producer
import json
from celery import Celery

celery = Celery('naviguide',
        broker='redis://localhost:6379',
        backend='redis://',
        include=['PurposeRecommender.Data_Injestion.producer', 'chatbot.utils'])

@celery.task
def produce_to_topic(topic_name, datas):
        # Set up the Kafka producer configuration
        conf = {'bootstrap.servers': 'localhost:9092',
                'client.id': 'python-producer',
                'batch.size': 1000}

        # Create a Kafka producer instance
        producer_instance = Producer(conf)
        
        for data in datas:
                # Convert the data to bytes
                data_bytes = json.dumps(data)

                # Push the data to the Kafka topic
                producer_instance.produce(topic_name, value=data_bytes)

        # Flush any outstanding messages in the producer buffer
        producer_instance.flush()

        # Close the Kafka producer instance
        # producer.close()


if __name__ == '__main__':

    datas = [
                {
                "Userid": 2,
                "Purposeid": "east kore",
                "Visit-frequency": 1
        }
        ]
    topic_name = 'user_activities'
    produce_to_topic(topic_name, datas)

