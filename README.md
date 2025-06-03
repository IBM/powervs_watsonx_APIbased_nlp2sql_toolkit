# NLP2SQL Toolkit: watsonx™ and IBM® Power® Virtual Server
With the ready-to-use NLP2SQL Toolkit, businesses can simplify data analysis. Whether it's a sales manager, assessing product performance, or a finance team monitor revenue trend, this AI-powered tool makes data analysis more accessible, efficient, and actionable for all.</br>
The Toolkit converts simple text-based questions such as What were the top-selling products last quarter?  - into SQL queries that retrieve the necessary data. The use of this toolkit eliminates reliance on technical teams, speeding up decision-making processes and significantly cutting down on the time that is required to implement these new features to fruition.
## Reference Architecture

<img width="1010" alt="image" src="https://github.com/user-attachments/assets/8b160e1e-17b8-4c04-872a-27a4a93bf35e" />


The above reference architecture diagram illustrates the Toolkit architecture for NLP2 SQL, highlighting its modular design and key considerations. 

RedHat OpenShift Container Platform is optional, and Toolkit can be installed directly on RHEL as explained in further sections.

The overall structure is divided into several components: 
- Databases which have mission critical data on Power VS
- An Enterprise Application for example a core banking enterprise application
- API-based NLP2SQL Toolkit and 
- watsonx AI Services. 

Databases supported include SAP HANA, Oracle and Postgres SQL which interact with the Enterprise Application. 

The Toolkit comprises three main layers: 
- Gen AI Asst - UI layer
- API Layer
- Database Layer. 

These layers facilitate API calls and NLP queries, converting natural language inputs into SQL statements. 

The watsonx.ai services, provided by IBM Cloud SaaS, include foundation models, prompt lab, and watsonx machine learning, which support the Toolkit by deploying pre-packaged LLM models and tuning them as needed. 

Overall, the diagram conveys a modular and scalable architecture designed to integrate watsonx.ai and PowerVS functionalities seamlessly.




