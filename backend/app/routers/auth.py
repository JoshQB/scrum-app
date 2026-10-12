import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_usuario_actual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    error = HTTPException(
        status_code=401,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        usuario_id = int(payload.get("sub"))
    except (jwt.PyJWTError, TypeError, ValueError):
        raise error

    usuario = db.get(models.Usuario, usuario_id)
    if usuario is None:
        raise error
    return usuario


@router.post("/registro", response_model=schemas.UsuarioSalida, status_code=201)
def registro(datos: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    email = datos.email.lower()
    existe = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")

    usuario = models.Usuario(
        nombre=datos.nombre,
        email=email,
        password_hash=security.hashear_password(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.email == form.username.lower())
        .first()
    )
    if not usuario or not security.verificar_password(form.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    return {"access_token": security.crear_token(usuario.id), "token_type": "bearer"}


@router.get("/yo", response_model=schemas.UsuarioSalida)
def yo(usuario: models.Usuario = Depends(get_usuario_actual)):
    return usuario