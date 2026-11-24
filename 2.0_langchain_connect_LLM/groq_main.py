from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b"
)

question = input("Aap kya puchna chahte hain? : ")

response = llm.invoke(question)

print("\nAnswer:")
print(response.content)