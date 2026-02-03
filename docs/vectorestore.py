import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone , ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONEDB_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")


os.environ["GOOGLE_API_KEY"]= GOOGLE_API_KEY
#Upload folder setup
upload_directory ="./uploads"
#creating a dirctory if it exists than it will not be created again
## exist_ok=True → prevents error if folder already exists
os.makedirs(upload_directory, exist_ok=True)

# -----------------------------
# Initialize Pinecone Client
# -----------------------------


# Create Pinecone client using API key
pc = Pinecone(api_key = PINECONE_API_KEY)

#Pinecone serverless spec

spec = ServerlessSpec(
    cloud= 'aws',
    region='us-east-1'
)


# -----------------------------
# Check if Index Already Exists
# -----------------------------

# pc.list_indexes() returns a list of dictionaries
# Example: [{"name": "medicalassistant"}, {"name": "jobbot"}]
#Finding for the existing index
existing_index = [i["name"]for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_index:
    pc.create_index(
                    name =PINECONE_INDEX_NAME,
                    dimension=768,
                    metric="dotproduct",
                    specs= spec
              )
              ## Wait until the index is ready
    while  not pc.describe_index(PINECONE_INDEX_NAME).status["READY"]:
        time.sleep(1)

# Get a handle to the Pinecone index so you can insert/search vectors
index = pc.Index(PINECONE_INDEX_NAME)