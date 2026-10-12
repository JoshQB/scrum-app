from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)

    sprints = relationship("Sprint", back_populates="usuario", cascade="all, delete-orphan")
    tareas = relationship("Tarea", back_populates="usuario", cascade="all, delete-orphan")
    horarios = relationship("Horario", back_populates="usuario", cascade="all, delete-orphan")


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    objetivo = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="sprints")
    tareas = relationship("Tarea", back_populates="sprint")


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    estado = Column(String(20), default="por_hacer")  # por_hacer, en_proceso, hecha
    prioridad = Column(String(10), default="media")   # baja, media, alta
    fecha_limite = Column(Date, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="tareas")
    sprint = relationship("Sprint", back_populates="tareas")
    horarios = relationship("Horario", back_populates="tarea")


class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=True)
    titulo = Column(String(200), nullable=False)
    dia_semana = Column(Integer, nullable=False)  # 0 = lunes ... 6 = domingo
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    usuario = relationship("Usuario", back_populates="horarios")
    tarea = relationship("Tarea", back_populates="horarios")