# /// script
# dependencies = [
#   "confluent-kafka",
# ]
# ///


from confluent_kafka import Consumer, KafkaError

# Configuration for the Consumer
conf = {
    "bootstrap.servers": "a8e72c2937e304e3986bb09de8dd450b-405726189.us-east-1.elb.amazonaws.com:9094",
    "group.id": "order-consumers",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe(["orders"])  # Consumes from the 'orders' topic

try:
    print("Waiting for messages... Press Ctrl+C to stop.")
    while True:
        msg = consumer.poll(1.0)  # Timeout of 1 second
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Observe how messages are distributed among partitions
        print(
            f"Key: {msg.key().decode('utf-8')} | "
            f"Partition: {msg.partition()} | "
            f"Value: {msg.value().decode('utf-8')}"
        )

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
