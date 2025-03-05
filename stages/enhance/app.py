import time
import json

from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    DeserializationSchema,
    FlinkKafkaConsumer,
    FlinkKafkaProducer,
    SerializationSchema,
)
from pyflink.datastream.execution_mode import RuntimeExecutionMode


# Custom JSON Deserialization Schema
class JSONDeserializationSchema(DeserializationSchema):
    def deserialize(self, message: bytes):
        return json.loads(message.decode("utf-8"))

    def is_end_of_stream(self, next_element):
        return False

    def get_produced_type(self):
        return Types.MAP(Types.STRING(), Types.STRING())


# Custom JSON Serialization Schema
class JSONSerializationSchema(SerializationSchema):
    def serialize(self, element) -> bytes:
        return json.dumps(element).encode("utf-8")


# Since the question states to mock the LLM and Google search, we’ll just do a placeholder function here.
def mock_enrich_text(post_text):
    # Pretend we used an LLM to figure out search topics, then "queried" them, returning fake data
    fake_topics = ["AI", "Coffee Beans", "Sunny Beaches"]
    return f"{post_text} [Enriched with topics: {', '.join(fake_topics)}]"


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    # Run in streaming mode
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)

    # Set parallelism to 1 for simplicity in a minimal example
    env.set_parallelism(1)

    # Create Kafka Consumer
    consumer = FlinkKafkaConsumer(
        topics="raw_posts",
        properties={
            "bootstrap.servers": "kafka:9092",
            "group.id": "flink_enhance_group",
        },
        deserialization_schema=JSONDeserializationSchema(),
    )

    # Create Kafka Producer
    producer = FlinkKafkaProducer(
        topic="enhanced_posts",
        producer_config={"bootstrap.servers": "kafka:9092"},
        serialization_schema=JSONSerializationSchema(),
    )

    # Create DataStream that receives data from Kafka
    ds = env.add_source(consumer)

    # Add enrichment stage to process received events
    ds.map(
        lambda post: {"id": post["id"], "text": mock_enrich_text(post["text"])},
        Types.MAP(Types.STRING(), Types.STRING()),
    )

    # Add sink that routes data to Kafka
    ds.add_sink(producer)

    # Execute
    env.execute("EnhanceFlinkJob")


if __name__ == "__main__":
    time.sleep(20)
    main()
