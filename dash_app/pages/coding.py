import json

import dash
import pandas as pd
import io
from dash import html, dcc, callback, Input, Output, ALL
import intersystems_iris.dbapi._DBAPI as dbapi
from dotenv import load_dotenv
load_dotenv()
import os
import dash_bootstrap_components as dbc
from datetime import datetime
from dash_table import DataTable

dash.register_page(__name__, title="Genomic Codes", name="(SQL)",path="/codes")

password = os.getenv("SQL_PASSWORD")
user = os.getenv("SQL_USERNAME")
host = os.getenv("SQL_SERVER")
namespace = os.getenv("SQL_NAMESPACE")
port = os.getenv("SQL_PORT")
if isinstance(port, str):
    port = int(port)

config = {
    "hostname": host,
    "port": port,
    "namespace": namespace,
    "username": user,
    "password": password,
}

try:
    conn = dbapi.connect(**config)
    print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

# create a cursor
cursor = conn.cursor()

sql = """
      select test.value_Value iGeneCode
           ,test.value_Text iGeneDisplay
           ,directory.value_Value TestDirectoryCode
           ,directory.value_Text TestDirectoryDisplay
      from HSFHIR_X0001_S_DiagnosticReport.code test
               join HSFHIR_X0001_S_DiagnosticReport.code directory on test.Key = directory.Key and directory.value_System = 'https://fhir.nhs.uk/CodeSystem/England-GenomicTestDirectory'
      where test.value_System = 'https://fhir.nwgenomics.nhs.uk/CodeSystem/IGEAP'
      group by test.value_Value, directory.value_Value
      order by test.value_Value \
      """

cursor.execute(sql)
data = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(data, columns=column_names)

layout = html.Div([
    html.H1('Coding'),
    dbc.Row([
        dbc.Col([
            html.H3("iGene Test Codes to Genomic Testing Directory Codes"),
            DataTable(data = df.to_dict('records'),
                     columns =  [{"name": i, "id": i} for i in df.columns],
                     style_cell=dict(textAlign='left'),
                     style_header=dict(backgroundColor="paleturquoise"),
                     style_data=dict(backgroundColor="lavender"))
        ])
    ])
])
