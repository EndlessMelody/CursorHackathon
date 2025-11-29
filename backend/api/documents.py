from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from database.models import Document, Project
from rag.ingest import ingest_text

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    project_id: int = 1, # Default project for now
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode("utf-8") # Assuming text
    
    # Save to DB
    db_doc = Document(filename=file.filename, content=text, project_id=project_id)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    
    # Ingest to Vector DB
    chunks = ingest_text(text, file.filename)
    
    return {"id": db_doc.id, "filename": db_doc.filename, "chunks": chunks}

@router.get("/")
def list_documents(project_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.project_id == project_id).all()
