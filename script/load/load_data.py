from helper.utils import logging_process,init_spark_session,warehouse_engine,warehouse_conn_prop,create_engine_warehouse
from sqlalchemy import create_engine, text
import logging
import pyspark
logging_process()


def load_data(df_result: pyspark.sql.DataFrame, table_name: str) -> None:
    """
    Function that used to dump the result to the database using PySpark

    Parameters
    ----------
    df_result (pyspark.sql.DataFrame): final result of pyspark dataframe
    """
    try:
         # create spark session
        spark = init_spark_session()
    
        # set engine & config for database
        warehouse_url = warehouse_engine()
        warehouse_prop = warehouse_conn_prop()

        #for truncate
        engine = create_engine_warehouse()
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name} Cascade"))
            conn.commit()

        logging.info("===== Start Load data to the database =====")

        # load data
        df_result.write.jdbc(
            url=warehouse_url,
            table=table_name,
            mode="append",
            properties=warehouse_prop,
        )

        logging.info("===== Finish Load data to the database =====")

    except Exception as e:
        logging.error("===== Failed Load data to the database =====")
        logging.error(e)
        raise Exception(e)
