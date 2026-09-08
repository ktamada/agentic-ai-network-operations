import json
import os

from aiokafka import AIOKafkaProducer
from app.services.metrics import KAFKA_MESSAGES_TOTAL


class KafkaProducerService:
    def __init__(self):
        self.topic = os.getenv("KAFKA_INCIDENT_TOPIC", "customer.incidents.inbound")
        self.bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = None

    async def start(self):
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap,
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            )
            await self.producer.start()

    async def stop(self):
        if self.producer is not None:
            await self.producer.stop()
            self.producer = None

    async def publish_incident(self, payload: dict):
        if self.producer is None:
            await self.start()

        try:
            metadata = await self.producer.send_and_wait(self.topic, payload)
            KAFKA_MESSAGES_TOTAL.labels(
                topic=self.topic,
                direction="published",
                result="success",
            ).inc()
            print(
                f"[Kafka] published topic={metadata.topic} "
                f"partition={metadata.partition} offset={metadata.offset}"
            )
            return metadata
        except Exception:
            KAFKA_MESSAGES_TOTAL.labels(
                topic=self.topic,
                direction="published",
                result="error",
            ).inc()
            raise


kafka_producer = KafkaProducerService()
