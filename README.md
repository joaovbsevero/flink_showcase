# Minimal Streaming Pipeline with Docker, Kafka & PyFlink

This repository contains a simple streaming pipeline with three distinct stages (Source, Enhance, Sink) running in separate Docker containers, connected by Kafka. The pipeline demonstrates how to:

1. **Source**: Produce a list of social media posts.
2. **Enhance**: Apply a PyFlink job that mocks an LLM-based data enrichment.
3. **Sink**: Consume and print the IDs of the processed messages.

---

## Architecture

The entire pipeline is orchestrated by **Docker Compose**:

1. **Zookeeper** & **Kafka** (for message brokering)
2. **Source** container (produces messages to Kafka)
3. **Enhance** container (consumes messages, applies transformations, writes enriched data to Kafka)
4. **Sink** container (consumes final messages and prints the IDs)

Communication flows:

```
[ Source ] -- raw_posts --> [ Enhance (PyFlink) ] -- enhanced_posts --> [ Sink ]
```

---

## Contents

-   `docker-compose.yml` – Orchestrates all services with Docker Compose.
-   `stages/`
        `source/` – Source container files.
        -   `Dockerfile`
        -   `requirements.txt`
        -   `app.py` – Produces messages.
    -   `enhance/` – Flink-based "Enhance" container files.
        -   `Dockerfile`
        -   `requirements.txt`
        -   `app.py` – Consumes, enriches, and re-sends messages.
    -   `sink/` – Sink container files.
        -   `Dockerfile`
        -   `requirements.txt`
        -   `app.py` – Consumes final messages.

---

## Prerequisites

-   **Docker**
-   **Docker Compose**

---

## Installation & Usage

1. **Clone** the repository:

    ```bash
    git clone <REPO_URL>
    cd <REPO_FOLDER>
    ```

2. **Build** and **start** services:

    ```bash
    docker-compose up --build
    ```

    - This starts containers for Zookeeper, Kafka, the Source, the Enhance (PyFlink), and the Sink.
    - By default, the Source produces a small list of social media posts to the `raw_posts` Kafka topic.
    - The Enhance container (Flink) reads from `raw_posts`, enriches the posts, and writes them to `enhanced_posts`.
    - The Sink container then reads from `enhanced_posts` and prints the ID of each post.

3. **Watch logs**:

    - You should see output from the Source about sending messages.
    - You should see the Sink print out lines like: `"[SINK] Received Post ID=1"`.

4. **Shutdown**:
    ```bash
    docker-compose down
    ```

---

## Customization

-   **Add more Source data**: Modify [`source`](stages/source/app.py) to produce different or larger sets of posts.
-   **Change Flink job**: Edit [`enhance`](stages/enhance/app.py) to apply more complex transformations or actual external lookups.
-   **Sink stage**: Extend [`sink`](stages/sink/app.py) to store or process data further.
-   **Scaling**: Adjust Docker Compose to increase parallelism or replicate containers.

---

## Performance Measurement

To assess performance:

-   **Latency**: Measure the time a single message takes to go from Source → Enhance → Sink.
-   **Throughput**: Measure how many messages/second the system processes.
-   **Efficiency**: Check CPU/memory usage vs. throughput.

You can run multiple Source containers or alter Flink's parallelism to see how the pipeline handles higher loads.

---

## License

[MIT License](LICENSE).

---