## Installation
**Step 1:** <br>Login to VM , git clone the toolkit repo : (https://github.com/IBM/powervs_watsonx_APIbased_nlp2sql_toolkit)</br>

**Step 2:** <br>Ensure Python3.8+ and pip is installed</br></br>
``#python -version``<br/>
OR<br/>
``#python3 -version``<br/>
``#pip version``<br/>

If Python or pip is not installed, download Python from python.org and pip typically come bundled with it.

**Step 3:** Install packages from requirements.txt(present in the code)

``#pip install -r requirements.txt``

<img width="426" alt="image" src="https://github.com/user-attachments/assets/2abae655-201a-464b-8c0e-07d3a4dfc5e5" />



Working with different database systems in Python, specific adapters and extension modules are required to establish connections and run database operations.

- **psycopg2:** A database adapter that follows the DB API 2.0 standard, which is designed specifically for PostgreSQL. It is essential for interacting with PostgreSQL databases.</br>
- **oracledb:** A Python extension module that enables seamless connections to Oracle databases, allowing efficient data access and manipulation.</br>
- **hdbcli:** A dedicated Python extension module for SAP HANA, facilitating integration and database operations.</br></br>
By default, the Toolkit supports all three databases: Oracle, PostgreSQL, and SAP HANA. If your project does not involve PostgreSQL, Oracle, or SAP HANA, you can exclude psycopg2, oracledb, or hdbcli from the requirements.txt file, keeping dependencies minimal and relevant.<br>

**Step 4:** Ensure all packages were installed correctly by listing installed packages:

` #pip list`


**Step 5:** Go to the folder “watsonx-integration-server” open the configuration files and update the following parameters

<img width="721" alt="image" src="https://github.com/user-attachments/assets/1947549c-5bdf-49d7-a3b8-ba67956f28ed" />


- [apiserver]<br/>
Port: Provide the port number at which the flask server must run. List of available ports on IBM Power Virtual Server : https://cloud.ibm.com/docs/power-iaas?topic=power-iaas-network-security


- [llmurl]<br/>
url: Provide the LLM scoring endpoint deployed on watsonx


- [apikey]<br/>
api_key:  Create a personal API key here : https://cloud.ibm.com/iam/apikeys, and use it to create temporary access tokens.


<img width="728" alt="image" src="https://github.com/user-attachments/assets/a9a55a5c-3251-449b-bdf6-997ab2aea543" />


The resp_config.json file defines the expected structured response format from an LLM that interacts with the toolkit. Defining the format allows an LLM to generate structured, machine-readable responses, ensuring easy integration with API layer.<br/>

type: "agent": Indicates that the response is coming from an AI agent.<br/>
sections: A list that contains different types of response elements.<br/>
- First section:<br/>
<img width="731" alt="image" src="https://github.com/user-attachments/assets/a6d29b64-9ef1-4192-99ee-ab8c784ec372" />

  - type: "text" → This section contains textual data.</br>
  - data: A string message informing the user about retrieved transactions.</br>

- Second section:<br/>
<img width="725" alt="image" src="https://github.com/user-attachments/assets/25ff6cf5-76d0-49dc-833b-eae3cd9f65ba" />

  - type: "table" → This section is meant to hold tabular data.</br>
  - data: [] (Empty array) → In case no transactions were found.


<img width="552" alt="image" src="https://github.com/user-attachments/assets/bae9e4e7-0e60-4b03-8fd7-f9af50c4f252" />

The Json structure here constitutes the body of the request sent to watsonx.ai service . Below are the Key description : - <br/>
- input: Contains a text prompt formatted in a specific syntax indicating roles and their inputs. Can include Database schema with sample NLP statement and equivalent SQL Query<br/>
- parameters: This object contains various parameters for the text generation process:</br>
  - decoding_method: The method used to generate the text. In this case, it's set to "greedy".</br>
  - max_new_tokens: The maximum number of new tokens (words) to generate. Here, it's set to 100.</br>
  - repetition_penalty: A value that discourages the model from repeating the same text. Here, it's set to 1.</br>
- model_id: The ID of the model to use for text generation</br>
- project_id: The ID of the project associated with the model. </br>
- moderations: This object contains settings for moderating the generated text. Here, it includes settings for handling sensitive information (PII) and harmful content (HAP). Both are set to mask any sensitive information with a threshold of 0.5.</br>


**Step 6:** Go to the folder “database-integration-service” open the db configuration files and update accordingly 


<img width="562" alt="image" src="https://github.com/user-attachments/assets/5debba0c-a0ba-4bb0-8770-1255ede56f41" />

Below are the values for databases: - 
- dbtype  = 1 for Oracle DB
- dbtype  = 2 for postgres
- dbtype  = 3 for HANA DB


where </br>
- User: username used to authenticate with the database.
- Password: password associated with the username
- Host: host / IP address where the database is located
- Port: port number where the database is listening for connections
- Dbname: Name of the database and in case of SAP HANA it also serves as the schema name

Open the file "database_integrate.py" and comment the lines based on the databases you are not using (Oracle, PostgreSQL, or SAP HANA):</br>
<img width="715" alt="image" src="https://github.com/user-attachments/assets/01d79ecd-b6ef-417f-8236-b79fd843a481" />



**Step 7:** Go to the folder “watsonx-integration-server” and run flask application

` #FLASK_APP=flask_api.py FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=9476 flask run`

Sample Output:


<img width="738" alt="image" src="https://github.com/user-attachments/assets/5aa04d67-ac7c-4441-8c37-a030d463d367" />


**Step 8:** To set up Gen AI Assistant follow the instructions in the below readme link
https://github.com/IBM/powervs_watsonx_APIbased_nlp2sql_toolkit/blob/main/chatbot_ui/README.md
























