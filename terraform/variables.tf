locals {
  data_lake_bucket = "citibike_nyc"
}

variable "project" {
  description = "Your GCP Project ID"
  

}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "trips_data"
}

variable "BQ_DATASET_DBT_DEV" {
  description = "BigQuery Dataset that dbt will use for during development"
  type = string
  default = "development"
}

variable "BQ_DATASET_DBT_PROD" {
  description = "BigQuery Dataset that dbt will use for during development"
  type = string
  default = "production"
}
