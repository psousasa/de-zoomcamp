# de-zoomcamp

Solved in cmd. Need to solve it accordingly

export GOOGLE_APPLICATION_CREDENTIALS=

terraform init
terraform plan
terraform apply


### load main and boroughs map
df = pd.read_csv("green_tripdata_2019-09.csv.gz", compression='gzip')
boroughs = pd.read_csv("taxi+_zone_lookup.csv")

- dates are string

### trips on 2019-09-18 (starting and & ending on)
df[df['lpep_pickup_datetime'].str.startswith("2019-09-18") & df['lpep_dropoff_datetime'].str.startswith("2019-09-18")]
15612

### largest tip
df[df.trip_distance ==df.trip_distance.max() ]
2019-09-26

### Map PU and DO boroughs and zones
df['PUborough'] = df['PULocationID'].map(boroughs['Borough'])
df['DOborough'] = df['DOLocationID'].map(boroughs['Borough'])

df['DOZone'] = df.DOLocationID.map(boroughs['Zone'])
df['PUZone'] = df.PULocationID.map(boroughs['Zone'])


### Three biggest pick up Boroughs
df[df['lpep_pickup_datetime'].str.startswith("2019-09-18") & df.borough != 'Unknown'][['borough', 'total_amount']].groupby('borough').sum()
               total_amount
borough                    
Bronx             818158.06
Brooklyn         2619378.54 <--
EWR                  719.70
Manhattan        2427880.92 <--
Queens           2460386.17 <--
Staten Island      11248.31
Unknown            25852.58


### Largest tip
df[df.tip_amount == df[(df.PUZone == 'Astoria') & (df.lpep_pickup_datetime.str.startswith("2019-09"))]['tip_amount'].max()]
JFK Airport








