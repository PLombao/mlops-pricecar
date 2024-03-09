from typing import Optional, List

import pandas as pd
from google.cloud import bigquery


def get_df_from_bq_query(query: str, job_config=bigquery.QueryJobConfig()) -> Optional[pd.DataFrame]:
    """Get a dataframe from BigQuery using a SQL query"""
    client = bigquery.Client()
    query_obj = client.query(query, job_config=job_config)
    result = query_obj.to_dataframe()
    return result

def insert_row(data: dict):
    client = bigquery.Client()
    dataset_id = "nifty-acolyte-415508.mlops_data"
    table_id = "predictions"
    table_ref = dataset_id + "." + table_id
    client.load_table_from_dataframe(data, table_ref)
    # errors = client.insert_rows_json(dataset_id, table_id, [data])

    

    


