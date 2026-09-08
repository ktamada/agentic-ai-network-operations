Place:
main.py -> app/main.py
kafka_consumer.py -> app/services/kafka_consumer.py
kafka_producer.py -> app/services/kafka_producer.py

.env:
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_INCIDENT_TOPIC=customer.incidents.inbound
KAFKA_CONSUMER_GROUP=agentic-ai-orchestrator

Install:
pip install aiokafka

Flow:
POST /incidents -> save NEW -> publish Kafka -> return NEW
Kafka consumer -> load incident by id -> SupervisorAgent -> save final state

Verify:
Kafka UI -> customer.incidents.inbound -> Messages
Prometheus:
sum by (topic,direction,result) (agentic_ai_kafka_messages_total)
