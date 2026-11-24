import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# Read MySQL configuration from environment variables
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "").replace("@", "%40")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "")

# SQLAlchemy Engine setup using environment variables
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# Existing Tools
@tool
def calculator(expression: str) -> str:
    """Solve mathematical expressions"""
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression"


@tool
def word_counter(text: str) -> str:
    """Counts words in a sentence"""
    return f"Total words: {len(text.split())}"


# MySQL Tool
@tool
def execute_sql_query(query: str) -> str:
    """Executes a read-only SQL SELECT query against the MySQL database using SQLAlchemy."""
    try:
        if not query.strip().lower().startswith("select"):
            return "Error: Only SELECT queries are allowed for security reasons."

        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            keys = result.keys()
            results_as_dict = [dict(zip(keys, row)) for row in rows]

            return str(results_as_dict) if results_as_dict else "No records found."
    except Exception as e:
        return f"MySQL Database Error: {str(e)}"


@tool
def search_knowledge_base(query: str) -> str:
    """Searches internal company HR policies and documentations."""
    mock_docs = {
        "leave policy": "Employees get 18 paid leave days per year.",
        "remote work": "Hybrid work is allowed up to 2 days a week with manager approval.",
        "reimbursement": "Submit travel receipts within 30 days via HR portal."
    }

    for key, text in mock_docs.items():
        if key in query.lower():
            return f"Found in HR Policy: {text}"

    return "No relevant internal documentation found."


@tool
def get_customer_details(customer_id: str) -> str:
    """Fetches customer profile details from CRM using Customer ID."""
    try:
        if customer_id.upper() == "CUST-101":
            return "{'name': 'Aarav Sharma', 'plan': 'Enterprise Tier', 'status': 'Active'}"
        return f"Customer ID '{customer_id}' not found."
    except Exception as e:
        return f"CRM Error: {str(e)}"


@tool
def send_email_notification(recipient: str, subject: str, message_body: str) -> str:
    """Sends an automated email notification to a given email address."""
    if "@" not in recipient:
        return "Error: Invalid email address format."

    return f"Email successfully sent to {recipient} with subject '{subject}'."


