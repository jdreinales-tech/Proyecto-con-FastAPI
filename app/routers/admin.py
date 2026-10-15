from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UsuarioDB
from app.dependencies import exigir_rol_admin  # O desde donde hayas importado la función anterior

router = APIRouter(prefix="/admin", tags=["Administración"])

@router.get("/usuarios")
def listar_todos_los_usuarios(
    db: Session = Depends(get_db),
    admin_user: UsuarioDB = Depends(exigir_rol_admin)
):
    # Como esta ruta usa 'exigir_rol_admin', un usuario normal recibirá un error 403 automáticamente
    usuarios = db.query(UsuarioDB).all()
    return [
        {"id": u.id, "email": u.email, "role": getattr(u, "role", "user")} 
        for u in usuarios
    ]