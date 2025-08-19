from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import logging
import psutil  # Make sure psutil is installed in the Airflow environment

# Function to log current working directory and files
def log_current_directory_and_files():
    cwd = os.getcwd()
    files = os.listdir(cwd)

    logging.info(f"Current Working Directory: {cwd}")
    logging.info("Files and directories:")
    for f in files:
        logging.info(f" - {f}")

# Function to log mount points
def log_mount_points():
    logging.info("Mounted File Systems:")
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        logging.info(f" - Mount point: {p.mountpoint}, Device: {p.device}, FS Type: {p.fstype}")

# Function to log files in /mnt/datasources
def log_datasources_files():  

    paths = ["/", "/mnt", "/mnt/user", "/mnt/shared", "/mnt/datasources", "/mnt/datasources/vast", "/mnt/datasources/vast/glfileshare"]
    
    for path in paths:
        files = os.listdir(path)
        logging.info(f"Files in {path}")
        for f in files:
            logging.info(f" - {f}")


# Define the DAG
with DAG(
    dag_id="log_directory_files_and_mounts",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    description="Logs current working directory, files, and mount points",
    access_control={'All': {'can_read', 'can_edit', 'can_delete'}}
) as dag:

    log_files_task = PythonOperator(
        task_id="log_directory_and_files",
        python_callable=log_current_directory_and_files,
    )

    log_mounts_task = PythonOperator(
        task_id="log_mount_points",
        python_callable=log_mount_points,
    )

    log_datasources_files_task = PythonOperator(
        task_id="log_datasources_files",
        python_callable=log_datasources_files,
    )

    log_files_task >> log_mounts_task >> log_datasources_files_task
