import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer

from app.agents.supervisor import SupervisorAgent
from app.services.metrics import KAFKA_MESSAGES_TOTAL, AGENT_WORKFLOW_SECONDS, INCIDENTS_TOTAL
from app.services.store import get_incident, save_incident


class IncidentKafkaConsumer:
    def __init__(self):
        self.topic = os.getenv("KAFKA_INCIDENT_TOPIC", "customer.incidents.inbound")
        self.bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.group = os.getenv("KAFKA_CONSUMER_GROUP", "agentic-ai-orchestrator")
        self.consumer = None
        self.task = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap,
            group_id=self.group,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        await self.consumer.start()
        self.task = asyncio.create_task(self._loop())

    async def stop(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        if self.consumer:
            await self.consumer.stop()

    async def _loop(self):
        async for msg in self.consumer:
            try:
                payload = msg.value
                incident_id = payload.get("id")

                incident = await get_incident(incident_id) if incident_id else None
                if incident is None:
                    raise ValueError(f"Incident not found for Kafka event: {incident_id}")

                with AGENT_WORKFLOW_SECONDS.labels(source="kafka_consumer").time():
                    await SupervisorAgent().run(incident)

                await save_incident(incident)

                INCIDENTS_TOTAL.labels(
                    source="kafka",
                    status=incident.status.value,
                ).inc()

                KAFKA_MESSAGES_TOTAL.labels(
                    topic=self.topic,
                    direction="consumed",
                    result="success",
                ).inc()

                print(
                    f"[Kafka] consumed topic={msg.topic} partition={msg.partition} "
                    f"offset={msg.offset} incident={incident.id} "
                    f"status={incident.status.value}"
                )

            except Exception as exc:
                KAFKA_MESSAGES_TOTAL.labels(
                    topic=self.topic,
                    direction="consumed",
                    result="error",
                ).inc()
                print(f"[Kafka] processing failed: {exc!r}")


incident_kafka_consumer = IncidentKafkaConsumer()
