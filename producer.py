import uuid

from confluent_kafka import Producer
import time

if __name__ == "__main__":
    producer_conf = {
        "bootstrap.servers": "localhost:9093",

        # Настройки безопасности SSL
        "security.protocol": "SASL_PLAINTEXT",
        "ssl.ca.location": "ca.crt",  # Сертификат центра сертификации
        "ssl.certificate.location": "kafka-1-creds/kafka-1.crt",  # Сертификат клиента Kafka
        "ssl.key.location": "kafka-1-creds/kafka-1.key",  # Приватный ключ для клиента Kafka

        # Настройки SASL-аутентификации
        "sasl.mechanism": "PLAIN",  # Используемый механизм SASL (PLAIN)
        "sasl.username": "admin",  # Имя пользователя для аутентификации
        "sasl.password": "password",  # Пароль пользователя для аутентификации
    }

    producer = Producer(producer_conf)
    while True:
        key = f"key-{uuid.uuid4()}"
        value = "SASL/PLAIN"
        producer.produce(
            "sasl-plain-topic2",
            key=key,
            value=value,
        )
        producer.flush()
        print(f"Отправлено сообщение: {key=}, {value=}")
        time.sleep(1)
