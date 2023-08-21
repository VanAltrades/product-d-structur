from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from process_txt import get_dict_from_txt, get_structured_dict

d, unique_keys = get_dict_from_txt("amazon-product-data.txt")
d_schema = get_structured_dict(d,unique_keys)

credentials = service_account.Credentials.from_service_account_file("..\secret.json")

# Your BigQuery project ID and dataset ID
project_id = 'e-commerce-demo-v'
dataset_id = 'class_product'
table_id = "d_product"

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(d_schema, orient='index')

# Reorder the columns
new_order = ["Brand", "MPN", "Title","Manufacturer","ProductGroup","ProductTypeName"] + [col for col in df.columns if col not in ["Brand", "MPN", "Title","Manufacturer","ProductGroup","ProductTypeName"]]
df = df[new_order]

# Upload the DataFrame to BigQuery
destination = f"{dataset_id}.{table_id}"  # Replace with your table name

df.to_gbq(
    destination_table=destination, 
    project_id=project_id,
    chunksize=2000, 
    if_exists='replace',
    credentials=credentials
    )