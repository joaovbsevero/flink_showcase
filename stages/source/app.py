from kafka import KafkaProducer
import json
import time

def main():
    producer = KafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # A small list of mock social media posts
    social_media_posts = [
        {"id": 1, "text": "Just had a great coffee!"},
        {"id": 2, "text": "Reading about AI trends"},
        {"id": 3, "text": "Sunny day at the beach"},
    ]

    # Produce messages to the 'raw_posts' topic
    for post in social_media_posts:
        producer.send("raw_posts", post)
        print(f"[SOURCE] Sent post with ID {post['id']}")
        time.sleep(1)  # small delay for demonstration

    producer.flush()
    print("[SOURCE] All messages sent. Going idle.")

    # Keep container alive (so it doesn't exit immediately)
    while True:
        time.sleep(10)

if __name__ == "__main__":
    time.sleep(20)
    main()
