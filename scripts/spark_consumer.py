from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


# Crear una sesión de Spark
spark = SparkSession.builder \
    .appName("SupermarketSalesStreaming") \
    .getOrCreate()

# Definir el esquema de los datos
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", IntegerType(), True),
    StructField("timestamp", StringType(), True),
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
    .select("data.*")

# Calcular los productos más vendidos
top_selling_products = sales_df \
    .groupBy("product_name") \
    .sum("quantity") \
    .orderBy(col("sum(quantity)").desc()) \
    .limit(10)

# Guardar los productos más vendidos en HDFS en formato CSV
query_top_selling = top_selling_products.writeStream \
    .outputMode("Append") \
    .format("console") \
    .option("path", "hdfs://10.6.129.98:9000/user/username/top_selling_products") \
    .option("checkpointLocation", "hdfs://10.6.129.98:9000/user/username/checkpoint_top_selling_products") \
    .start()

# Calcular productos con existencias bajas
low_stock_products = sales_df \
    .groupBy("product_name") \
    .sum("quantity") \
    .filter(col("sum(quantity)") < 10) \
    .orderBy(col("sum(quantity)").asc())

# Guardar los productos con existencias bajas en HDFS en formato CSV
query_low_stock = low_stock_products.writeStream \
    .outputMode("Append") \
    .format("console") \
    .option("path", "hdfs://10.6.129.98:9000/user/username/low_stock_products") \
    .option("checkpointLocation", "hdfs://10.6.129.98:9000/user/username/checkpoint_low_stock_products") \
    .start()

    
# Iniciar el streaming y esperar a que termine
query_top_selling.awaitTermination()
query_low_stock.awaitTermination()
