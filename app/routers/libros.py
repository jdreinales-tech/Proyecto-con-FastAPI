from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import models, schemas
from app.database import get_db
from app.dependencies import obtener_usuario_actual  # Dependencia JWT actualizada

router = APIRouter(
    prefix="/libros",
    tags=["Libros"]
)

# 1. GET /libros - PÚBLICO
@router.get("/", response_model=List[schemas.Libro])
def obtener_libros(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    prestado: Optional[bool] = Query(None),
    buscar: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.LibroDB)
    if prestado is not None:
        query = query.filter(models.LibroDB.prestado == prestado)
    if buscar:
        termino = f"%{buscar}%"
        query = query.filter(
            or_(
                models.LibroDB.titulo.ilike(termino),
                models.LibroDB.autor.ilike(termino)
            )
        )
    return query.offset(skip).limit(limit).all()


# 2. POST /libros - PROTEGIDO CON JWT
@router.post("/", response_model=schemas.Libro, status_code=status.HTTP_201_CREATED)
def crear_libro(
    libro: schemas.LibroCrear, 
    db: Session = Depends(get_db),
    usuario_actual: models.UsuarioDB = Depends(obtener_usuario_actual) # Pide Bearer Token
):
    nuevo_libro = models.LibroDB(**libro.model_dump(), usuario_id=usuario_actual.id)
    
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro


# 3. DELETE /libros/{libro_id} - PROTEGIDO CON JWT
@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(
    libro_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: models.UsuarioDB = Depends(obtener_usuario_actual)
):
    libro_db = db.query(models.LibroDB).filter(models.LibroDB.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="El libro especificado no existe")
    
    db.delete(libro_db)
    db.commit()
    return None