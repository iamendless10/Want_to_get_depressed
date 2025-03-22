import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import ollama
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 🔥 Initialize FastAPI
app = FastAPI()

# 🔥 Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Define upload folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔥 Ollama Model Setup
ollama.pull("nomic-embed-text")
llm = ChatOllama(model="llama3.2")

# 🔥 Define savage roast prompt
template = """
You are a **brutally honest career expert** with **zero patience for mediocrity**. Your job is to **roast** resumes in the most **savage and soul-crushing way possible.** 
Analyze the candidate’s **certifications, skills, achievements, work experience, and projects** and **tear them apart** with maximum sarcasm and use emojis in between like laughing. 
Make them feel like their resume is **an embarrassment to humanity**, but also give them **one last hope** by suggesting what they must **fix immediately.**

🔥 **RULES:**
1. **Be ruthless but real** – don’t sugarcoat.
2. **Make it under 50 words** – quick and **painful**.
3. **Use extreme sarcasm** – destroy their delusions.
4. **Give a constructive tip at the end** – they need some hope.

### Resume Content:
{context}

### 🚨 Roast This Resume:
"""

prompt = ChatPromptTemplate.from_template(template)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 🔥 Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 Load the PDF
        loader = UnstructuredPDFLoader(file_path)
        data = loader.load()

        # 🔥 Split document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
        chunks = text_splitter.split_documents(data)

        # 🔥 Create vector database
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=OllamaEmbeddings(model="nomic-embed-text"),
            collection_name="resume_roast",
        )

        # 🔥 Define retriever
        retriever = vector_db.as_retriever()

        # 🔥 Setup LangChain pipeline
        retrieval_chain = retriever | RunnablePassthrough()
        chain = (
            {"context": retrieval_chain}
            | prompt
            | llm
            | StrOutputParser()
        )

        # 🔥 Generate the roast
        roast = chain.invoke("Roast this resume brutally.")

        return {"roast": roast}

    except Exception as e:
        return {"error": str(e)}

