from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.declarative_base import Base


class Ejercicio(Base):
    # Nombre de la tabla
    __tablename__ = 'ejercicio'
    # id de busqueda del Ejercicio
    id = Column(Integer, primary_key=True)

    nombre          = Column(String, nullable=False)
    descripcion     = Column(String, nullable=False)
    youtube         = Column(String, nullable=False)
    calorias        = Column(Integer, nullable=False) 

    entrenamientos = relationship("Entrenamiento")

    def __init__(self, nombre, descripcion, youtube, calorias):
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del ejercicio no puede estar vacío")
            
        if not descripcion or descripcion.strip() == "":
            raise ValueError("La descripción del ejercicio no puede estar vacía")
            
        if not youtube or youtube.strip() == "":
            raise ValueError("El enlace de YouTube no puede estar vacío")
            
        if not isinstance(calorias, (int, float)) or calorias <= 0:
            raise ValueError("Las calorías deben ser un número positivo")

        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.youtube = youtube.strip()
        self.calorias = calorias