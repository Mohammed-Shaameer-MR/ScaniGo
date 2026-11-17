#clean console viewing
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  #Hide all except crash and fatals

#hide depreciation warnings
import tensorflow as tf
tf.get_logger().setLevel("ERROR")

#Fix relative path issue
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #Convert file path to abspath
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db") #Build a clear file path

#Code starts here
from sentence_transformers import SentenceTransformer
import chromadb

#load embedding model
model=SentenceTransformer("all-MiniLM-L6-v2")

#Create chroma client
client=chromadb.PersistentClient(path=CHROMA_PATH)

#Create collection (idempotency)
collection=client.get_or_create_collection(
    name="scanigo_data"
)
print(client.list_collections())

#read file "hemak.txt"
with open("data/scanigo_data.txt","r",encoding="utf-8") as f:
    raw_text=f.read()

#Split based on blank lines
lines = [block.strip() for block in raw_text.split("\n\n") if block.strip()]

print("Number of events:", len(lines))
for i, event in enumerate(lines, 1):
    print(f"\n--- Event {i} ---\n{event}")

#create embeddings
embeddings=model.encode(lines).tolist()
print("\nNo of chunks [data]: ",len(embeddings))
print("\nDimension : ",len(embeddings[0]))

#Create ids for accessing
ids=[f"data_{i}" for i in range(len(lines))]

#Add all to chroma collection  (upsert: insert if missing, update if exists)
collection.upsert(
    documents=lines,
    embeddings=embeddings,
    ids=ids
)

print("ScaniGo Data was indexed successfully")