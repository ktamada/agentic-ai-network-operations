# Kafka topics

Run after `docker compose up -d`:

```powershell
docker exec agentic-kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic customer.incidents.inbound --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec agentic-kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic agent.incidents.completed --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec agentic-kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic network.change.events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec agentic-kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic customer.incidents.retry --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec agentic-kafka /opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic customer.incidents.dlq --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
