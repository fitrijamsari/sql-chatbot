# CHATBOT MYSQL

## Introduction

This project will enable communication in natural language with the database.

![The Concept](img/chat-with-mysql-chain-langchain.jpg)

> [!NOTE]
> This project is not an agent. It is just a sample to direct communicate with the database. If the user asking anything unrelated, it will produce error. No fallback has been establish yet.

The project will run on sample database (Chinook Database). This sample database is provided by the LangChain Documentation.
This is a sample database that represents a digital media store, including tables for artists, albums, media tracks, invoices, and customers. We will use this database to test our chatbot.

## Technology Used

The following modules are used in this project:

- OpenAI
- LangChain
- Chroma

## Getting started

To run this demo project, create an virtual environment and install the src package:

1. Clone the repository:

2. Setup the sample database

The project will use a SQLite connection with Chinook database. Follow these [installation steps](https://database.guide/2-sample-databases-sqlite/) to create Chinook.db in the same directory as this notebook:

- Save [this file](https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql) as Chinook_Sqlite.sql

- First, save the Chinook_Sqlite.sql script to a folder/directory on your computer. That’s a direct link to the script on GitHub.

Now create a database called Chinook. You can do this by connecting to SQLite with the following command:

```bash
sqlite3 Chinook.db
```

- Now you can run the script. To run it from the file, use the following command:

```bash
.read Chinook_Sqlite.sql
```

- Test the database

```bash
SELECT * FROM Artist LIMIT 10;
```

Now, Chinhook.db is in our directory and we can interface with it using the SQLAlchemy-driven SQLDatabase class.

3. create .env files with the following secret keys:

```bash
LANGCHAIN_TRACING_V2='true'
LANGCHAIN_ENDPOINT='https://api.smith.langchain.com'
LANGCHAIN_API_KEY=<your-api-key>

OPENAI_API_KEY=<your-api-key>
GROQ_API_KEY=<your-api-key>
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
streamlit run src/app.py
```

## Challenges

1. The return JSON score of each agent might not be consistent although the PromptTemplate already provide a clear instruction.
2. The time taken to generate final answer by local machine is too long. (note that i just use mac mac1 for this project)

## To Do

1. Convert the notebook into functional component and classes with standard python project structure with logging, config and others.
2. Accept for various other input data format such as pdf and sql.

## Reference & Documentation

1. ![LangChain with SQL Documentation](https://python.langchain.com/docs/use_cases/sql/quickstart/)
2. ![Streamlit Documentation](https://docs.streamlit.io/get-started/tutorials/create-an-app)
