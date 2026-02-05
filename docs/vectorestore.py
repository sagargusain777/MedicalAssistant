import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone , ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import asyncio

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
                    name = PINECONE_INDEX_NAME,
                    dimension=768,
                    metric="dotproduct",
                    spec= spec
              )
              ## Wait until the index is ready
    while  not pc.describe_index(PINECONE_INDEX_NAME).status.state["READY"]:
        time.sleep(1)

# Get a handle to the Pinecone index so you can insert/search vectors
index = pc.Index(PINECONE_INDEX_NAME)



async def load_vectorstore(uploaded_files,role:str,doc_id:str):
     # Initialize the embedding model that will later convert text into vectors
    embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
     # Loop through every file uploaded from the frontend
    for file in uploaded_files:
        # Create the full path on the server where this file will be saved
        # Example: ./uploads/report.pdf
        save_path = Path(upload_directory)/file.filename
        # Open a new file on disk in write-binary mode ("wb")
        # This creates the file if it doesn't exist and overwrites it if it does
        with open(save_path,"wb") as f:
             # Read all bytes from the uploaded file (temporary storage)
            # and write them permanently to the server's filesystem
            f.write(file.file.read())

            loader = PyPDFLoader(str(save_path))
            document = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500 , chunk_overlap = 200)
            # Split the loaded document into multiple smaller chunked documents
            chunked_documents = text_splitter.split_documents(document)
           
            texts = [chunk.page_content for chunk in chunked_documents]
            #Generate unique IDs for every chunk
            # Example: doc123-0, doc123-1, ...
            ids = [f"{doc_id}-{i}" for i in range(len(chunked_documents))]
            # Build metadata for each chunk
            # Stored alongside vectors in Pinecone
            metadata = [
                {
                    "source": file.filename,
                    "doc_id": doc_id,
                    "role": role,
                    "page":chunk.metadata.get("page",0)
                }
                for i ,chunk in enumerate(chunked_documents)
            ]
            print(f"Embedding {len(texts)} chunks...")
            embeddings = await asyncio.to_thread(embed_model.embed_documents,texts)

            print(f"Uploading to Pinecone Database")
            with tqdm(total=len(embeddings),desc="Upseting to Pinecone") as progress:
                index.upsert(vectors=zip(ids,embeddings,metadata))
                progress.update(len(embeddings))

            print(f"Upload complete for {file.filename}")



