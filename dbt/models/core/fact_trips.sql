{{ config(materialized='table') }}




select
    ride_id,
    rideable_type,
    start_datetime,
    end_datetime,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    start_lat,
    start_lng,
    end_lat,
    end_lng,
    member_casual as member_type,
    CONCAT(start_lat, ',', start_lng) AS start_LatLong,
    CONCAT(end_lat, ',', end_lng) AS end_LatLong

from {{ ref('stg_tripdata') }}


