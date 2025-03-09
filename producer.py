import logging
import time
import uuid

from confluent_kafka import Producer

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    producer_conf = {
        "bootstrap.servers": "kafka-1:9093",

        # Настройки безопасности SSL
        "security.protocol": "SSL",
        "ssl.ca.location": "certs/ca.crt",  # Сертификат центра сертификации
        "ssl.certificate.location": "certs/kafka-1.crt",  # Сертификат клиента Kafka
        "ssl.key.location": "certs/kafka-1.key",  # Приватный ключ для клиента Kafka

        # Настройки SASL-аутентификации
        # "sasl.mechanism": "PLAIN",  # Используемый механизм SASL (PLAIN)
        # "sasl.username": "admin",  # Имя пользователя для аутентификации
        # "sasl.password": "password",  # Пароль пользователя для аутентификации
    }

    producer = Producer(producer_conf)
    while True:
        key = f"key-{uuid.uuid4()}"
        value = "SSL"
        producer.produce(
            "ssl-topic1",
            key=key,
            value=value,
        )
        producer.flush()
        logger.info("Отправлено сообщение: key='%s', value='%s'", key, value)
        time.sleep(1)
