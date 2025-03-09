import logging

from confluent_kafka import Consumer

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    # producer_conf = {
    #         "bootstrap.servers": "127.0.0.1:29092",
    #
    #         # Настройки безопасности SSL
    #         "security.protocol": "sasl_ssl",
    #         "ssl.ca.location": "pem/ca-root.pem",  # Сертификат центра сертификации
    #         "ssl.certificate.location": "pem/client-certificate.pem",  # Сертификат клиента Kafka
    #         "ssl.key.location": "pem/client-private-key.pem",  # Приватный ключ для клиента Kafka
    #
    #         # Настройки SASL-аутентификации
    #         "ssl.endpoint.identification.algorithm": "none",
    #         "sasl.mechanism": "PLAIN",  # Используемый механизм SASL (PLAIN)
    #         "sasl.username": "producer",  # Имя пользователя для аутентификации
    #         "sasl.password": "111111",  # Пароль пользователя для аутентификации
    #     }
    consumer_conf = {
        "bootstrap.servers": "127.0.0.1:29092",
        "group.id": "consumer-ssl-group",
        "auto.offset.reset": "earliest",

        # "security.protocol": "SASL_PLAINTEXT",
        "security.protocol": "sasl_ssl",
        "ssl.ca.location": "pem/ca-root.pem",  # Сертификат центра сертификации
        "ssl.certificate.location": "pem/client-certificate.pem",  # Сертификат клиента Kafka
        "ssl.key.location": "pem/client-private-key.pem",  # Приватный ключ для клиента Kafka

        "ssl.endpoint.identification.algorithm": "none",
        "sasl.mechanism": "PLAIN",
        "sasl.username": "consumer",  # Имя пользователя для аутентификации
        "sasl.password": "222222",  # Пароль пользователя для аутентификации
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(["topic-1", "topic-2"])

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
            logger.error("Получено сообщение: key='%s', value='%s', offset=%s", key, value, message.offset())
    finally:
        consumer.close()
