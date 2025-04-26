from flask import Flask, render_template, jsonify, request
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
from src.helper import download_hugging_face_embedding_model
import os
from langchain_pinecone import PineconeVectorStore

load_dotenv()
app = Flask(__name__)
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

embeddings = download_hugging_face_embedding_model()

index_name = "medical-chatbot-embeddings"
#Load existing index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", sarch_kwargs={'k':3})
#retrieved_docs = retriever.invoke("what is acne?")

llm = OpenAI(temperature=0.4, max_tokens=500)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    render_template("chat.html")
    
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print("user input received", input)
    response = rag_chain.invoke({"input", input})
    print('response is ', response['answer'])
    return str(response["answer"])