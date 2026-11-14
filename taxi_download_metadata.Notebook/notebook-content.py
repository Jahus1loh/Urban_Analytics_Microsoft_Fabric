# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "aeec20e2-163c-44e8-8987-c37faf72dd95",
# META       "default_lakehouse_name": "lh_urban_analytics",
# META       "default_lakehouse_workspace_id": "98b6d407-d99a-48f1-a048-6cacdf7adf6c",
# META       "known_lakehouses": [
# META         {
# META           "id": "aeec20e2-163c-44e8-8987-c37faf72dd95"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.types import StructType, StructField, StringType
from collections.abc import Sequence

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

metadata_rows = []
start_year = 2009
end_year = 2027
start_month = 1
end_month = 13

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def find_taxi_colors_for_date(yyyymm: str) -> Sequence[str]:
    if yyyymm <= 201307:
        colors = ['yellow']
    elif 201308 <= yyyymm <= 201412:
        colors = ['yellow', 'green']
    elif 201501 <= yyyymm <= 201901:
        colors = ['yellow', 'green', 'fhv']
    else:
        colors = ['yellow', 'green', 'fhv', 'fhvhv']
    return colors

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for year in range(start_year, end_year):
    for month in range(start_month, end_month):
        if year == 2026 and month > 9:
            break
        yyyymm = year * 100 + month
        month_str = f"{month:02d}"
        year_str = str(year)
        colors = find_taxi_colors_for_date(yyyymm)  
        for color in colors:
            metadata_rows.append((color, year_str, month_str))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema = StructType([
    StructField("taxi_color", StringType(), True),
    StructField("year", StringType(), True),
    StructField("month", StringType(), True)
])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.createDataFrame(metadata_rows, schema)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.format("delta").mode("overwrite").saveAsTable("taxi_download_metadata")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
