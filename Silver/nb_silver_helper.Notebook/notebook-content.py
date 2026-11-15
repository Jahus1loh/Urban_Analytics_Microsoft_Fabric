# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

from pyspark.sql import functions as F, DataFrame, Window
import re

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def to_snake_case(df: DataFrame) -> DataFrame:
    for c in df.columns:
        new = re.sub(r"[^0-9a-zA-Z]+", "_", c).strip("_").lower()
        df = df.withColumnRenamed(c, new)
    return df

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def add_datetime_cols(df: DataFrame, utc_col: str) -> DataFrame:
    local = F.from_utc_timestamp(F.col(utc_col), LOCAL_TZ)
    return (df
        .withColumn("datetime_local", local)
        .withColumn("date_key", F.date_format(local, "yyyyMMdd").cast("int"))
        .withColumn("hour", F.hour(local))
        .withColumn("year", F.year(local))
        .withColumn("month", F.month(local)))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def write_silver(df: DataFrame, table: str, partition_by=None) -> None:
    df = (df.withColumn("_silver_loaded_at", F.current_timestamp()))
    w = df.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
    if partition_by:
        w = w.partitionBy(*partition_by)
    w.saveAsTable(f"lh_urban_analytics_silver.dbo.{table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
