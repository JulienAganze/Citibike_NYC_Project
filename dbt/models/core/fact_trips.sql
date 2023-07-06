{{ config(materialized='table') }}

-- Add the new column
ALTER TABLE {{ ref('stg_tripdata') }} ADD COLUMN start_LatLong VARCHAR(50);

-- Populate the new column with the concatenated values
UPDATE {{ ref('stg_tripdata') }} SET start_LatLong = CONCAT(start_lat, ',', start_lng);

-- Add the new column
ALTER TABLE {{ ref('stg_tripdata') }} ADD COLUMN end_LatLong VARCHAR(50);

-- Populate the new column with the concatenated values
UPDATE {{ ref('stg_tripdata') }} SET end_LatLong = CONCAT(end_lat, ',', end_lng);


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
    member_casual as member_type

from {{ ref('stg_tripdata') }}