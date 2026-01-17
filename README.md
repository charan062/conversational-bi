\# Conversational Business Intelligence



A conversational Business Intelligence (BI) system that allows non-technical users to query a relational database using natural language.  

The system converts English questions into SQL queries using a local Large Language Model (LLM) and displays results as tables or metrics.



---



\## Problem Statement



Traditional BI tools require users to know SQL or depend on analysts for data queries.  

This creates friction for business users who want quick answers from data.



This project solves that problem by enabling:

\- Natural language questions

\- Automatic SQL generation

\- Direct execution on a relational database

\- Clear tabular or metric-based outputs



---



\## What This System Does



\- Takes a business question in plain English

\- Converts it into a valid SQL `SELECT` query

\- Executes the query on a SQLite database

\- Displays results as:

&nbsp; - Metric cards (for single values)

&nbsp; - Tables and charts (for multi-row results)



Example questions:

\- “How many customers are there?”

\- “List customer names and countries”

\- “Show total orders”



---



\## High-Level Architecture



1\. \*\*Streamlit UI\*\* for user interaction  

2\. \*\*Local LLM (Ollama – Phi model)\*\* for NL → SQL conversion  

3\. \*\*Cached schema grounding (RAG-inspired)\*\* to reduce hallucination  

4\. \*\*SQLite database\*\* for structured data  

5\. \*\*Defensive SQL extraction\*\* to ensure safe execution  



The system runs fully offline with no paid APIs.



---



\## Tech Stack



\- Python

\- Streamlit (UI)

\- SQLite (Database)

\- Ollama (Local LLM runtime)

\- Phi model (lightweight, low-memory)

\- Pandas (query execution \& formatting)

\- Plotly (visualizations)



---



\## How to Run the Project Locally



\### 1. Clone the repository

```bash

git clone https://github.com/charan062/conversational-bi.git

cd conversational-bi



