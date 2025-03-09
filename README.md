# test_4_module


## Задание 1
```text
Не вижу смысла в перераспределении партиций с фактором репликации 3 и 3 нодами в кластере, нужно либо увеличивать 
количество брокеров, либо уменьшать фактор репликации. Создам с фактором репликации 3 и перераспределение уменьшу до 2
```

- Создание топика 8 партиций и фактор репликации 3 - [скрин](screenshots/1_topic_created.png)
  ```shell
  compose exec -it kafka-0 kafka-topics \
    --bootstrap-server localhost:9092 \
    --topic test-topic \
    --create \
    --partitions 8 \
    --replication-factor 3
  ```
  
- Вывести информацию о распределении партиций по брокерам - [скрин](screenshots/2_status.png)
  ```shell
   compose exec -it kafka-0 kafka-topics \
    --bootstrap-server localhost:9092 \
    --describe \
    --topic test-topic
  ```
  <details>
  <summary>Статус партиций</summary>
  
  ***Партиции распределены по 3 брокерам и все в синхронизированном состоянии***
  <pre>
  Topic: test-topic       TopicId: GsM6RoCmTWuNwTDSSoqg4w PartitionCount: 8       ReplicationFactor: 3    Configs: 
        Topic: test-topic       Partition: 0    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
        Topic: test-topic       Partition: 1    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1
        Topic: test-topic       Partition: 2    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2
        Topic: test-topic       Partition: 3    Leader: 2       Replicas: 2,1,0 Isr: 2,1,0
        Topic: test-topic       Partition: 4    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2
        Topic: test-topic       Partition: 5    Leader: 0       Replicas: 0,2,1 Isr: 0,2,1
        Topic: test-topic       Partition: 6    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2
        Topic: test-topic       Partition: 7    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0
  </pre>
  </details>


- [Файл](reassignment.json) для перераспределения партиций по брокерам
- Копирование файла в контейнер docker
  ```shell
  compose cp ./reassignment.json kafka-0:/tmp/reassignment.json
  ```
- Подготовка плана переназначения - [скрин](screenshots/3_plan_generated.png)
  ```shell
  compose exec -it kafka-0 kafka-reassign-partitions.sh \
    --bootstrap-server localhost:9092 \
    --broker-list "0,1,2" \
    --topics-to-move-json-file "/tmp/reassignment.json" \
    --generate
  ```
  <details>
  <summary>Вывод в консоль</summary>
  
  <pre>
  Current partition replica assignment
  {"version":1,"partitions":[]}

  Proposed partition reassignment configuration
  {"version":1,"partitions":[]}
  </pre>
  </details>


- Запуск плана перераспределения - [скрин](screenshots/4_reassignment_executed.png)
  ```shell
  compose exec -it kafka-0 kafka-reassign-partitions.sh \
    --bootstrap-server localhost:9092 \
    --reassignment-json-file "/tmp/reassignment.json" \
    --execute
  ```
  <details>
  <summary>Вывод в консоль</summary>

  <pre>
  Current partition replica assignment

  {"version":1,"partitions":[{"topic":"test-topic","partition":0,"replicas":[1,2,0],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":1,"replicas":[2,0,1],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":2,"replicas":[0,1,2],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":3,"replicas":[2,1,0],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":4,"replicas":[1,0,2],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":5,"replicas":[0,2,1],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":6,"replicas":[0,1,2],"log_dirs":["any","any","any"]},{"topic":"test-topic","partition":7,"replicas":[1,2,0],"log_dirs":["any","any","any"]}]}
  
  Save this to use as the --reassignment-json-file option during rollback
  Successfully started partition reassignments for test-topic-0,test-topic-1,test-topic-2,test-topic-3,test-topic-4,test-topic-5,test-topic-6,test-topic-7
  </pre>
  </details>


- Проверка перераспределения - [скрин](screenshots/5_status.png)
  ```shell
  compose exec -it kafka-0 kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --describe \
    --topic test-topic
  ```
  <details>
  <summary>Статус партиций</summary>
  
  ***Реплики остались только на двух нодах, тк мы принудительно оставили по 2 ноды в плане, синхронизированное состояние
  только на двух брокерах***
  <pre>
  Topic: test-topic       TopicId: GsM6RoCmTWuNwTDSSoqg4w PartitionCount: 8       ReplicationFactor: 2    Configs: 
        Topic: test-topic       Partition: 0    Leader: 0       Replicas: 0,2   Isr: 2,0
        Topic: test-topic       Partition: 1    Leader: 0       Replicas: 0,1   Isr: 0,1
        Topic: test-topic       Partition: 2    Leader: 1       Replicas: 1,2   Isr: 1,2
        Topic: test-topic       Partition: 3    Leader: 0       Replicas: 0,1   Isr: 1,0
        Topic: test-topic       Partition: 4    Leader: 0       Replicas: 0,2   Isr: 0,2
        Topic: test-topic       Partition: 5    Leader: 1       Replicas: 1,2   Isr: 2,1
        Topic: test-topic       Partition: 6    Leader: 1       Replicas: 1,2   Isr: 1,2
        Topic: test-topic       Partition: 7    Leader: 1       Replicas: 1,2   Isr: 1,2
  </pre>
  </details>


- Остановим kafka-1
  ```shell
  compose stop kafka-1
  ```

