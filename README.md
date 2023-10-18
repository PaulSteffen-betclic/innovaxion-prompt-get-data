# innovaxion-prompt-get-data
Get data from database using Large Language Model

## How to use it

### Setup (do it only 1 time)
1. If you're note in the directory of the project, head back over to the command line and navigate to your `innovaxion-prompt-get-data` folder.  
2. Create a virtual environment with all the required dependencies:  
   `conda env create -f environment.yml`
3. Add a folder within your `innovaxion-prompt-get-data` folder called `.streamlit`.  
Using the command line, you can do this by entering `mkdir .streamlit`.
4. Within the `.streamlit` folder, add a file called `secrets.toml`.  
Using the command line, you can do this by first navigating to the `.streamlit` folder via `cd .streamlit` and then entering `touch secrets.toml`.
5. Fill this `secrets.toml` file:  
```
OPENAI_API_KEY = "sk-2v...X"

[connections.snowpark]
user = "<username>"
password = "<password>"
warehouse = "<warehouse>"
role = "<role>"
account = "<account-id>"
```
To use SSO, replace the use of password by `authenticator = "externalbrowser"`.  
Need to be relevent to request the schema the schema `INOVAXION` in the database `DATASCIENCE_DEV`.

### Quick start (do it for each run)
1. If you're note in the directory of the project, head back over to the command line and navigate to your `innovaxion-prompt-get-data` folder.
2. Activate the virtual environment.
   `conda activate prompt-get-data`
3. Run the Streamlit app via streamlit.
   `treun frosty_app.py`

## How does it work
1. Give to your LLM (ChatGPT here), a short description of the tables involved for your project (manually), including the type of each column in the tables (automatically).
2. Ask him a question related to the data in your tables.
3. The LLM send you an SQL query, that you execute automatically to get your answer.


Based on https://quickstarts.snowflake.com/guide/frosty_llm_chatbot_on_streamlit_snowflake/#0
