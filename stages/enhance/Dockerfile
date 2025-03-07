FROM python:3.8

# Install Java
RUN apt-get update && \
    apt-get install -y default-jre-headless && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY resources/flink-connector-kafka.jar /usr/local/lib/python3.8/site-packages/pyflink/lib
COPY resources/kafka-clients.jar /usr/local/lib/python3.8/site-packages/pyflink/lib

COPY app.py .

CMD ["python", "app.py"]
