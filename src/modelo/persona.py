from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.declarative_base import Base


class Persona(Base):
    # Nombre de la tabla
    __tablename__ = 'persona'
    # id de busqueda de la persona
    id = Column(Integer, primary_key=True)

    nombre      = Column(String)
    apellido    = Column (String)
    edad        = Column (Integer)
    talla       = Column (Float)
    peso        = Column (Integer)
    brazo       = Column (Integer)
    pecho       = Column (Integer)
    cintura     = Column (Integer)
    pierna      = Column (Integer)

    fecha_retiro = Column (String)
    razon_retiro = Column (String)

    entrenamientos = relationship("Entrenamiento")