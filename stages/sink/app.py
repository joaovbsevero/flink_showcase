import json
import time

from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer(
        "enhancedPosts",
        bootstrap_servers="kafka:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="sinkConsumerGroup",
    )

    print("[SINK] Started listening to 'enhanced_posts'...")
    for message in consumer:
        post = message.value
        print(f"[SINK] Received Post ID={post['id']}")


if __name__ == "__main__":
    # Sleep to ensure topics/producers are ready
    time.sleep(10)
    main()
