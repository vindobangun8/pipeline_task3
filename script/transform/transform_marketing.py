import logging
import pyspark
from helper.utils import logging_process
from pyspark.sql.functions import regexp_replace

logging_process()

def transform_marketing(marketing_df):
    try:
        logging.info("===== Start Transform Marketing Data =====")
        # balance
        marketing_df = marketing_df.withColumn("balance",regexp_replace("balance", r'\$', ''))
        marketing_df = marketing_df.withColumn("balance",marketing_df['balance'].cast("int"))
    
        # duration
        marketing_df = marketing_df.withColumn("duration_in_year",(marketing_df['duration'] / 365).cast("int"))
    
        # rename columns
        list_columns ={
        'pdays':'days_since_last_campaign',
        'previous':'previous_campaign_contacts',
        'poutcome':'previous_campaign_outcome'
        }
        marketing_df = marketing_df.withColumnsRenamed(list_columns)
    
        logging.info("===== Finish Transform Marketing Data =====")
    
        return marketing_df
    except Exception as e:
        logging.error("===== Failed Transform Marketing Data =====")
        logging.error(e)

        raise Exception(e)