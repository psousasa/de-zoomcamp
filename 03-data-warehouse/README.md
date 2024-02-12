# 03-data-warehouse


Create external table from GCS parquet files
~~~
CREATE OR REPLACE EXTERNAL TABLE `green_taxi_data.external_green_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://03-data-warehouse/green/green_tripdata_2022-*.parquet']
);
~~~

Create materilized table from external table
~~~
CREATE OR REPLACE TABLE `green_taxi_data.green_tripdata_non_partitioned`
SELECT * FROM `green_taxi_data.external_green_tripdata`
~~~

1. Get number of records
~~~
SELECT count(*) FROM `taxi-rides-ny.nytaxi.fhv_tripdata`;
~~~

2.  query memory - select query and wait for GCP to tell the estimate
~~~
select count(distinct(PULocationId)) FROM `hybrid-saga-412112.green_taxi_data.external_green_tripdata`;

select count(distinct(PULocationId)) FROM `hybrid-saga-412112.green_taxi_data.green_tripdata_non_partitioned`;
~~~

3. Get number of records with fare_amount = 0
~~~
SELECT COUNT(*) FROM `green_taxi_data.external_green_tripdata` WHERE fare_amount = 0;
~~~

Create partitioned + clustered table
~~~
CREATE OR REPLACE TABLE `hybrid-saga-412112.green_taxi_data.green_tripdata_partitioned_clustered`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS (
  SELECT * FROM `hybrid-saga-412112.green_taxi_data.green_tripdata_non_partitioned`
);
~~~
5.Compare memory non partitioned vs partitioned + clustered - select query and wait for GCP to tell the estimate
~~~
SELECT distinct PULocationID FROM `hybrid-saga-412112.green_taxi_data.green_tripdata_non_partitioned` where lpep_pickup_datetime between '2022-06-01' and '2022-06-30';

SELECT distinct PULocationID FROM `hybrid-saga-412112.green_taxi_data.green_tripdata_partitioned_clustered` where lpep_pickup_datetime between '2022-06-01' and '2022-06-30';
~~~
