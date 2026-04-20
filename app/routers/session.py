from app.models import pc as pc_model
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import session as session_model
from app.schemas import session as session_schema
from app.auth.security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/sessions", tags=["Usage Sessions"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

@router.post("/", response_model=session_schema.UsageSession, status_code=status.HTTP_201_CREATED)
def create_session(
    session: session_schema.SessionCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_pc = db.query(pc_model.PCStation).filter(pc_model.PCStation.id == session.pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=404, detail="PC Station tidak ditemukan")
        
    db_session = session_model.UsageSession(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/", response_model=List[session_schema.UsageSession])
def read_sessions(db: Session = Depends(get_db)):
    return db.query(session_model.UsageSession).all()

@router.patch("/{session_id}", response_model=session_schema.UsageSession)
def close_session(session_id: int, session_update: session_schema.SessionUpdate, db: Session = Depends(get_db)):
    db_session = db.query(session_model.UsageSession).filter(session_model.UsageSession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    db_session.end_time = session_update.end_time
    db_session.total_price = session_update.total_price
    db.commit()
    db.refresh(db_session)
    return db_session