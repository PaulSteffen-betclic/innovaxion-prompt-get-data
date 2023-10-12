import streamlit as st

ITEMS_TABLE_NAME = "DATASCIENCE_DEV.INOVAXION.ITEMS"
ITEMS_TABLE_DESCRIPTION = """
This table has various sports booking metrics for football events of the season 2018-2019 of French Ligue 1. 
The date of the event, the event name (concatenation of home team (HT) and away team (AT)), the number of goals for each 
team, the result of the game (A for Away team, H for Home team, D for Draw), the associated odds and an Id is available.
The user may use vocabulary as “selection” for bets.
"""

INTERACTIONS_TABLE_NAME = "DATASCIENCE_DEV.INOVAXION.INTERACTIONS"
INTERACTIONS_TABLE_DESCRIPTION = """
This table refers to the bets of users. 
It includes the user ids, the match they bet on, the date they betted, the selection they choose and the bet amount. 
"""

GEN_SQL = """
You will be acting as an AI Snowflake SQL expert named Frosty.
Your goal is to give correct, executable SQL queries to users.
You will be replying to users who will be confused if you don't respond in the character of Frosty.
You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
The user will ask questions; for each question, you should respond and include a SQL query based on the question and the table. 

{items_context}

{interactions_context}

Here are 6 critical rules for the interaction you must abide:
<rules>
1. You MUST wrap the generated SQL queries within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
4. Make sure to generate a single Snowflake SQL code snippet, not multiple. 
5. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names.
6. DO NOT put numerical at the very front of SQL variable.
</rules>

Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
and wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```

For each question from the user, make sure to include a query in your response.

Now to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
Then provide 3 example questions using bullet points.
"""

@st.cache_data(show_spinner=False)
def get_table_context(table_name: str, table_description: str, metadata_query: str = None):
    table = table_name.split(".")
    conn = st.experimental_connection("snowpark")
    columns = conn.query(f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
        """,
    )
    columns = "\n".join(
        [
            f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
            for i in range(len(columns["COLUMN_NAME"]))
        ]
    )
    context = f"""
Here is the table name <tableName> {'.'.join(table)} </tableName>

<tableDescription>{table_description}</tableDescription>

Here are the columns of the {'.'.join(table)}

<columns>\n\n{columns}\n\n</columns>
    """
    if metadata_query:
        metadata = conn.query(metadata_query)
        metadata = "\n".join(
            [
                f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                for i in range(len(metadata["VARIABLE_NAME"]))
            ]
        )
        context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"
    return context

def get_system_prompt():
    items_table_context = get_table_context(
        table_name=ITEMS_TABLE_NAME,
        table_description=ITEMS_TABLE_DESCRIPTION,
    )
    interactions_table_context = get_table_context(
        table_name=INTERACTIONS_TABLE_NAME,
        table_description=INTERACTIONS_TABLE_DESCRIPTION,
    )
    return GEN_SQL.format(items_context=items_table_context,
                          interactions_context=interactions_table_context)

# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for Frosty")
    st.markdown(get_system_prompt())