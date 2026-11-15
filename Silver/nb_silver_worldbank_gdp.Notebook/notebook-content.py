# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "aeec20e2-163c-44e8-8987-c37faf72dd95",
# META       "default_lakehouse_name": "lh_urban_analytics_bronze",
# META       "default_lakehouse_workspace_id": "98b6d407-d99a-48f1-a048-6cacdf7adf6c",
# META       "known_lakehouses": [
# META         {
# META           "id": "aeec20e2-163c-44e8-8987-c37faf72dd95"
# META         },
# META         {
# META           "id": "f8567248-07e3-4d35-b2ad-22452d9d88ec"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

%run nb_silver_helper

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Import data

# CELL ********************

df = spark.sql("SELECT * FROM lh_urban_analytics_bronze.dbo.worldbank_gdp_usa LIMIT 1000")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Clean data

# CELL ********************

gdp = (df
    .withColumnRenamed("value", "gdp_usd")
    .withColumnRenamed("date", "year")
    .select("year", "gdp_usd")
    .withColumn("year", F.col("year").cast("int"))
    .withColumn("gdp_usd", F.col("gdp_usd").cast("double"))
    .filter(F.col("gdp_usd").isNotNull() & F.col("year").isNotNull())
    .drop_duplicates(["year"])
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Write to silver table

# CELL ********************

write_silver(gdp, "worldbank_gdp")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ###
