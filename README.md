# NLP2SQL Toolkit: watsonx™ and IBM® Power® Virtual Server
With the ready-to-use NLP2SQL Toolkit, businesses can simplify data analysis. Whether it's a sales manager, assessing product performance, or a finance team monitor revenue trend, this AI-powered tool makes data analysis more accessible, efficient, and actionable for all.</br>
The Toolkit converts simple text-based questions such as What were the top-selling products last quarter? into SQL queries that retrieve the necessary data. The use of this toolkit eliminates reliance on technical teams, speeding up decision-making processes and significantly cutting down on the time that is required to implement these new features to fruition.
## Reference Architecture

![Screenshot 2025-03-18 at 14 37 51](https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/e068b193-c406-4a24-a47b-46c41a8f5fed)



## Installation
**Step 1:** <br>Login to VM , git clone the toolkit repo (https://github.ibm.com/AIonPower/powervs_watsonx_toolkit.git)</br>

**Step 2:** <br>Ensure Python3.8+ and pip is installed</br></br>
``#python -version``<br/>
OR<br/>
``#python3 -version``<br/>
``#pip version``<br/>

If Python or pip is not installed, download Python from python.org and pip typically come bundled with it.

**Step 3:** Install packages from requirements.txt(present in the code)

``#pip install -r requirements.txt``

<img width="453" alt="image" src="https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/b569e795-b138-490e-9af5-6a9d1f6ea5fd">


Working with different database systems in Python, specific adapters and extension modules are required to establish connections and run database operations.

- **psycopg2:** A database adapter that follows the DB API 2.0 standard, which is designed specifically for PostgreSQL. It is essential for interacting with PostgreSQL databases.</br>
- **oracledb:** A Python extension module that enables seamless connections to Oracle databases, allowing efficient data access and manipulation.</br>
- **hdbcli:** A dedicated Python extension module for SAP HANA, facilitating integration and database operations.</br></br>
By default, the Toolkit supports all three databases: Oracle, PostgreSQL, and SAP HANA. If your project does not involve PostgreSQL, Oracle, or SAP HANA, you can exclude psycopg2, oracledb, or hdbcli from the requirements.txt file, keeping dependencies minimal and relevant.<br>

**Step 4:** Ensure all packages were installed correctly by listing installed packages:

` #pip list`


**Step 5:** Go to the folder “watsonx-integration-server” open the configuration files and update the following parameters

![image](https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/14fec286-a6dd-49f4-867e-6493e90cb1df)

- [apiserver]<br/>
Port: Provide the port number at which the flask server must run. List of available ports on IBM Power Virtual Server : https://cloud.ibm.com/docs/power-iaas?topic=power-iaas-network-security


- [llmurl]<br/>
url: Provide the LLM scoring endpoint deployed on watsonx


- [apikey]<br/>
api_key:  Create a personal API key here : https://cloud.ibm.com/iam/apikeys, and use it to create temporary access tokens.


<img width="500" alt="image" src="https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/d8a79cc8-64a5-4c72-99c1-5449e1482349">

The resp_config.json file defines the expected structured response format from an LLM that interacts with the toolkit. Defining the format allows an LLM to generate structured, machine-readable responses, ensuring easy integration with API layer.<br/>

type: "agent": Indicates that the response is coming from an AI agent.<br/>
sections: A list that contains different types of response elements.<br/>
- First section:<br/>
<img width="500" alt="image" src="https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/6f2c5eb2-4aa5-4f61-9b2a-f402c54f0c0d"></br>
  - type: "text" → This section contains textual data.</br>
  - data: A string message informing the user about retrieved transactions.</br>

- Second section:<br/>
<img width="500" alt="image" src="https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/ef870cb2-e890-422e-a534-f0c039ba35b9"></br>
  - type: "table" → This section is meant to hold tabular data.</br>
  - data: [] (Empty array) → In case no transactions were found.


<img width="452" alt="image" src="https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/e01fc27c-9a3c-4b7c-a7b0-2d7e1cecf875"></br></br>
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


![image](https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/d1d06583-7cc7-4696-aa04-489d39d01bf1)</br>
<img width="213" alt="image" src="https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/048c6fab-dab9-4e12-ace0-fef5a5f836c1"></br>
where </br>
- User: username used to authenticate with the database.
- Password: password associated with the username
- Host: host / IP address where the database is located
- Port: port number where the database is listening for connections
- Dbname: Name of the database and in case of SAP HANA it also serves as the schema name

Open the file "database_integrate.py" and comment the lines based on the databases you are not using (Oracle, PostgreSQL, or SAP HANA):</br>
![image](https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/assets/404635/3022e67a-89a5-49ca-9333-b3dce9bc3ce6)



**Step 7:** Go to the folder “watsonx-integration-server” and run flask application

` #FLASK_APP=flask_api.py FLASK_RUN_HOST=0.0.0.0 FLASK_RUN_PORT=9476 flask run`

**Step 8:** To set up Gen AI Assistant follow the instructions in the below readme link
https://github.ibm.com/AIonPower/powervs_watsonx_toolkit/blob/main/chatbot_ui/README.md
























