import streamlit as st
import sqlite3
import pandas as pd
import ollama
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Conversational BI", layout="wide")
st.title("Conversational Business Intelligence")

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
conn = sqlite3.connect("data/sales.db")

# -------------------------------------------------
# CACHED RAG SCHEMA (PRECOMPUTED OFFLINE)
# -------------------------------------------------
RELEVANT_SCHEMA = """
Table: customers
Columns:
- customer_id: unique customer identifier
- name: customer name
- country: customer country
- signup_date: date when customer signed up
- segment: business segment

Table: orders
Columns:
- order_id: unique order identifier
- customer_id: customer who placed the order
- product_id: product ordered
- order_date: date of order
- quantity: number of items
- total_amount: total order value
"""

# -------------------------------------------------
# HARD SQL EXTRACTION (CRITICAL SAFETY LAYER)
# -------------------------------------------------
def extract_sql(text):
    """
    Extract the first valid SELECT statement from LLM output.
    Prevents explanations or multiple statements from reaching SQLite.
    """
    lines = text.splitlines()
    sql_lines = []
    collecting = False

    for line in lines:
        line = line.strip()

        if line.upper().startswith("SELECT"):
            collecting = True
            sql_lines.append(line)
            continue

        if collecting:
            if line.upper().startswith(
                ("FROM", "JOIN", "INNER", "LEFT", "RIGHT", "WHERE",
                 "GROUP", "ORDER", "HAVING", "LIMIT")
            ):
                sql_lines.append(line)
            else:
                break

    sql = " ".join(sql_lines)

    if not sql.upper().startswith("SELECT"):
        raise ValueError("LLM did not return valid SQL")

    return sql

# -------------------------------------------------
# NL → SQL FUNCTION (CACHED RAG + DEFENSIVE PROMPT)
# -------------------------------------------------
def nl_to_sql(question):
    prompt = f"""
You are a SQL generator.

IMPORTANT:
- Your output will be executed directly on a database.
- Output MUST contain ONLY ONE valid SQL SELECT statement.
- Do NOT include explanations, comments, headings, or extra text.
- Do NOT include multiple queries.

Database schema:
{RELEVANT_SCHEMA}

User question:
"{question}"

Return ONLY the SQL query.
"""

    response = ollama.chat(
        model="phi",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]
    return extract_sql(raw_output)

# -------------------------------------------------
# CLEAN COLUMN NAMES (BUSINESS FRIENDLY)
# -------------------------------------------------
def clean_column_names(df):
    df.columns = [
        col.lower()
           .replace("(", "")
           .replace(")", "")
           .replace("count", "total")
           .replace("_id", "")
           .replace(" ", "_")
        for col in df.columns
    ]
    return df

# -------------------------------------------------
# AUTO CHART SELECTION
# -------------------------------------------------
def auto_chart(df):
    if df.shape[1] == 2:
        col1, col2 = df.columns

        if "date" in col1 or "date" in col2:
            return px.line(df, x=col1, y=col2)

        return px.bar(df, x=col1, y=col2)

    return None

# -------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------
question = st.text_input("Ask a business question:")

if question:
    try:
        with st.spinner("Analyzing your question..."):
            # Generate SQL
            sql = nl_to_sql(question)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # Execute SQL
            df = pd.read_sql_query(sql, conn)
            df = clean_column_names(df)

        st.subheader("Query Result")

        # Metric card for single value
        if df.shape == (1, 1):
            st.metric(
                label=df.columns[0].replace("_", " ").title(),
                value=df.iloc[0, 0]
            )
        else:
            chart = auto_chart(df)
            if chart:
                st.plotly_chart(chart, use_container_width=True)

            st.dataframe(df)

    except Exception as e:
        st.error(f"Error: {str(e)}")
