Spark, Hadoop y Kafka están configurados en el clúster de las máquinas de IaaS.

Version Spark:

- spark-shell --version 

    version 3.2.0

Version Java:

openjdk version "11.0.23" 2024-04-16
OpenJDK Runtime Environment (build 11.0.23+9-post-Ubuntu-1ubuntu120.04.2)
OpenJDK 64-Bit Server VM (build 11.0.23+9-post-Ubuntu-1ubuntu120.04.2, mixed mode, sharing)

Version HAdoop:
- hadoop version

    Hadoop 3.3.6
    Source code repository https://github.com/apache/hadoop.git -r 1be78238728da9266a4f88195058f08fd012bf9c
    Compiled by ubuntu on 2023-06-18T08:22Z
    Compiled on platform linux-x86_64
    Compiled with protoc 3.7.1
    From source with checksum 5652179ad55f76cb287d9c633bb53bbd
    This command was run using /opt/hadoop/share/hadoop/common/hadoop-common-3.3.6.jar

Version Kafka:



Ejecucion proyecto:

- iniciar zookeper: bin/zookeeper-server-start.sh config/zookeeper.properties

- iniciar kafka: bin/kafka-server-start.sh config/server.properties

- inicar api: python3 api_simulation.py

- iniciar kafka producer: python3 ./scripts/kafka_producer.py

- ejecutar proyecto: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 spark_consumer.py

python3 app.py
