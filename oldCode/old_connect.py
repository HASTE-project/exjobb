#this coe snippet was used when connecting to Kafka in the tests "p", for each message the producer had to connect
# to Kafka, therefore not very effective and not used


def connect(message):
    kafka = KafkaClient("130.239.81.54:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'

    try:
        producer.send_messages(topic, message)
    except LeaderNotAvailableError:
        # https://github.com/mumrah/kafka-python/issues/249
        time.sleep(1)
        print_response(producer.send_messages(topic, message))

    kafka.close()
