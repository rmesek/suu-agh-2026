# /// script
# dependencies = [
#   "requests",
#   "rich",
#   "confluent-kafka",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])

from confluent_kafka import Producer
import random
import json

# Configuration for the Producer
conf = {
    "bootstrap.servers": "a8e72c2937e304e3986bb09de8dd450b-405726189.us-east-1.elb.amazonaws.com:9094",
    "client.id": "python-producer",
}

producer = Producer(conf)
topic = "orders"

# List of people who can make an order
people = [
    {"id": "user_1", "name": "Alice"},
    {"id": "user_2", "name": "Bob"},
    {"id": "user_3", "name": "Charlie"},
    {"id": "user_4", "name": "Diana"},
]


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(
            f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


# Generate random orders for each person
for person in people:
    num_orders = random.randint(1, 5)
    for i in range(num_orders):
        order_data = {
            "order_id": random.randint(1000, 9999),
            "user": person["name"],
            "item": random.choice(["Laptop", "Mouse", "Keyboard", "Monitor"]),
        }

        # Produce the order using the Person ID as the KEY
        producer.produce(
            topic,
            key=person["id"],
            value=json.dumps(order_data),
            callback=delivery_report,
        )

producer.flush()  # Wait for all messages to be delivered
