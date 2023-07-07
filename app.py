from flask import Flask, render_template, request, jsonify
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import AzureOpenAI
from datetime import datetime

# Set up OpenAI environment variables
import os
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = "ca54d9c9a14f4308b1f8da08fbcb5d44"
os.environ["OPENAI_API_BASE"] = "https://azureopenaichatbot123.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"

# Create an instance of AzureOpenAI language model
llm = AzureOpenAI(
    deployment_name="MyChatBotDeployment",
    model_name="text-davinci-003",
    openai_api_key="ca54d9c9a14f4308b1f8da08fbcb5d44",
    model_kwargs={
        "api_type": "azure",
        "api_version": "2022-12-01"
    }
)

# SQL Server connection settings
from sqlalchemy import create_engine
import urllib.parse

server = 'DESKTOP-PV2MMT2\SQLEXPRESS'
database = 'Details'
trusted_connection = 'yes'

# Set up SQLAlchemy connection string
conn_str = "DRIVER={SQL Server};SERVER=DESKTOP-PV2MMT2\SQLEXPRESS;DATABASE=Employee;Trusted_Connection=True"

# Create SQLAlchemy engine
quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')

# Execute SQL query and fetch data into a DataFrame
query = 'Select * from Details'
import pandas as pd
df = pd.read_sql(query, engine)
print(df)

# Create the agent
agent = create_pandas_dataframe_agent(llm, df)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    if not question:
        return jsonify({'response': 'Please enter a question.'})
    try:
        response = agent.run(question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': str(e)})

if __name__ == '__main__':
    app.run()
