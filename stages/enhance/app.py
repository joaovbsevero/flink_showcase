import json
import time
from pathlib import Path

from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    DeliveryGuarantee,
    KafkaRecordSerializationSchema,
    KafkaSink,
    KafkaSource,
)
from pyflink.datastream.execution_mode import RuntimeExecutionMode


# Since the question states to mock the LLM and Google search, we’ll just do a placeholder function here.
def mock_enrich_text(post_text):
    # Pretend we used an LLM to figure out search topics, then "queried" them, returning fake data
    fake_topics = ["AI", "Coffee Beans", "Sunny Beaches"]
    return f"{post_text} [Enriched with topics: {', '.join(fake_topics)}]"


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    jar_path = Path(__file__).parent / "resources"
    env.add_jars(*[f"file://{p.absolute()}" for p in jar_path.glob("*.jar")])

    # Run in streaming mode
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)

    # Set parallelism to 1 for simplicity in a minimal example
    env.set_parallelism(8)

    # Create Kafka Consumer
    consumer = (
        KafkaSource.builder()
        .set_topics("rawPosts")
        .set_bootstrap_servers("kafka:9092")
        .set_group_id("flinkEnhanceGroup")
        .set_property("transaction.max.timeout.ms", "100")
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )

    # Create Kafka Producer
    producer = (
        KafkaSink.builder()
        .set_bootstrap_servers("kafka:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_value_serialization_schema(SimpleStringSchema())
            .set_topic("enhancedPosts")
            .build()
        )
        # .set_delivery_guarantee(DeliveryGuarantee.EXACTLY_ONCE)
        .set_property("transaction.max.timeout.ms", "100")
        .build()
    )

    # Create DataStream that receives data from Kafka
    ds = env.from_source(consumer, WatermarkStrategy.no_watermarks(), "EnhanceSource")

    def process(post):
        post = json.loads(post)
        post = {"id": str(post["id"]), "text": mock_enrich_text(post["text"])}
        return post

    # Add enrichment stage to process received events
    ds.map(
        process,
        Types.MAP(Types.STRING(), Types.STRING()),
    )

    # Add sink that routes data to Kafka
    ds.sink_to(producer)

    # Execute
    env.execute("EnhanceFlinkJob")


if __name__ == "__main__":
    time.sleep(15)
    main()
