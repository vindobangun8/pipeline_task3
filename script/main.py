from pyspark.sql import SparkSession
from helper.utils import init_spark_session
from extract.extract import extract_data
from transform.transform_marketing import transform_marketing
from transform.transform_transaction import transform_transaction
from transform.transform_customer import transform_customer
from load.load_data import load_data

if __name__ == "__main__":
    # Inisialisasi SparkSession
    spark = init_spark_session()
    
    # handle legacy time parser
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    
    # Extract data 
    education_df = extract_data('education_status','db')
    marital_df = extract_data('marital_status','db')
    marketing_df = extract_data('marketing_campaign_deposit','db')
    bank_df = extract_data('new_bank_transaction','csv')
    
    # Transform data
    # Marketing
    marketing_df = transform_marketing(marketing_df)
    
    # Bank
    bank_df = transform_customer(bank_df)
    cust_df = bank_df.select(['customer_id','birth_date','gender','location','account_balance'])

    bank_df = transform_transaction(bank_df)
    trans_df= bank_df.select(['transaction_id','customer_id','transaction_date','transaction_time','transaction_amount'])
    
    # Load data
    load_data(education_df,'education_status')
    load_data(marital_df,'marital_status')
    load_data(marketing_df,'marketing_campaign_deposit')
    load_data(cust_df,'customers')
    load_data(trans_df,'transactions')