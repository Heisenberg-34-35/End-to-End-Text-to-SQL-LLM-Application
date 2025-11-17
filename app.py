import os
import sqlite3
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# SQL GENERATING FUNCTION USING CHATGROQ LLM, GROQ API KEY CHAINED WITH PROMPT(CHATPROMPTTEMPLATE) USING STROUTPUTPARSER
def get_sql_query(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
                    You are an expert in converting English questions to SQL query!
                    The SQL database has the name STUDENT and has the following columns - NAME, COURSE, 
                    SECTION and MARKS. For example, 
                    Example 1 - How many entries of records are present?, 
                        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
                    Example 2 - Tell me all the students studying in Data Science COURSE?, 
                        the SQL command will be something like this SELECT * FROM STUDENT 
                        where COURSE="Data Science"; 
                    also the sql code should not have ``` in beginning or end and sql word in output.
                    Now convert the following question in English to a valid SQL Query: {user_query}. 
                    No preamble, only valid SQL please
                                                       """)
    model="llama-3.1-8b-instant"
    llm = ChatGroq(
    groq_api_key = os.environ.get("GROQ_API_KEY"),
    model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    return response

# FUNCTION TO CHECK IF THE REQUESTED QUERY BY USER IS DESTRUCTIVE IN NATURE OR NOT OR TO AVOID ANY ALTERATIONS TO OUR DATABASE
def return_sql_response(sql_query):
    
    if not sql_query.lstrip().upper().startswith("SELECT"):
        st.error("Operation not allowed. Only read-only (SELECT) queries are permitted.")
        return None
    
    database = "student.db"
    try:
        with sqlite3.connect(database) as conn:
            return conn.execute(sql_QUERY).fetchall()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return None


# MAIN FUNCTION THAT CALLS SQL GENERATING FUNCTION AND OUTPUTS THE SQL QUERY
def main():
    st.set_page_config(page_title="Text To SQL")
    st.header("Talk to your Database!")

    user_query=st.text_input("Input:")
    submit=st.button("Enter")

    if submit:
        with st.spinner("Generating SQL and fetching results..."):
            sql_query = get_sql_query(user_query)
 
            if sql_query:
                st.subheader(f"Generated Query: `{sql_query}`")

                database = "student.db"
                try:
                    with sqlite3.connect(database) as conn:
                        df = pd.read_sql_query(sql_query, conn)
                        st.dataframe(df)
                except sqlite3.Error as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Could not generate SQL query.")

    # Sidebar Codes
    st.sidebar.title("Tired of raising tickets or requesting data analysts for data?")
    st.sidebar.markdown("---")
    st.sidebar.info("Now you don't have to sit and wait for someone to fetch you data, just ask simple questions, observe the data and start with your analysis!")
    st.sidebar.markdown("---")

if __name__ == '__main__':
    main()
