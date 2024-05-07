# CHATBOT MYSQL

## Introduction

This project will implement the combination ideas of Adaptive RAG, Corrective RAG and Self-RAG into a RAG agent to improve the RAG workflow:

- **Routing:** Adaptive RAG ([paper](https://arxiv.org/abs/2403.14403)). Route questions to different retrieval approaches.
- **Fallback:** Corrective RAG ([paper](https://arxiv.org/pdf/2401.15884.pdf)). Fallback to web search if docs are not relevant to query.
- **Self-correction:** Self-RAG ([paper](https://arxiv.org/abs/2310.11511)). Fix answers w/ hallucinations or don’t address question.

The concept is the following diagram:

![The Concept](langgraph_adaptive_rag.png)

## Technology Used

The following modules are used in this project:

- OpenAI
- LangChain
- Chroma

## Getting started

To run this demo project, create an virtual environment and install the src package:

1. Clone the repository:

2. Download the llama3 model locally first. [Llama3 Model](https://ollama.com/)

3. Test run the llama3 on terminal. Open the terminal and run:

```bash
ollama run llama3
```

3. create .env files with the following secret keys:

```bash
LANGCHAIN_TRACING_V2='true'
LANGCHAIN_ENDPOINT='https://api.smith.langchain.com'
LANGCHAIN_API_KEY=<your-api-key>
```

4. Install Dependencies

```bash
pip install -r requirements.txt
```

5. Run the various jupyter notebook

## Challenges

1. The return JSON score of each agent might not be consistent although the PromptTemplate already provide a clear instruction.
2. The time taken to generate final answer by local machine is too long. (note that i just use mac mac1 for this project)

## To Do

1. Convert the notebook into functional component and classes with standard python project structure with logging, config and others.
2. Accept for various other input data format such as pdf and sql.
