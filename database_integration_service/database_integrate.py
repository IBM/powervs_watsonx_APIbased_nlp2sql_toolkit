import json
import requests
import oracledb
import psycopg2
from hdbcli import dbapi
from datetime import date, datetime
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
import os
import configparser


def db_retrieve_data(sql_query):
    print('Inside db_retrieve_data and reading config.ini')
    print('os.getcwd():',os.getcwd())
    os.chdir('../database_integration_service')
    print('os.getcwd():',os.getcwd())
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extract database connection variables
    dbtype = int(config.get('database', 'dbtype'))
    host = config.get('database', 'host')
    port = int(config.get('database', 'port'))
    username = config.get('database', 'user')
    password = config.get('database', 'password')
    dbname = config.get('database', 'dbname')
    
    print("read all params")

    if dbtype == 1:
        rows = db_oracle(sql_query,host,port,username,password,dbname)
    elif dbtype ==2:
        rows  = db_postgres(sql_query,host,port,username,password,dbname)
    elif dbtype == 3:
        rows  == db_hana(sql_query,host,port,username,password,dbname)
    else:
        print("Unsupported dbtype value")
    return rows


def db_oracle(sql_query,host,port,username,password,dbname):
    JSON_SQL_QUERY = "select JSON_OBJECT(*) from (" + sql_query+ ")"
    print(f'Updated SQL : {JSON_SQL_QUERY}')
    print(f"\nQuerying database...")

    dsn_name = host+':'+str(port)+'/'+dbname
    db_conn = oracledb.connect(user=username, password=password, dsn=dsn_name)
    db_cursor = db_conn.cursor()
    db_cursor.execute(JSON_SQL_QUERY)

    rows = db_cursor.fetchall()

    orows = []
    for row in rows:
        r = json.loads(row[0])
        r = {k.lower(): v for k, v in r.items()}
        tt = ( r,)
        orows.append(tt) 

    for t in orows:
        print(t);

    db_cursor.close()
    db_conn.close()
    return orows 


def db_postgres(sql_query,host,port,username,password,dbname):
    #JSON_SQL_QUERY = "select row_to_json(row) from(" + sql_query + ") row;"
    JSON_SQL_QUERY = "select JSON_OBJECT(*) from (" + SQL_QUERY + ")"
    
    print(f'Updated SQL : {JSON_SQL_QUERY}')
    print(f"\nQuerying datbase...")
    
    db_conn = psycopg2.connect(
        dbname="digitalbank",
        user="postgres",
        password="mynewpassword",
        host="postgresql",
        port="5432"
    )

    db_cursor = db_conn.cursor()
    db_cursor.execute(JSON_SQL_QUERY)
    rows = db_cursor.fetchall()

    #print("\nResponse from database:: ")
    for row in rows:
        print(row)

    db_cursor.close()
    db_conn.close()
    return rows

def db_hana(sql_query,host,port,username,password,dbname):
    ##########    HANA DB CONNECTION ########
    # Example: "your-hana-db-url.hana.ondemand.com"

    # Connect to SAP HANA Cloud
    db_conn = dbapi.connect(
        address=host,
        port=port,
        user=username,
        password=password,
        encrypt=True,           # Use encryption for cloud connections
        sslValidateCertificate=False  # Set to False to skip certificate validation, not recommended for production
    )

    schema_query = "SET SCHEMA "+dbname 
    db_cursor = db_conn.cursor()
    db_cursor.execute(schema_query)   

    db_cursor.execute(SQL_QUERY)

    rows = db_cursor.fetchall()

    print("\nResponse from database:: ")
    for row in rows:
        print(row)
    #---------- Convert obtained rows in desired JSON format 
    #  Get column names from cursor description
    columns = [desc[0] for desc in db_cursor.description]
    columnhdr =[]
    for element in columns:
        element = element.lower()
	#print('element :',element)
        columnhdr.append(element)
    
    for i in columnhdr:
        print(i)
    #  Format the results into a list of dictionaries
    results = []
    for row in rows:
        results.append(dict(zip(columnhdr, row)))

    #  Convert the list of dictionaries to JSON
    json_result = json.dumps(results, default=custom_serializer, indent=4)

    #  Print or use the JSON result
    #print('\n\njson_result\n',json_result)
    
    data = json.loads(json_result)
   
    #  Convert each dictionary to the desired format and store in a variable
    formatted_output = []
    for item in data:
        formatted_output.append((item,))  # Wrap the item in a tuple
    print('after the for , printing formatted O/P')
    for row in formatted_output:
        print(row)
        
    #  Join the tuples into a single string with newline characters
    result = "\n".join(str(entry) for entry in formatted_output)

    db_cursor.close()
    db_conn.close()

    return formatted_output



#Test the DB  code
#sql_query = "SELECT column_name FROM all_tab_columns WHERE table_name = USERS ORDER BY column_name"
#sql_query = "select * from accounts, users where accounts.u_id=users.user_id and accounts.balance>1000"
#rows = db_retrieve_data(sql_query)
#print("rows") 
