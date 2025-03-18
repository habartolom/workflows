import unittest

from src.modelo.persona import Persona
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.ejercicio import Ejercicio

from src.logica.LogicaMock import LogicaMock

from src.modelo.declarative_base import Session, testDB, Base

class LogicaMockTestCase(unittest.TestCase):

    def crearDB(self):
        #Crea la BD
        Base.metadata.create_all(testDB)

        #Abre la sesion
        session = Session()

        # Crear Personas

        persona1 = Persona(nombre = "Federico", apellido = "Contreras", edad = 15, talla = 1.53, peso = 50, brazo = 15, pecho = 80, cintura = 70, pierna = 35, fecha_retiro = "", razon_retiro = "")
        persona2 = Persona(nombre = "Angelica", apellido = "Mora", edad = 42, talla = 1.90, peso = 75, brazo = 18, pecho = 95, cintura = 76, pierna = 40, fecha_retiro = "2023-03-30", razon_retiro = "Incapacidad")
        persona3 = Persona(nombre = "Julian", apellido = "Salazar", edad = 30, talla = 1.69, peso = 59, brazo = 17, pecho = 69, cintura = 60, pierna = 28, fecha_retiro = "2023-01-18", razon_retiro = "Cambio de instructor")
        persona4 = Persona(nombre = "Bruno", apellido = "Diaz", edad = 26, talla = 1.53, peso = 60, brazo = 16, pecho = 72, cintura = 54, pierna = 20, fecha_retiro = "", razon_retiro = "")

        session.add(persona1)
        session.add(persona2)
        session.add(persona3)
        session.add(persona4)
        session.commit()

        # Crear Ejercicios

        ejercicio1 = Ejercicio(nombre = "Press de pierna", descripcion = "Ejercicio de entrenamiento con pesas en el que el individuo empuja un peso o una resistencia con las piernas.", youtube = "https://www.youtube.com/watch?v=zac9BPZiUTQ", calorias = 120)
        ejercicio2 = Ejercicio(nombre = "Sentadilla", descripcion = "Ejercicio de fuerza en el que se baja la cadera desde una posición de pie y luego vuelve a levantarse.", youtube = "https://www.youtube.com/watch?v=l7aszLSPCVg", calorias = 80)
        ejercicio3 = Ejercicio(nombre = "Abducción de cadera", descripcion = "Mover la pierna derecha hacia la derecha o alejarla del cuerpo y viceversa.", youtube = "https://www.youtube.com/watch?v=dILxTvY88uI", calorias = 90)

        session.add(ejercicio1)
        session.add(ejercicio2)
        session.add(ejercicio3)
        session.commit()

        # Crear Entrenamientos

        entrenamiento1 = Entrenamiento(fecha = "2023-01-18", repeticiones = 15, tiempo = 20)
        entrenamiento2 = Entrenamiento(fecha = "2023-01-18", repeticiones = 12, tiempo = 5)
        entrenamiento3 = Entrenamiento(fecha = "2023-03-11", repeticiones = 15, tiempo = 20)
        entrenamiento4 = Entrenamiento(fecha = "2023-01-18", repeticiones = 15, tiempo = 30)
        entrenamiento5 = Entrenamiento(fecha = "2023-07-02", repeticiones = 10, tiempo = 5)

        session.add(entrenamiento1)
        session.add(entrenamiento2)
        session.add(entrenamiento3)
        session.add(entrenamiento4)
        session.add(entrenamiento5)
        session.commit()

        # Relacionar Personas con Entrenamientos
        persona1.entrenamientos = [entrenamiento1, entrenamiento2, entrenamiento3]
        persona4.entrenamientos = [entrenamiento4, entrenamiento5]


        # Relacionar Ejercicios con los Entrenamientos 
        ejercicio1.entrenamientos = [entrenamiento1, entrenamiento3, entrenamiento4]
        ejercicio2.entrenamientos = [entrenamiento2, entrenamiento5]

        
        session.commit()
        session.close()
        

    def setUp(self):

        self.crearDB()

        self.logica = LogicaMock()
        self.logica.crear_persona( "Sergio", "Barrera", 31, 90, 90, 50, 40, 30, 20)
    
    def tearDown(self):
        self.logica.eliminar_persona(-1)
        self.logica = None
        
    def test_dar_persona(self):

        persona = self.logica.dar_persona(-1)
        self.assertEqual(persona["nombre"], "Sergio")
        self.assertEqual(persona["apellido"], "Barrera")


        persona = self.logica.dar_persona(1)
        self.assertEqual(persona["nombre"], "Angelica")
        self.assertEqual(persona["apellido"], "Mora")

    
