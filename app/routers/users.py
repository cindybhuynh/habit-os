from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return {"ok": True}
