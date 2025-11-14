import logging
from pyspark.sql import SparkSession
from sqlalchemy import create_engine, text

# for truncate
def create_engine_warehouse():
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_NAME = "data_warehouse"
    DB_PORT = 5432
    DB_CONTAINER = "data_warehouse_container"
    
    warehouse_engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_CONTAINER}:{DB_PORT}/{DB_NAME}")
    return warehouse_engine

def source_engine():
    src_container = "source_db_container"
    src_database = "source"
    src_port = 5432
    
    return f"jdbc:postgresql://{src_container}:{src_port}/{src_database}"

def source_conn_prop():
    DB_USER = "postgres"
    DB_PASS = "postgres"
    return {
        "user": DB_USER,
        "password": DB_PASS,
        "driver": "org.postgresql.Driver",  # set driver postgres
    }


def warehouse_engine():
    wr_container = "data_warehouse_container"
    wr_database = "data_warehouse"
    wr_port = 5432
    
    return f"jdbc:postgresql://{wr_container}:{wr_port}/{wr_database}"

def warehouse_conn_prop():
    DB_USER = "postgres"
    DB_PASS = "postgres"
    return {
        "user": DB_USER,
        "password": DB_PASS,
        "driver": "org.postgresql.Driver",  # set driver postgres
    }

def logging_process():
    # Configure logging
    logging.basicConfig(
        filename="/home/jovyan/work/log/info.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def init_spark_session():
    spark = SparkSession.builder.appName(
        "Mentoring 3"
    ).getOrCreate()
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    return spark

# Check null values
def check_null_values(df):
    list_columns = df.columns
    is_null = False
    
    for cols in list_columns:
        missing_count = df.filter(df[cols].isNull()).count()
        if missing_count > 0 :
            is_null = True
            print(f"{cols} has null values")
        

    if is_null == False:
        print("There's no null value")
    

