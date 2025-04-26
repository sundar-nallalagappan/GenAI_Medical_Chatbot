from src.helper import load_pdf_file, text_split, download_hugging_face_embedding_model
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

extracted_data = load_pdf_file(data_dir="data")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embedding_model()

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-chatbot-embeddings"

pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)


#Embed each chunk and upsert each embeddings into index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)
