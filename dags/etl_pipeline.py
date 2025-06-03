from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.dbt.operators.dbt import DbtRunOperator

# Default arguments for the DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for data processing',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'production'],
)

# Extract data from source systems
def extract_data(**context):
    """Extract data from various sources"""
    # Add your extraction logic here
    pass

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# Load data to staging
load_to_staging = SnowflakeOperator(
    task_id='load_to_staging',
    sql="""
    COPY INTO staging.raw_data
    FROM @my_stage/data/
    FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
    """,
    snowflake_conn_id='snowflake_conn',
    dag=dag,
)

# Run dbt transformations
dbt_run = DbtRunOperator(
    task_id='dbt_run',
    dir='/dbt',
    profiles_dir='/dbt/profiles',
    dag=dag,
)

# Data quality checks
def run_quality_checks(**context):
    """Run data quality validation"""
    # Add your quality check logic here
    pass

quality_check = PythonOperator(
    task_id='quality_check',
    python_callable=run_quality_checks,
    dag=dag,
)

# Define task dependencies
extract_task >> load_to_staging >> dbt_run >> quality_check 