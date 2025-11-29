from .store import VectorStore
import uuid

def ingest_text(text: str, filename: str):
    store = VectorStore()
    doc_id = str(uuid.uuid4())
    
    # Simple chunking for now
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk": i} for i in range(len(chunks))]
    
    store.add_documents(documents=chunks, metadatas=metadatas, ids=ids)
    return len(chunks)
