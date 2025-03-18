from sqlalchemy import Column, Integer, String, Date , ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.declarative_base import Base


class Entrenamiento(Base):
    # Nombre de la tabla
    __tablename__ = 'entrenamiento'
    # id de busqueda de los Entrenamientos
    id = Column(Integer, primary_key=True)

    fecha = Column(String)
    repeticiones = Column(Integer)
    tiempo = Column(Integer)

    personaid = Column(Integer, ForeignKey('persona.id'))
    ejercicioid = Column(Integer, ForeignKey('ejercicio.id'))

    persona = relationship("Persona", back_populates="entrenamientos")
    ejercicio = relationship("Ejercicio", back_populates="entrenamientos")
