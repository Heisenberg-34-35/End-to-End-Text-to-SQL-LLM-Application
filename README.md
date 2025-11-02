# End-to-End Text-to-SQL LLM Application

This project is a powerful and intuitive web application that converts natural language questions into SQL queries. It allows non-technical users to interact with a database and retrieve information simply by asking questions in plain English.

The application is built using Streamlit for the user interface, LangChain for LLM orchestration, and the Groq API (powering Llama 3) for incredibly fast text-to-SQL conversion.


## 🚀 Features

* **Intuitive Web UI:** A clean and simple interface built with Streamlit.
* **Natural Language to SQL:** Asks questions like "Who has the highest marks?" instead of writing `SELECT NAME, MARKS FROM STUDENT ORDER BY MARKS DESC LIMIT 1`.
* **High-Speed Inference:** Uses the Groq API for near-instantaneous query generation from the Llama 3 model.
* **Accurate Schema Awareness:** Utilizes prompt engineering to make the LLM aware of the database schema (table name, columns) for high accuracy.
* **Direct Database Execution:** Runs the generated SQL query directly against the included `student.db` (SQLite) file.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM & Orchestration:** LangChain (`langchain-groq`, `ChatPromptTemplate`)
* **LLM Provider:** Groq (using `llama3-8b-8192` model)
* **Database:** SQLite
* **Environment:** Python 3.11, Pipenv

## ⚙️ How It Works

1.  **User Input:** The user enters an English query into the Streamlit text box.
2.  **Prompt Engineering:** LangChain takes the query and combines it with a `ChatPromptTemplate`. This template (in `app.py`) instructs the LLM, provides the database schema (`STUDENT` table with `NAME`, `COURSE`, `SECTION`, `MARKS`), and gives examples.
3.  **LLM Call:** The formatted prompt is sent to the Llama 3 model via the Groq API.
4.  **SQL Generation:** The LLM returns a valid SQL query string.
5.  **Database Query:** The application's `return_sql_response` function connects to `student.db` and executes the generated SQL query.
6.  **Display Results:** The fetched data is displayed to the user in the Streamlit app.
