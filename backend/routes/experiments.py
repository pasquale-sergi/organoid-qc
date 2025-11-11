from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from database import get_db

router = APIRouter(prefix="/experiments", tags=["experiments"])

class ExperimentCreate(BaseModel):
    name: str

@router.post("", status_code=status.HTTP_201_CREATED)
def create_experiment(exp: ExperimentCreate, db: Session = Depends(get_db)):
    """Create a new experiment"""
    result = db.execute(
        text("INSERT INTO experiments (name) VALUES (:name) RETURNING id"),
        {"name": exp.name}
    )
    exp_id = result.scalar()
    db.commit()
    return {"id": exp_id, "name": exp.name}

@router.get("")
def list_experiments(db: Session = Depends(get_db)):
    """List all experiments"""
    experiments = db.execute(
        text("SELECT id, name, created_at FROM experiments ORDER BY created_at DESC")
    ).fetchall()
    return [
        {"id": e.id, "name": e.name, "created_at": e.created_at}
        for e in experiments
    ]

@router.delete("/{exp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiment(exp_id: int, db: Session = Depends(get_db)):
    """Delete experiment and associated images"""
    db.execute(text("DELETE FROM images WHERE experiment_id = :id"), {"id": exp_id})
    db.execute(text("DELETE FROM experiments WHERE id = :id"), {"id": exp_id})
    db.commit()