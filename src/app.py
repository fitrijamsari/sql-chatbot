import os

import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def init_database(host: str, port: str, user: str, password: str, database: str):
    # db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"  # for mysql
    db_uri = f"sqlite:///{database}"  # for sqlite
    db = SQLDatabase.from_uri(db_uri)
    return db


st.set_page_config(page_title="Chatbot with MySQL", page_icon=":robot:")

st.title("Chatbot with MySQL")

with st.sidebar:
    st.subheader("Settings")
    st.write(
        "This is a simple chat application to communicate with MySQL database. Connect to the database and start chatting!"
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

st.chat_input(placeholder="Type your message here...", key="input", on_submit=None)