- Проверим состояние - [скрин](screenshots/6_status.png)
  ```shell
  compose exec -it kafka-0 kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --describe \
    --topic test-topic
  ```
  <details>
  <summary>Статус партиций</summary>
  
  ***После падения 1 ноды ожидаемо синхронизированное состояние осталось только на одном брокере из двух у тех партиций,
  которые были распределены на упавшую ноду***
  <pre>
  Topic: test-topic       TopicId: GsM6RoCmTWuNwTDSSoqg4w PartitionCount: 8       ReplicationFactor: 2    Configs: 
        Topic: test-topic       Partition: 0    Leader: 0       Replicas: 0,2   Isr: 2,0
        Topic: test-topic       Partition: 1    Leader: 0       Replicas: 0,1   Isr: 0
        Topic: test-topic       Partition: 2    Leader: 2       Replicas: 1,2   Isr: 2
        Topic: test-topic       Partition: 3    Leader: 0       Replicas: 0,1   Isr: 0
        Topic: test-topic       Partition: 4    Leader: 0       Replicas: 0,2   Isr: 0,2
        Topic: test-topic       Partition: 5    Leader: 2       Replicas: 1,2   Isr: 2
        Topic: test-topic       Partition: 6    Leader: 2       Replicas: 1,2   Isr: 2
        Topic: test-topic       Partition: 7    Leader: 2       Replicas: 1,2   Isr: 2
  </pre>
  </details>


- Восстановим kafka-1
  ```shell
  compose start kafka-1
  ```
- Проверим состояние - [скрин](screenshots/7_status.png)
  ```shell
  compose exec -it kafka-0 kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --describe \
    --topic test-topic
  ```
  <details>
  <summary>Статус партиций</summary>
  
  ***Синхронизированное состояние вернулось в норму, с учетом ручного перераспределения. Для возвращения синхронизации
  по всем нодам следует в плане в ключе "replicas" указать 3 ноды***
  <pre>
  Topic: test-topic       TopicId: GsM6RoCmTWuNwTDSSoqg4w PartitionCount: 8       ReplicationFactor: 2    Configs: 
        Topic: test-topic       Partition: 0    Leader: 0       Replicas: 0,2   Isr: 2,0
        Topic: test-topic       Partition: 1    Leader: 0       Replicas: 0,1   Isr: 0,1
        Topic: test-topic       Partition: 2    Leader: 2       Replicas: 1,2   Isr: 2,1
        Topic: test-topic       Partition: 3    Leader: 0       Replicas: 0,1   Isr: 0,1
        Topic: test-topic       Partition: 4    Leader: 0       Replicas: 0,2   Isr: 0,2
        Topic: test-topic       Partition: 5    Leader: 2       Replicas: 1,2   Isr: 2,1
        Topic: test-topic       Partition: 6    Leader: 2       Replicas: 1,2   Isr: 2,1
        Topic: test-topic       Partition: 7    Leader: 2       Replicas: 1,2   Isr: 2,1
  </pre>
  </details>


## Задание 2
- Создание топиков
  ```shell
  compose exec -it kafka-0 kafka-topics.sh \
    --bootstrap-server kafka-0:9091 \
    --create \
    --topic topic-1 \
    --partitions 3 \
    --replication-factor 2 \
    --command-config /home/admin.properties
  ```
  ```shell
  compose exec -it kafka-0 kafka-topics.sh \
    --bootstrap-server kafka-0:9091 \
    --create --topic topic-2 \
    --partitions 3 \
    --replication-factor 2 \
    --command-config /home/admin.properties
  ```


- Выдача прав
  ```shell
  compose exec -it kafka-0 kafka-acls.sh \
    --bootstrap-server kafka-0:9091 \
    --add \
    --allow-principal User:consumer \
    --operation Read \
    --topic topic-1 \
    --group consumer-ssl-group \
    --command-config /home/admin.properties
  ```
  ```shell
  compose exec -it kafka-0 kafka-acls.sh \
    --bootstrap-server kafka-0:9091 \
    --add \
    --allow-principal User:producer \
    --operation Write \
    --topic topic-1 \
    --command-config /home/admin.properties
  ```
  ```shell
  compose exec -it kafka-0 kafka-acls.sh \
    --bootstrap-server kafka-0:9091 \
    --add \
    --allow-principal User:producer \
    --operation Write \
    --topic topic-2 \
    --command-config /home/admin.properties
  ```


- Проверка
  - Продюсер
    ```shell
    python producer.py
    ```
    <details>
    <summary>Вывод в консоль</summary>
  
    ***будет писать в топики по очереди***
    <pre>
    Отправлено сообщение: topic='topic-1' key='key-531c2def-c5b3-4e42-b971-46eb79627484', value='SSL'
    Отправлено сообщение: topic='topic-2' key='key-d0c7923d-2877-4ddd-b005-b7f58aed3fa3', value='SSL'
    </pre>
    </details>
  
  - Консьюмер
    ```shell
    python consumer.py
    ```
    
    <details>
    <summary>Вывод в консоль</summary>
  
    ***попытается подписаться на обе топика, но сможет только на topic-1***
    <pre>
    Ошибка: KafkaError{code=TOPIC_AUTHORIZATION_FAILED,val=29,str="Subscribed topic not available: topic-2: Broker: Topic authorization failed"}
    Получено сообщение: key='key-cdf247f9-4cab-41ab-a0de-366aaf6c9a63', value='SSL', offset=6
    Получено сообщение: key='key-7093824e-74c5-4881-bd43-a6bb63f44264', value='SSL', offset=7

    </pre>
    </details>
