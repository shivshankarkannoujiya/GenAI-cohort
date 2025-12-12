from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage 


pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)

# Returns => Pages [] <docs>
docs = loader.load()

"""
NOTE: 
    - Ingesting a whole page is very bad
    - Text available in Pages me cause `OUT OF CONTEXT ERROR`
    - SO, split according to text
    Eg: 1000 paragarphs ke chunks bana do 
    Use: 
        - text splitter
        - Overlap <Otherwise context loose ho jayegs>
"""

# Initialize splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split documnets
split_docs = text_splitter.split_documents(documents=docs)


# Embedding
embedder = OpenAIEmbeddings(model="text-embedding-3-large", api_key="api_key")

# Embedding the Split_docs and store the embeddings into `vector-database`
# USE: Qdrant db: open source

# initialize vector_store
vector_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder,
)

# store: Embeddings with pages content as well as some meta data
vector_store.add_documents(documents=split_docs)
print("INJECTION DONE...")


# RETRIVE FROM THE SAME DB COLLECTION
retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder,
)

# USER ASKED QUESTIONS: SERACH IN DB AND RETURN THE RESULT <Relevant Chunks>
user_query = "What is FS Module ?"
relevant_chunks = retriver.similarity_search(
    query=user_query
)

context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])

print("Relevant Chunks: ", relevant_chunks)
print("Context Text: ", context_text)


# BASED ON RELEVANT CHUNKS CHAT WITH LARGE LANGUAGE MODEL <LLM>
SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who responds based on the available context.
If the answer is not in the context, say you don't know.

Context:
{context_text}
"""


# Initialize the LLM
AI = ChatOpenAI(
    model="gpt-4o",
      api_key="api_key"
)

# Create the messages
messages = [
   SystemMessage(content=SYSTEM_PROMPT),
   HumanMessage(content=user_query)
]

# Generate the response
response = AI.invoke(messages)

print("----- AI Response -----")
print(response)



"""
NOTE:
    - Creating 1000 wrods chunks also can cause: CONTEXT BREAK
    - Overlap hokar next chunk me chala jayega 
    - Chunking is an ART in iteself
    - Large Chunks cause: HALLUCINATION
    - Smaller Chunk cause: LOOSING DATA
    - It's a HIT & TRIAL

    ---- DEPENDS ON THE APPLICATION ----
    - Chunking process depends on the `Application`
    - SO,
        - THERE IS DIFFERENT - DIFFERENT RAG Approaches

"""