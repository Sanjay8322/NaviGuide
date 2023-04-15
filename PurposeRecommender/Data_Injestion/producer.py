from confluent_kafka import Producer
import json

def produce(topic_name, datas):
        # Set up the Kafka producer configuration
        conf = {'bootstrap.servers': 'localhost:9092',
                'client.id': 'python-producer'}

        # Create a Kafka producer instance
        producer = Producer(conf)

        for data in datas:
                # Convert the data to bytes
                data_bytes = json.dumps(data)

                # Push the data to the Kafka topic
                producer.produce(topic_name, value=data_bytes)

        # Flush any outstanding messages in the producer buffer
        producer.flush()

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
    produce(topic_name, datas)

