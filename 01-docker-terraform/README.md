# 01-docker-terraform

1. Modify ingest_data.py to use lpep* instead of tpep* date fields.

2. Create ingest_zones.py file to insert Zones data into the PostGreSQL DB.

3. Create the docker network.
~~~
docker network create pg-network
~~~

4. Startup the PostGresSQL DB:
~~~
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
~~~
  
5. Run PG Admin:
~~~
docker run -it   \
 -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
 -e PGADMIN_DEFAULT_PASSWORD="root" \
 -p 8080:80   \
 --network=pg-network   \
 --name pgadmin-2 \
 dpage/pgadmin4
~~~

4. Ingest Green Trip Data:
~~~
python3 ingest_data.py \
 --user=root \
 --password=root \
 --host=localhost \
 --port=5432 \
 --db=ny_taxi \
 --table_name=green_taxi_trips \
 --url=https://github.com/DataTalksClub/nyc-tlc-data/releases download/green/green_tripdata_2019-09.csv.gz
~~~ 

5. Ingest Zones data:
~~~
python3 ingest_zones.py \
 --user=root \
 --password=root \
 --host=localhost \
 --port=5432 \
 --db=ny_taxi \
 --table_name=green_taxi_trips \
 --url=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
~~~

6. Startup the PostGres CLI:
~~~
pgcli -h localhost -p 5432 -u root -d ny_taxi
~~~


### Queries

1. How many taxi trips were totally made on September 18th 2019?
~~~
select count(1) 
from green_taxi_trips 
where cast(lpep_dropoff_datetime as date) = '2019-09-18' and 
      cast(lpep_pickup_datetime as date) = '2019-09-18'

15612
~~~


2. Which was the pick up day with the longest trip distance? 
~~~
select lpep_pickup_datetime 
from green_taxi_trips 
where trip_distance = (
  select max(trip_distance) 
  from green_taxi_trips
  )

2019-09-26 19:32:52
~~~


3. Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown. Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

~~~
select 
  zpu."Borough", 
  sum(gtt."total_amount") 
from green_taxi_trips gtt 
join zones as zpu on zpu."LocationID" = gtt."PULocationID" 
where cast(gtt.lpep_pickup_datetime as date) = '2019-09-18'  
group by zpu."Borough"
having sum(gtt."total_amount") > 50000

+-----------+-------------------+
| Borough   | sum               |
|-----------+-------------------|
| Brooklyn  | 96333.2400000032  |
| Manhattan | 92271.30000000466 |
| Queens    | 78671.7100000036  |
+-----------+-------------------+
~~~


4. For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? 

~~~
select 
  zdo."Zone", 
  gtt.tip_amount 
from green_taxi_trips gtt 
join zones as zpu on zpu."LocationID" = gtt."PULocationID" 
join zones as zdo on gtt."DOLocationID"=zdo."LocationID" 
where 
  cast(gtt.lpep_pickup_datetime as date) >= '2019-09-01' and
  cast(gtt.lpep_pickup_datetime as date) <= '2019-09-30' and 
  zpu."Zone" = 'Astoria'  
order by gtt.tip_amount desc limit 1
  
+-------------+------------+
| Zone        | tip_amount |
|-------------+------------|
| JFK Airport | 62.31      |
+-------------+------------+
~~~