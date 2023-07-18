# NYC Bike project

## Objective



## Architecture


## Problem statement




## Main objective

The following steps were performed to analyze the air quality data for the 100 Polish cities:



## Dataset description






## Proposal

### Technologies
## What technologies are being used?
- Cloud: [Google Cloud](https://cloud.google.com)
- Infrastructure: [Terraform](https://www.terraform.io/)
- Orchestration: [Prefect](https://www.prefect.io/)
- Data lake: [Google Cloud Storage](https://cloud.google.com/storage)
- Data transformation: [DBT](https://www.getdbt.com/)
- Data warehouse: [BigQuery](https://cloud.google.com/bigquery)
- Data visualization: [Google Looker Studio](https://cloud.google.com/looker)


### Repository organization
- \dbt: dbt files (dbt_project.yml, models, etc.).
- \airflow: prefect flows files (etl_tasks.py, history_parameterized_flow.py, current_parameterized_flow.py, docker_deployment.py).  
- \images: pictures.  
- \terraform: terraform files for the definition of the infrastructure to deploy.  
- \README.md: this document.  
- \setup_gcp.md: instructions to configure cgp account.  
- \setup_vm.md: instructions to setup the VM in GCP.  

**Infrastructure as code:**  

Use Terraform to create a bucket GCS and dataset in BQ  
- airpollution bucket to store parquet files.
- raw dataset for the ingestion into BigQuery.
- development dataset for dbt cloud development environment.
- production dataset for dbt cloud production environment. 

  **Orchestration:**  
To use Prefect to retrieve data from the Weather API (https://openweathermap.org/api) and load it into CGS before finally inserting it into a regular BigQuery table, follow the steps below:
- Create a free account on https://home.openweathermap.org/users/sign_up and generate your API key.
- Export your API key in the following format:
```bash
export API_KEY=<insert your key here>
```
This key will be used by the script to authenticate your requests to the Weather API.
- Sign-up for the prefect cloud and create a workspace [here](https://app.prefect.cloud/auth/login)
- Create the [prefect blocks](https://docs.prefect.io/concepts/blocks/) via the cloud UI or adjust the variables in `/blocks/make_gcp_blocks.py` and `/blocks/make_docker_block.py` then run
```bash
python blocks/make_gcp_blocks.py
python blocks/make_docker_block.py
```
- To execute the flow, run the following commands in two different CL terminals
```bash
prefect agent start -q 'default'
```
```bash
python flows/history_parameterized_flow.py
```

**Transformations using dbt:**  
  
  Use dbt cloud to perform joins and aggregations on BQ.  
  - Staging (materialized=view):  
    - airpollution and cities: Create staged model from airpollution and cities tables in Big Query.  
    - The output will be `stg_air_pollution` and `stg_cities` models.  
       
  - Core (materialized=table):
    - `fact_pollution` materialized model by joining `stg_air_pollution` with `stg_cities` models. 
    - In addition, a `agg_pollution_by_day` model has been created. This model averages the daily observations and determines daily pollution quality for every city. 
  - Job:
    - For the convenient creation of the production dataset, a job `dbt build` will be created.
    - This job can be run manually (or scheduled) from dbt cloud.

    **Dashboard:**  
  
  Connect Google Data Studio to BQ dataset and design dashboard  

  ## Results

**Dashboard**

<p align="left">
<img src="images/example_dashboard.JPG" width="600">
</p>

You can check my dashboard here:
https://lookerstudio.google.com/reporting/34c9db2f-e5e6-4fae-9a89-c89c0f134c3e

## Setup and running

Terraform and Prefect will run in a VM in Google Cloud. Prefect will run as docker container (It is possible to just install requirements in conda environment for example).
For data transformation:  
Dbt cloud will be used to perform data transformation pipeline.  
  
Your gcp account will be used and, unless you have google's welcome credit, it will have some cost.
Your dbt cloud account will be used. Developer account is free.

If you wish to install the required tools in your own machine instead of in the VM, the instructions in `setup_gcp.md` will be a good starting point.

### Setup

Note: This setup is not mean to be for production environment. More specific service account roles should be implemented as well as changing default passwords (e.g. `sudo passwd` in your VM to create the root password since VMs in GCE does not provide a password for root user).

Follow the following steps in the same order:
1. Google Cloud Platform account and project:  
  Follow the instructions in `setup_gcp.md`  
2. Virtual Machine in Google Cloud Compute Engine:  
  Follow the instructions in `setup_vm.md`

### Run pipelines
1. Setup your Google Cloud environment
- Create a [Google Cloud Platform project](https://console.cloud.google.com/cloud-resource-manager)
- Configure Identity and Access Management (IAM) for the service account, giving it the following privileges: BigQuery Admin, Storage Admin and Storage Object Admin
- Download the JSON credentials and save it, e.g. to `~/.gc/<credentials>`
- Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
- Let the [environment variable point to your GCP key](https://cloud.google.com/docs/authentication/application-default-credentials#GAC), authenticate it and refresh the session token
```bash
export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```
2. Install all required dependencies into your environment
```bash
pip install -r requirements.txt
```
3. Terraform
`cd terraform`
`terraform init`
`terraform plan -var="project=<your-gcp-project-id>"`
`terraform apply -var="project=<your-gcp-project-id>"`

4. API_KEY
- Export your API key in the following format:
```bash
export API_KEY=<insert your key here>
```

5. Setup your orchestration

- Create the [prefect blocks](https://docs.prefect.io/concepts/blocks/) via the cloud UI or adjust the variables in `/blocks/make_gcp_blocks.py` and `/blocks/make_docker_block.py` then run
```bash
python blocks/make_gcp_blocks.py
python blocks/make_docker_block.py
```
- To execute the flow, run the following commands in two different CL terminals
```bash
prefect agent start -q 'default'
```
```bash
python flows/history_parameterized_flow.py
```
