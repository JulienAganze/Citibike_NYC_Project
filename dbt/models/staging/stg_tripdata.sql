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
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    start_lat,
    start_lng,
    end_lat,
    end_lng,
    member_casual

from tripdata
where rn = 1 
-- dbt build --m <model.sql> --var 'is_test_run: false'
--{% if var('is_test_run', default=true) %}

--  limit 100

--{% endif %}