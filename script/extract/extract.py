
from helper.utils import logging_process,init_spark_session,source_engine,source_conn_prop
import logging
import pyspark
logging_process()


def extract_data(
    data_name: str, format_data: str
) -> pyspark.sql.DataFrame:
    """
    Function to extract movie data in csv or database table

    Parameters
    ----------
    data_name (str): name of data or table of data sources
    format_data (str): format data of data sources, currently on csv or db

    Returns
    -------
    df (pyspark.sql.DataFrame): dataframe of data sources
    """
    # create spark session
    spark = init_spark_session()

    # set engine & config for database
    source_url = source_engine()
    source_prop = source_conn_prop()

    try:
        if format_data.lower() == "csv":
            logging.info(f"===== Start Extracting {data_name} data (CSV) =====")

            df =  spark.read.option("header", True).csv(f"data/new_bank_transaction.csv", header=True)

            logging.info(f"===== Finish Extracting {data_name} data =====")

            return df

        elif format_data.lower() == "db":
            logging.info(f"===== Start Extracting {data_name} data (Database) =====")

            df = spark.read.jdbc(
                url=source_url, table=data_name, properties=source_prop
            )

            logging.info(f"===== Finish Extracting {data_name} data =====")

            return df

        else:
            raise Exception("Format data not supported yet")

    except Exception as e:
        logging.error("====== Failed to Extract Data ======")
        logging.error(e)

        raise Exception(e)