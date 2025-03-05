import logging

from confluent_kafka import Consumer

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    consumer_conf = {
        "bootstrap.servers": "kafka-1:9093",
        "group.id": "consumer-ssl-group",
        "auto.offset.reset": "earliest",

        # "security.protocol": "SASL_PLAINTEXT",
        "security.protocol": "SSL",
        "ssl.ca.location": "certs/ca.crt",  # Сертификат центра сертификации
        "ssl.certificate.location": "certs/kafka-client.crt",  # Сертификат клиента Kafka
        "ssl.key.location": "certs/kafka-client.key",  # Приватный ключ для клиента Kafka


        # "sasl.mechanism": "PLAIN",
        # "sasl.username": "admin",  # Имя пользователя для аутентификации
        # "sasl.password": "password",  # Пароль пользователя для аутентификации
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(["ssl-topic1"])

    try:
        while True:
            message = consumer.poll(1)

            if message is None:
                continue
            if message.error():
                print(f"Ошибка: {message.error()}")
                continue

            key = message.key().decode("utf-8")
            value = message.value().decode("utf-8")
            logger.info("Получено сообщение: key='%s', value='%s', offset=%s", key, value, message.offset())
    finally:
        consumer.close()
