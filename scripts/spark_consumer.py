from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Crear una sesión de Spark
spark = SparkSession.builder \
    .appName("SupermarketSalesStreaming") \
    .getOrCreate()

# Definir el esquema de los datos
schema = StructType([
    StructField("product", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", IntegerType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Leer datos de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "supermarket-sales") \
    .load()

# Convertir el valor de los datos de Kafka a JSON y aplicarle el esquema
sales_df = df.selectExpr("CAST(value AS STRING)") \
          .select(from_json(col("value"), schema).alias("data")) \
          .select("data.product", "data.quantity", "data.price", col("data.timestamp").alias("timestamp"))

# Calcular los productos más vendidos
top_selling_products_per_batch = sales_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy("product", window("timestamp", "1 hour")) \
    .sum("quantity") \
    .select("product", "window.start", "window.end", "sum(quantity)")

# Guardar los productos más vendidos en HDFS en formato CSV
query_top_selling = top_selling_products_per_batch.writeStream \
    .format("csv") \
    .option("checkpointLocation", "/tmp/top_selling_checkpoint") \
    .option("path", "hdfs://10.6.129.98:9000/user/username/top_selling_products") \
    .option("append", True) \
    .start()

# Mostrar los datos procesados en la consola
query_console = top_selling_products_per_batch.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Iniciar el streaming y esperar a que termine
query_top_selling.awaitTermination()
