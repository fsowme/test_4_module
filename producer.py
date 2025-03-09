import logging
import time
import uuid

from confluent_kafka import Producer

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    producer_conf = {
        "bootstrap.servers": "127.0.0.1:29092",

        # Настройки безопасности SSL
        "security.protocol": "sasl_ssl",
        "ssl.ca.location": "pem/ca-root.pem",  # Сертификат центра сертификации
        "ssl.certificate.location": "pem/client-certificate.pem",  # Сертификат клиента Kafka
        "ssl.key.location": "pem/client-private-key.pem",  # Приватный ключ для клиента Kafka

        # Настройки SASL-аутентификации
        "ssl.endpoint.identification.algorithm": "none",
        "sasl.mechanism": "PLAIN",  # Используемый механизм SASL (PLAIN)
        "sasl.username": "producer",  # Имя пользователя для аутентификации
        "sasl.password": "111111",  # Пароль пользователя для аутентификации
    }
    topics = ["topic-1", "topic-2"]
    producer = Producer(producer_conf)
    while True:
        for topic in topics:
            key = f"key-{uuid.uuid4()}"
            value = "SSL"
            producer.produce(
                topic,
                key=key,
                value=value,
            )
            producer.flush()
            logger.error("Отправлено сообщение: topic='%s' key='%s', value='%s'", topic, key, value)
            time.sleep(1)
