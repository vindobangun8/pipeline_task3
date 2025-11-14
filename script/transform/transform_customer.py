import logging
import pyspark
from helper.utils import logging_process
from pyspark.sql.functions import regexp_replace,to_date,year,month,dayofmonth,when,make_date
from pyspark.sql.types import DecimalType

logging_process()

def transform_customer(bank_df):
    try:
        logging.info("===== Start Transform Customer Data =====")

        # remove null values
        bank_df = bank_df.dropna()
       
        # rename columns
        list_cols = {
            'CustomerID':'customer_id',
            'CustomerDOB':'birth_date',
            'CustGender':'gender',
            'CustLocation':'location',
            'CustAccountBalance':'account_balance'
        }
        bank_df = bank_df.withColumnsRenamed(list_cols)
    
       # birth date
        bank_df = bank_df.withColumn(
            "birth_date",
            to_date(bank_df["birth_date"], "d/M/yy")
        )
        # adjust birth_date > 2025 
        bank_df = bank_df.withColumn(
            "birth_date",
            when(year(bank_df["birth_date"]) >= 2025,
                 make_date((year(bank_df["birth_date"]) - 100), month(bank_df["birth_date"]), dayofmonth(bank_df["birth_date"]))
                ).otherwise(bank_df["birth_date"])
        )
        
        # gender
        bank_df = bank_df.filter(bank_df['gender'].isin(['M','F']))
        
        gender_list = {
            'M':"Male",
            "F":"Female"
        }
        bank_df = bank_df.replace(gender_list,subset=['gender'])

        # account balance
        bank_df = bank_df.withColumn('account_balance',bank_df['account_balance'].cast(DecimalType(10, 2)))
        logging.info("===== Finish Transform Customer Data =====")
        return bank_df
    except Exception as e:
        logging.error("===== Failed Transform Customer Data =====")
        logging.error(e)

        raise Exception(e)