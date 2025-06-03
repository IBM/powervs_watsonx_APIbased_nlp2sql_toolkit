import oracledb
import json
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database_integration_service')))
from database_integrate import db_retrieve_data

from dotenv import load_dotenv
import configparser



config = configparser.ConfigParser()
config.read('config.ini')

# Access LLM URL
url = config['llmurl']['url']
print('URL:',url)

def watsonx_integrate(user_query):
    os.chdir('../watsonx-integration-server')

    print(f'User query: \n {user_query}')
    load_dotenv()
    AUTHENTICATION_TOKEN = os.getenv("WATSONX_ACCESS_TOKEN")
 
    body_file = "llm_params_config.json"
    try:
        with open(body_file, "r") as file:
            body = json.load(file)
    except FileNotFoundError:
        raise Exception(f"Configuration file {body_file} not found.")
    except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON in {body_file}: {e}")
    # Replace the {user_query} placeholder in the input
    body["input"] = body["input"].replace("{user_query}", user_query)

 
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTHENTICATION_TOKEN}"
    }

    response = requests.post(
           url,
           headers=headers,
           json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    
    data = response.json()

    print(f'Response from WatsonX::\n {data}')
    sql_resp = data['results']


    SQL_QUERY = sql_resp[0]['generated_text'].split(';')[0]
    print(f"\nWatsonX generated SQL:: {SQL_QUERY}")
    JSON_SQL_QUERY = "select JSON_OBJECT(*) from (" + SQL_QUERY + ")"
    print(f'Updated SQL : {JSON_SQL_QUERY}')
    
    orows = db_retrieve_data(SQL_QUERY)
    return orows 
