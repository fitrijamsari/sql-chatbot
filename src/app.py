import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def init_database(host: str, port: str, user: str, password: str, database: str):
    try:
        db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"  # for mysql
        # db_uri = f"sqlite:///{database}"  # for sqlite
        db = SQLDatabase.from_uri(db_uri)
    except Exception as e:
        st.error(e)
    return db


# using few-shot prompt, the get_sql_chain will return the SQL command for the selected question
def get_sql_chain(db: SQLDatabase):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    If the user's question is not related to the table schema, just write "You question is not related to the database. Please ask a related question to the database".
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
        
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)

    if model == "gpt-3.5-turbo":
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    else:
        llm = ChatGroq(model_name=model, temperature=0, groq_api_key=GROQ_API_KEY)

    def get_schema(_):
        return db.get_table_info()

    sql_chain = (
        RunnablePassthrough.assign(schema=get_schema) | prompt | llm | StrOutputParser()
    )
    return sql_chain


def get_response(model: str, user_query: str, chat_history: list, db: SQLDatabase):
    sql_chain = get_sql_chain(db)

    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    Double check on the sql query. Make sure the sql query is only from the available table schema. 
    If the sql query is not from the table schema, just write "No results found. The SQL query is not from the table schema. Please ask a related question to the table schema".


    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)

    if model == "gpt-3.5-turbo":
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    elif model == "gpt-4-turbo":
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    else:
        llm = ChatGroq(model_name=model, temperature=0, groq_api_key=GROQ_API_KEY)

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    response = chain.invoke({"question": user_query, "chat_history": chat_history})

    return response


# initialize chat_history in streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(
            content="Hello, I'am your SQL Assistant. Ask me anything about your database?"
        ),
    ]

st.set_page_config(page_title="Chatbot with MySQL", page_icon=":robot:")

st.title("Chatbot with MySQL")

with st.sidebar:
    st.sidebar.title("Settings")
    st.write(
        "This is a simple chat application to communicate with MySQL database. Connect to the database and start chatting!"
    )

    model = st.sidebar.selectbox(
        "Choose a model",
        [
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it",
            "gpt-3.5-turbo",
            "gpt-4-turbo",
        ],
    )

    st.text_input("Host", value="localhost", key="host")
    st.text_input("Port", value="3306", key="port")
    st.text_input("User", value="root", key="user")
    st.text_input("Password", value="admin", key="password")
    st.text_input("Database", value="Chinook", key="database")

    if st.button("Connect", key="connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                host=st.session_state.host,
                port=st.session_state.port,
                user=st.session_state.user,
                password=st.session_state.password,
                database=st.session_state.database,
            )
            st.session_state.db = db
            st.success("Connected to database!")

# streamlit chat display
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input(
    placeholder="Type your message here...", key="input", on_submit=None
)
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    # # to get the native SQL response
    # with st.chat_message("AI"):
    #     sql_chain = get_sql_chain(st.session_state.db)
    #     response = sql_chain.invoke(
    #         {"chat_history": str(st.session_state.chat_history), "question": user_query}
    #     )
    #     st.markdown(response)

    # get the natural language response
    with st.chat_message("AI"):
        try:
            response = get_response(
                model, user_query, st.session_state.chat_history, st.session_state.db
            )
            st.markdown(response)

        except Exception as e:
            st.markdown(
                "No results found. Please ask a related question to the table schema."
            )

    st.session_state.chat_history.append(AIMessage(content=response))
