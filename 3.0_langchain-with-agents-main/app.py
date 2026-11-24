import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from tools import (
    calculator, 
    word_counter, 
    execute_sql_query, 
    search_knowledge_base, 
    get_customer_details, 
    send_email_notification, 
    
)

# Load environment variables
load_dotenv()

# Google API Key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini model initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=GOOGLE_API_KEY, 
    temperature=0
)

tools = [
    calculator, 
    word_counter, 
    execute_sql_query, 
    search_knowledge_base, 
    get_customer_details, 
    send_email_notification, 

]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant.\n"
            "You can answer questions using your own knowledge.\n"
            "Use tools only when necessary.\n"
            "If a question requires calculation, use the calculator tool.\n"
            "If a question asks for word count, use the word_counter tool.\n"
            "If asked about SQL queries or MySQL database, use execute_sql_query tool.\n"
            "If asked about internal HR policies or leaves, use search_knowledge_base tool.\n"
            "If asked about CRM or customer details, use get_customer_details tool.\n"
            "If requested to send an email, use send_email_notification tool.\n"
           
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

def myoutput(query):
    result = agent_executor.invoke({"input": query})
    return result["output"]

# Streamlit UI
st.set_page_config(page_title="AI Agent")
st.title("🤖 Gemini Agent Bot (Secure .env Configuration)")

query = st.text_input("Ask something")

if st.button("Ask Agent"):
    if query:
        response = myoutput(query)
        st.subheader("Response")
        st.write(response)