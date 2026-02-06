import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONEDB_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Create Pinecone client using API key
pc = Pinecone(api_key = PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX_NAME)
# Initialize the embedding model that will later convert text into vectors
embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",output_dimensionality=768)

llm = ChatGroq(temperature= 0.3 , model_name ="openai/gpt-oss-20b",api_key=GROQ_API_KEY)
prompt = PromptTemplate.from_template(""""
    
""")
