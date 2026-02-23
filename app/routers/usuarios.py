# Creación de usuarios
from fastapi import APIRouter, HTTPException
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.db.memory_db import usuarios_db, next_id, find_by_id

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    return usuarios_db

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int):
    usuario = find_by_id(usuarios_db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(data: UsuarioCreate):
    # Verificar si username ya existe
    if any(u.get("username") == data.username for u in usuarios_db):
        raise HTTPException(status_code=400, detail="El username ya está en uso")
    
    nuevo = {
        "id": next_id(usuarios_db),
        **data.model_dump()
    }
    usuarios_db.append(nuevo)
    return nuevo

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate):
    usuario = find_by_id(usuarios_db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar username único si se está actualizando
    if data.username and data.username != usuario.get("username"):
        if any(u.get("username") == data.username for u in usuarios_db):
            raise HTTPException(status_code=400, detail="El username ya está en uso")
    
    # Actualizar solo los campos proporcionados
    cambios = data.model_dump(exclude_unset=True)
    usuario.update(cambios)
    
    return usuario

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    usuario = find_by_id(usuarios_db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # No permitir eliminar el último admin
    if usuario.get("rol") == "admin":
        admins = [u for u in usuarios_db if u.get("rol") == "admin"]
        if len(admins) <= 1:
            raise HTTPException(
                status_code=400, 
                detail="No se puede eliminar el último administrador"
            )
    
    usuarios_db[:] = [u for u in usuarios_db if u.get("id") != usuario_id]
    return {"ok": True, "message": "Usuario eliminado"}

@router.put("/{usuario_id}/activar")
def activar_usuario(usuario_id: int):
    usuario = find_by_id(usuarios_db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario["estado"] = True
    return usuario

@router.put("/{usuario_id}/desactivar")
def desactivar_usuario(usuario_id: int):
    usuario = find_by_id(usuarios_db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario["estado"] = False
    return usuario