#Clean console viewing
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  #Hide all except crash and fatals

#Hide depreciation warnings
import tensorflow as tf
tf.get_logger().setLevel("ERROR")

#Fix relatve path issue
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

#Code starts here
from sentence_transformers import SentenceTransformer
import chromadb
from query_optimiser import query_fixer

#Load Embedding model
model=SentenceTransformer("all-MiniLM-L6-v2")

#Create client
client=chromadb.PersistentClient(path=CHROMA_PATH)

#Load existing collection
collection=client.get_or_create_collection("scanigo_data")

#Query-> Embedding-> Search -> Top-k similar results ->Return chunks
def context_retriever(query,k=2):

    #Make query into embedded query
    optimised_query=query_fixer(query)
    print(optimised_query)
    print()
    embedded_query=model.encode([optimised_query]).tolist()

    #Search and get chunks
    results=collection.query(
        query_embeddings=embedded_query,
        n_results=k,
        include=["documents"]
    )

    #Give answer  [innermost top-k] [[-90.1,-90.23]]
    return results["documents"][0]

#print(context_retriever("WHat time does Karthick reach home?"))