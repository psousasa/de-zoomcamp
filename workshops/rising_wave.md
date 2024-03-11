1. Not being able to run ctes in terminal.
SELECT pu_zone.zone, do_zone.zone, avg(tpep_dropoff_datetime - tpep_pickup_datetime) average, min(tpep_dropoff_datetime - tpep_pickup_datetime) shortest, max(tpep_dropoff_datetime - tpep_pickup_datetime) longest FROM trip_data
JOIN taxi_zone do_zone
        ON trip_data.DOLocationID = do_zone.location_id 
JOIN taxi_zone pu_zone
	on trip_data.PULocationID = pu_zone.location_id
        
 group by pu_zone.zone, do_zone.zone
 order by average desc;
 
 2.  Adding count to above
 SELECT pu_zone.zone, do_zone.zone, avg(tpep_dropoff_datetime - tpep_pickup_datetime) average, min(tpep_dropoff_datetime - tpep_pickup_datetime) shortest, max(tpep_dropoff_datetime - tpep_pickup_datetime) longest, count(1) FROM trip_data
JOIN taxi_zone do_zone
        ON trip_data.DOLocationID = do_zone.location_id 
JOIN taxi_zone pu_zone
	on trip_data.PULocationID = pu_zone.location_id
        
 group by pu_zone.zone, do_zone.zone
 order by average desc;

3. Question enunciate was not clear with the 17 interval versus the example it gave (only 1h). The output (below) is not an option. Selected option on 2 out of 3 match.
              zone              |  a  
--------------------------------+-----
 JFK Airport                    | 130
 LaGuardia Airport              |  80
 Penn Station/Madison Sq West   |  60

 SELECT pu_zone.zone, count(*) as a
 from trip_data
 
 JOIN taxi_zone do_zone
        ON trip_data.DOLocationID = do_zone.location_id 
 JOIN taxi_zone pu_zone
	on trip_data.PULocationID = pu_zone.location_id
 WHERE tpep_dropoff_datetime >= (SELECT max(tpep_pickup_datetime) - INTERVAL '17 HOUR' from trip_data)
 and  tpep_dropoff_datetime <= (SELECT max(tpep_pickup_datetime) from trip_data)
 group by pu_zone.zone
 order by a desc;
 
 
 
