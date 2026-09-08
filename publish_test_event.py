import asyncio
import json
import os
from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv

load_dotenv()


async def main():
    producer = AIOKafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )
    await producer.start()
    try:
        await producer.send_and_wait(
            os.getenv("KAFKA_INCIDENT_TOPIC", "customer.incidents.inbound"),
            {
                "customer_id": "CUST-1001",
                "message": "Kafka event: my internet is slow and my bill is higher this month.",
            },
        )
        print("Kafka test event published.")
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
