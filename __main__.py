import sys
from src.vista.InterfazEnForma import App_EnForma
from src.logica.FachadaEnForma import FachadaEnForma

from src.modelo.declarative_base import Session, produccionDB, Base

if __name__ == '__main__':
    # Punto inicial de la aplicación

    # Base de Datos
    #Crea la BD
    Base.metadata.create_all(produccionDB)
    
    #Abre la sesion
    session = Session()

    # Logica Aplicación Nueva
    logica = FachadaEnForma()

    # Interfaz Aplicación
    app = App_EnForma(sys.argv, logica)
    sys.exit(app.exec_())