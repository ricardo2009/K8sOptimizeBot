from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import matplotlib.pyplot as plt

# Autenticação
personal_access_token = ''
organization_url = ''
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Clientes
core_client = connection.clients.get_core_client()
git_client = connection.clients.get_git_client()
build_client = connection.clients.get_build_client()
agent_client = connection.clients_v7_0.get_task_agent_client()