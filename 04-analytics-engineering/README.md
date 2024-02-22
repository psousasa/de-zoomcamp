# Week 4: Analytics Engineering 

1. Started  by loading the FHV data into a GCP bucket using what was done in module 3. Had to make changes and impose the datatypes before writting.

2.Created external table from GCS parquet files
~~~
CREATE OR REPLACE EXTERNAL TABLE `green_taxi_data.external_green_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://03-data-warehouse/green/green_tripdata_2022-*.parquet']
);
~~~

3. Create materilized table from external table
~~~
CREATE OR REPLACE TABLE `green_taxi_data.green_tripdata_non_partitioned`
SELECT * FROM `green_taxi_data.external_green_tripdata`
~~~

4. Implemented the ETL in dbt

5. Create some widgets in Looker.


