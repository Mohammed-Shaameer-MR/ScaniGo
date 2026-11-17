# Clean console viewing
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Hide TensorFlow warnings
import tensorflow as tf
tf.get_logger().setLevel("ERROR")

from dotenv import load_dotenv
from requests import post
from retriever import context_retriever

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("OLLAMA_BASE_URL")
MODEL = os.getenv("OLLAMA_MODEL")

# Safety check
if not BASE_URL or not MODEL:
    raise ValueError("Missing OLLAMA_BASE_URL or OLLAMA_MODEL in .env")

OLLAMA_URL = BASE_URL.rstrip("/") + "/api/generate"

# Augments prompt and gets the LLM generated reply
def asks_rag(query):
    context = context_retriever(query)

    if not context:
        return "No relevant records were found."

    context_text = "\n".join(context)

    prompt = f"""
You are an assistant that answers questions ONLY using the provided bus attendance records.
Do NOT assume or invent information.

Attendance Records:
{context_text}

Query:
{query}

Instructions:
- Use ONLY the records above.
- Do NOT assume or invent any information.
- Do NOT explain your reasoning process.
- Identify the record that matches the query intent (StudentName, TripType, Action).
- Use Exit records for queries about reaching home or arrival.
- Do NOT reinterpret TripType or Action beyond what matches the query.

Response Style:
- Answer in one natural sentence.
- Mention StudentName, Date and Time.
- Do NOT list multiple records.
- If multiple matches exist, use the latest one.
- If no match exists, say: Insufficient data.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = post(OLLAMA_URL, json=payload, timeout=30)
    except Exception as e:
        return f"Connection Error: {e}"

    if response.status_code != 200:
        return f"LLM Error: {response.text}"

    data = response.json()
    return data.get("response", "No response from model.")

# Run
q1 = input("Enter Query 1: ")
print(asks_rag(q1))