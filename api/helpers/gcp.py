from typing import Optional, List

import pandas as pd
from google.cloud import bigquery


def get_df_from_bq_query(query: str, job_config=bigquery.QueryJobConfig()) -> Optional[pd.DataFrame]:
    """Get a dataframe from BigQuery using a SQL query"""
    client = bigquery.Client()
    query_obj = client.query(query, job_config=job_config)
    result = query_obj.to_dataframe()
    return result


def get_partition_datatime_table(table: str, date_partition_field: str, date_field: str, first_day: str,
                                 last_day: str, columns: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
    
    """Descarga una tabla particionada por tiempo de BQ en las fechas dadas.
    
    Args:
        table:                  URl de tabla BQ (ej: 'mllifecycledxc.landing_prodiq.prodiq_preparation')
        date_partition_field:   Campo de la tabla BQ que se utiliza para particionar
        date_field:             Campo de la tabla BQ que almacena la fecha
        first_day:              Primer día a descargar en formato YYYY-MM-DD
        last_day:               Último día a descargar en formato YYYY-MM-DD
        column:                 Nombre de columna o columnas separadas por comas (por defecto, todas)
    
    Return:
        result:         a pandas dataframe containing the result of the query created with args of the funtion
    """
    try:
        first_month_date = first_day.split("-")[0] + "-" + first_day.split("-")[1] + "-01"
        last_month_date = last_day.split("-")[0] + "-" + last_day.split("-")[1] + "-01"
    except IndexError:
        raise IndexError("El formato de fechas utilizado no es el correcto, utilizar YYYY-MM-DD.")

    if not columns:
        select = "*"
    else:
        select = ",".join(columns)
    
    query = f"""
    SELECT {select} FROM {table}
    WHERE DATE({date_partition_field}) >= "{first_month_date}" AND DATE({date_partition_field}) <= "{last_month_date}"
    AND DATE({date_field}) >= "{first_day}" AND DATE({date_field}) <= "{last_day}"
    ORDER BY {date_field} ASC"""

    result = get_df_from_bq_query(query)
    
    return result