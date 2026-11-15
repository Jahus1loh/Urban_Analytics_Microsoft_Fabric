# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f8567248-07e3-4d35-b2ad-22452d9d88ec",
# META       "default_lakehouse_name": "lh_urban_analytics_silver",
# META       "default_lakehouse_workspace_id": "98b6d407-d99a-48f1-a048-6cacdf7adf6c",
# META       "known_lakehouses": [
# META         {
# META           "id": "f8567248-07e3-4d35-b2ad-22452d9d88ec"
# META         },
# META         {
# META           "id": "aeec20e2-163c-44e8-8987-c37faf72dd95"
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

df = spark.sql("SELECT * FROM lh_urban_analytics_bronze.dbo.ECB_daily_FX")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Clean data

# CELL ********************

ecb_daily_fx = (df
    .withColumnRenamed("time_period", "rate_date")
    .withColumnRenamed("obs_value", "eur_usd_rate")
    .withColumn("rate_date", F.to_date("rate_date"))
    .withColumn("eur_usd_rate", F.col("eur_usd_rate").cast("double"))
    .filter(F.col("rate_date").isNotNull() & F.col("eur_usd_rate").isNotNull())
    .select("rate_date", "eur_usd_rate")
    .dropDuplicates(["rate_date"])
    .sort("rate_date")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

earliest_latest_dates = ecb_daily_fx.agg(
    F.min("rate_date").alias("first_date"),
    F.max("rate_date").alias("latest_date")
).first()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

calendar = (
    spark.range(1)
    .select(
        F.explode(
            F.sequence(
                F.lit(earliest_latest_dates.first_date),
                F.lit(earliest_latest_dates.latest_date),
                F.expr("INTERVAL 1 DAY")
            )
        ).alias("rate_date")
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

ecb_daily_fx = calendar.join(
    ecb_daily_fx.select("rate_date", "eur_usd_rate"),
    on="rate_date",
    how="left"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

w = Window.orderBy("rate_date").rowsBetween(Window.unboundedPreceding, 0)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

ecb_daily_fx = ecb_daily_fx.withColumn(
    "eur_usd_rate",
    F.last("eur_usd_rate", ignorenulls=True).over(w)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Save table

# CELL ********************

write_silver(ecb_daily_fx, "ecb_daily_fx")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
