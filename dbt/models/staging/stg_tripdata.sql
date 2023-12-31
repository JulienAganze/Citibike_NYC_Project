{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by started_at) as rn
  from {{ source('staging','citibike_tripdata') }}
  WHERE end_station_id !="" 
)

select
    ride_id,
    rideable_type,
    cast(started_at as timestamp) as start_datetime,
    cast(ended_at as timestamp) as end_datetime,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    cast(start_lat as numeric) as start_lat,
    cast(start_lng as numeric) as start_lng,
    cast(end_lat as numeric) as end_lat,
    cast(end_lng as numeric) as end_lng,
    member_casual,
    CONCAT(start_lat, ',', start_lng) AS start_Lat_Long,
    CONCAT(end_lat, ',', end_lng) AS end_Lat_Long,
    ROUND(
        (6371 * ACOS(
            COS(SAFE_DIVIDE(start_lat * ACOS(-1), 180)) *
            COS(SAFE_DIVIDE(end_lat * ACOS(-1), 180)) *
            COS(SAFE_DIVIDE(end_lng - start_lng * ACOS(-1), 180)) +
            SIN(SAFE_DIVIDE(start_lat * ACOS(-1), 180)) *
            SIN(SAFE_DIVIDE(end_lat * ACOS(-1), 180))
        )), 2
    ) AS distance_traveled_km
    

from tripdata
where rn = 1 
-- dbt build --m <model.sql> --var 'is_test_run: false'
--{% if var('is_test_run', default=true) %}

--  limit 100

--{% endif %}