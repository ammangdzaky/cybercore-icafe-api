from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import pc as pc_model
from app.schemas import pc as pc_schema

router = APIRouter(prefix="/pcs", tags=["PC Stations"])

@router.post("/", response_model=pc_schema.PC, status_code=status.HTTP_201_CREATED)
def create_pc(pc: pc_schema.PCCreate, db: Session = Depends(get_db)):
    existing_pc = db.query(pc_model.PCStation).filter(pc_model.PCStation.pc_number == pc.pc_number).first()
    if existing_pc:
        raise HTTPException(status_code=400, detail="Nomor PC sudah terdaftar")
        
    db_pc = pc_model.PCStation(**pc.dict())
    db.add(db_pc)
    db.commit()
    db.refresh(db_pc)
    return db_pc

@router.get("/", response_model=List[pc_schema.PC])
def read_pcs(db: Session = Depends(get_db)):
    return db.query(pc_model.PCStation).all()

@router.get("/{pc_id}", response_model=pc_schema.PC)
def read_pc(pc_id: int, db: Session = Depends(get_db)):
    db_pc = db.query(pc_model.PCStation).filter(pc_model.PCStation.id == pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=404, detail="PC not found")
    return db_pc

@router.put("/{pc_id}", response_model=pc_schema.PC)
def update_pc(pc_id: int, pc_update: pc_schema.PCCreate, db: Session = Depends(get_db)):
    db_pc = db.query(pc_model.PCStation).filter(pc_model.PCStation.id == pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=404, detail="PC not found")
    for key, value in pc_update.dict().items():
        setattr(db_pc, key, value)
    db.commit()
    db.refresh(db_pc)
    return db_pc

@router.delete("/{pc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pc(pc_id: int, db: Session = Depends(get_db)):
    db_pc = db.query(pc_model.PCStation).filter(pc_model.PCStation.id == pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=404, detail="PC not found")
    db.delete(db_pc)
    db.commit()
    return None