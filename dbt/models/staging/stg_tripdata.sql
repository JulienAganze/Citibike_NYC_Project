{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by started_at) as rn
  from {{ source('staging','citibike_tripdata') }}
  --where VendorID is not null 
)

select
    ride_id,
    rideable_type,
    cast(started_at as timestamp) as start_datetime,
    cast(ended_at as timestamp) as end_datetime,
    cast(start_station_name as VARCHAR),
    cast(start_station_id as VARCHAR),
    cast(end_station_name as VARCHAR),
    cast(end_station_id as VARCHAR),
    cast(start_lat as VARCHAR),
    cast(start_lng as VARCHAR),
    cast(end_lat as VARCHAR),
    cast(end_lng as VARCHAR),
    cast(member_casual as VARCHAR)

from tripdata
where rn = 1 
-- dbt build --m <model.sql> --var 'is_test_run: false'
--{% if var('is_test_run', default=true) %}

--  limit 100

--{% endif %}