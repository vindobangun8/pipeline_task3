import logging
import pyspark
from helper.utils import logging_process
from pyspark.sql.functions import regexp_replace,to_date,year,date_format,lpad,to_timestamp
from pyspark.sql.types import DecimalType

logging_process()

def transform_transaction(bank_df):
    try:
        logging.info("===== Start Transform Customer Data =====")
        list_cols = {
            'TransactionID':'transaction_id',
            'TransactionDate':'transaction_date',
            'TransactionTime':'transaction_time',
            'TransactionAmount (INR)':'transaction_amount'
        }
        bank_df = bank_df.withColumnsRenamed(list_cols)
    
       # transaction_date
        bank_df = bank_df.withColumn(
            "transaction_date",
            to_date(bank_df["transaction_date"], "d/M/yy")
        )
        
        # filter transaction_date > 2025 
       
        bank_df = bank_df.filter(year('transaction_date') <= 2025)

        # Transaction_time 
        bank_df = bank_df.withColumn("transaction_time",date_format(to_timestamp(lpad(bank_df['transaction_time'], 6, "0"),"HHmmss"),"HH:mm:ss"))

        # account balance
        bank_df = bank_df.withColumn('transaction_amount',bank_df['transaction_amount'].cast(DecimalType(10, 2)))

        logging.info("===== Finish Transform Transaction Data =====")
        return bank_df
    except Exception as e:
        logging.error("===== Failed Transform Transaction Data =====")
        logging.error(e)

        raise Exception(e)