import unittest

from src.modelo.persona import Persona
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.ejercicio import Ejercicio
from src.logica.FachadaEnForma import FachadaEnForma

from src.modelo.declarative_base import Session, testDB, Base

from faker import Faker

class LogicaFachadaTestCase(unittest.TestCase):

    def setUp(self):

        self.logica = FachadaEnForma()
        self.faker = Faker()
    
    def tearDown(self):
        self.logica = None
        

    # Pruebas unitarias HU002 - Listar personas

    def test_listar_personas(self):

        personas = self.logica.dar_personas()
        self.assertIsNotNone(personas)
        self.assertIsInstance(personas, list)

    def test_personas_diccionario(self):

        personas = self.logica.dar_personas()
        for persona in personas:
            self.assertIsNotNone(persona)

    def test_personas_campos_no_vacios(self):

        personas = self.logica.dar_personas()
        for persona in personas:
            self.assertIsNotNone(persona)
            self.assertNotEqual(persona['nombre'], "")
            self.assertNotEqual(persona['apellido'], "")


    # Pruebas unitarias HU010 - Listar entrenamientos de persona
    
    def test_listar_entrenamientos_persona(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        entrenamientos = self.logica.dar_entrenamientos(id_primera_persona)

        self.assertIsNotNone(entrenamientos)
        self.assertIsInstance(entrenamientos, list)

    def test_tipo_entrenamientos(self):

        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        entrenamientos = self.logica.dar_entrenamientos(id_primera_persona)
        for entrenamiento in entrenamientos:
            self.assertIsNotNone(entrenamiento)

    def test_entrenamientos_campos_no_vacios(self):

        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        entrenamientos = self.logica.dar_entrenamientos(id_primera_persona)
        for entrenamiento in entrenamientos:
            self.assertIsNotNone(entrenamiento)

            self.assertIsInstance(entrenamiento['ejercicio'], str)
            self.assertNotEqual(entrenamiento['ejercicio'].strip(), "")

            self.assertIsInstance(entrenamiento['fecha'], str)
            self.assertNotEqual(entrenamiento['fecha'].strip(), "")

            self.assertIsInstance(entrenamiento['repeticiones'], int)
            self.assertGreater(entrenamiento['repeticiones'], 0)

            self.assertIsInstance(entrenamiento['tiempo'], int)
            self.assertGreater(entrenamiento['tiempo'], 0)


    # Pruebas unitarias HU011 - Crear entrenamiento personal

    def test_crear_entrenamiento_persona(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        # Persona a la que se le agregara el ejercicio
        persona = self.logica.dar_persona(id_primera_persona)
        ejercicios = self.logica.dar_ejercicios()
        ejercicio = ejercicios[0]["nombre"] if ejercicios else "Sentadilla"
        fecha_futura = self.faker.date_between(start_date='today', end_date='+2y')
        repeticiones = self.faker.random_int(min=5, max=30)
        tiempo = self.faker.random_int(min=10, max=60)

        self.logica.crear_entrenamiento(persona, ejercicio, fecha_futura.strftime("%Y-%m-%d"), repeticiones, tiempo)

        # Valido los entrenamiento
        entrenamientos = self.logica.dar_entrenamientos(id_primera_persona)
        for entrenamiento in entrenamientos:
            self.assertIsNotNone(entrenamiento)

    def test_validar_datos_entrenamiento_persona(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        # Persona a la que se le agregara el ejercicio
        persona = self.logica.dar_persona(id_primera_persona)
        ejercicios = self.logica.dar_ejercicios()
        ejercicio = ejercicios[0]["nombre"] if ejercicios else "Sentadilla"
        fecha_futura = self.faker.date_between(start_date='today', end_date='+2y')
        repeticiones = self.faker.random_int(min=5, max=30)
        tiempo = self.faker.random_int(min=10, max=60)
        fecha_str = fecha_futura.strftime("%Y-%m-%d")

        self.logica.crear_entrenamiento(persona, ejercicio, fecha_str, repeticiones, tiempo)

        # Valido los entrenamiento
        entrenamientonuevo = self.logica.dar_entrenamientos(id_primera_persona)[-1]
        
        self.assertEqual(entrenamientonuevo['fecha'], fecha_str)
        self.assertEqual(entrenamientonuevo['repeticiones'], repeticiones)
        self.assertEqual(entrenamientonuevo['tiempo'], tiempo)

    def test_validar_campos_entrenamiento_no_vacios(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        # Persona a la que se le agregara el ejercicio
        persona = self.logica.dar_persona(id_primera_persona)
        ejercicios = self.logica.dar_ejercicios()
        ejercicio = ejercicios[0]["nombre"] if ejercicios else "Sentadilla"
        fecha_futura = self.faker.date_between(start_date='today', end_date='+2y')
        repeticiones = self.faker.random_int(min=5, max=30)
        tiempo = self.faker.random_int(min=10, max=60)

        self.logica.crear_entrenamiento(persona, ejercicio, fecha_futura.strftime("%Y-%m-%d"), repeticiones, tiempo)

        # Valido el entrenamiento creado a la persona
        entrenamientonuevo = self.logica.dar_entrenamientos(id_primera_persona)[-1]
        
        self.assertIsNotNone(entrenamientonuevo['fecha'])
        self.assertIsNot(entrenamientonuevo['fecha'], "")
        
        self.assertIsNotNone(entrenamientonuevo['repeticiones'])
        self.assertGreater(entrenamientonuevo['repeticiones'], 0)

        self.assertIsNotNone(entrenamientonuevo['tiempo'])
        self.assertGreater(entrenamientonuevo['tiempo'], 0)

    # Pruebas unitarias HU014 - Generar reporte persona

    def test_obtener_reporte_persona(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        reporte = self.logica.dar_reporte(id_primera_persona)
        self.assertIsNotNone(reporte)
        self.assertIsInstance(reporte, dict)

    def test_estructura_reporte_persona(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        reporte = self.logica.dar_reporte(id_primera_persona)
        
        claves_esperadas = [
            'persona', 
            'estadisticas'
        ]

        for clave in claves_esperadas:
            self.assertIn(clave, reporte)

    def test_calculo_imc_reporte(self):

        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]


        reporte = self.logica.dar_reporte(id_primera_persona)
        
        persona = self.logica.dar_persona(id_primera_persona)

        imc_esperado = persona['peso'] / (persona['talla'] ** 2)
        
        self.assertEqual(reporte['estadisticas']['imc'], imc_esperado)

    def test_clasificacion_imc_reporte(self):

        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        reporte = self.logica.dar_reporte(id_primera_persona)
        imc = reporte['estadisticas']['imc']
        clasificacion = reporte['estadisticas']['clasificacion']

        if imc < 18.5:
            self.assertEqual(clasificacion, "Bajo peso")
        elif imc < 25:
            self.assertEqual(clasificacion, "Peso saludable")
        elif imc < 30:
            self.assertEqual(clasificacion, "Sobrepeso")
        else:
            self.assertEqual(clasificacion, "Obesidad")

    def test_calculo_totales_reporte(self):
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        reporte = self.logica.dar_reporte(id_primera_persona)
        
        total_repeticiones_esperado = 0
        total_calorias_esperado = 0

        entrenamientos = self.logica.dar_entrenamientos(id_primera_persona)
        ejercicios = self.logica.dar_ejercicios()

        for entrenamiento in entrenamientos:
            total_repeticiones_esperado += entrenamiento['repeticiones']
            ejercicio = next((p for p in ejercicios if p["nombre"] == entrenamiento['ejercicio']), None)
            total_calorias_esperado += entrenamiento['repeticiones'] * ejercicio['calorias']
        
        self.assertEqual(reporte['estadisticas']['total_repeticiones'], total_repeticiones_esperado)
        self.assertEqual(reporte['estadisticas']['total_calorias'], total_calorias_esperado)
        
    # Pruebas unitarias HU006 - Listar ejercicios disponibles

    def test_lista_ejercicios_no_vacios(self):  
        ejercicios = self.logica.dar_ejercicios()
        self.assertIsNotNone(ejercicios)
        self.assertIsInstance(ejercicios, list)

    def test_lista_ejercicios(self):  
        ejercicios = self.logica.dar_ejercicios()
        for ejercicio in ejercicios:
            self.assertIsNotNone(ejercicio)

    def test_ejercicios_campos_no_vacios(self):
        ejercicios = self.logica.dar_ejercicios()
        for ejercicio in ejercicios:
            self.assertIsNotNone(ejercicio)
            self.assertNotEqual(ejercicio['nombre'], "")
            self.assertNotEqual(ejercicio['descripcion'], "")
            self.assertNotEqual(ejercicio['youtube'], "")
            self.assertNotEqual(ejercicio['calorias'], 0)
            
    # Pruebas unitarias HU007 - Crear nuevo ejercicio

    def test_crear_ejercicio(self):
        ejercicios_inicial = len(self.logica.dar_ejercicios())
        
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        youtube = "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????")
        calorias = self.faker.random_int(min=5, max=500)
        
        self.logica.crear_ejercicio(
            nombre,
            descripcion,
            youtube,
            calorias
        )
        
        ejercicios_final = len(self.logica.dar_ejercicios())
        self.assertEqual(ejercicios_final, ejercicios_inicial + 1)

    def test_crear_ejercicio_verificar_datos(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        youtube = "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????")
        calorias = self.faker.random_int(min=5, max=500)

        self.logica.crear_ejercicio(nombre, descripcion, youtube, calorias)
        
        ejercicios = self.logica.dar_ejercicios()
        ejercicio_nuevo = next((e for e in ejercicios if e['nombre'] == nombre), None)
        
        self.assertIsNotNone(ejercicio_nuevo)
        self.assertEqual(ejercicio_nuevo['nombre'], nombre)
        self.assertEqual(ejercicio_nuevo['descripcion'], descripcion)
        self.assertEqual(ejercicio_nuevo['youtube'], youtube)
        self.assertEqual(ejercicio_nuevo['calorias'], calorias)

    def test_crear_ejercicio_tipos_datos(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        youtube = "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????")
        calorias = self.faker.random_int(min=5, max=500)

        self.logica.crear_ejercicio(nombre, descripcion, youtube, calorias)
        
        ejercicios = self.logica.dar_ejercicios()
        ejercicio_nuevo = next((e for e in ejercicios if e['nombre'] == nombre), None)
        
        self.assertIsInstance(ejercicio_nuevo['nombre'], str)
        self.assertIsInstance(ejercicio_nuevo['descripcion'], str)
        self.assertIsInstance(ejercicio_nuevo['youtube'], str)
        self.assertIsInstance(ejercicio_nuevo['calorias'], int)

    def test_crear_ejercicio_campos_no_vacios(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        youtube = "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????")
        calorias = self.faker.random_int(min=5, max=500)

        self.logica.crear_ejercicio(nombre, descripcion, youtube, calorias)
        
        ejercicios = self.logica.dar_ejercicios()
        ejercicio_nuevo = next((e for e in ejercicios if e['nombre'] == nombre), None)
        
        self.assertIsNotNone(ejercicio_nuevo)
        self.assertNotEqual(ejercicio_nuevo['nombre'].strip(), "")
        self.assertNotEqual(ejercicio_nuevo['descripcion'].strip(), "")
        self.assertNotEqual(ejercicio_nuevo['youtube'].strip(), "")
        self.assertGreater(ejercicio_nuevo['calorias'], 0)

    def test_crear_ejercicio_url_youtube_valida(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        youtube = "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????")
        calorias = self.faker.random_int(min=5, max=500)

        self.logica.crear_ejercicio(nombre, descripcion, youtube, calorias)
        
        ejercicios = self.logica.dar_ejercicios()
        ejercicio_nuevo = next((e for e in ejercicios if e['nombre'] == nombre), None)
        
        self.assertTrue(ejercicio_nuevo['youtube'].startswith("https://www.youtube.com/watch?v="))
        self.assertGreater(len(ejercicio_nuevo['youtube']), len("https://www.youtube.com/watch?v="))

    def test_crear_ejercicio_campos_solo_espacios(self):
        with self.assertRaises(ValueError):
            self.logica.crear_ejercicio(
                "   ",
                "     ",
                "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????"),
                str(self.faker.random_int(min=5, max=500))
            )

    def test_crear_ejercicio_url_invalida(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        calorias = str(self.faker.random_int(min=5, max=500))
        urls_invalidas = [
            "",
            "http://" + self.faker.domain_name(),
            "https://www.youtube.com/",
            "https://www.youtube.com/watch",
        ]
        
        for url in urls_invalidas:
            with self.assertRaises(ValueError):
                self.logica.crear_ejercicio(
                    nombre,
                    descripcion,
                    url,
                    calorias
                )

    # Pruebas unitarias HU008 - Crear nuevo persona

    def test_validacion_exitosa(self):
        resultado = self.logica.validar_crear_editar_persona(
            id_persona=1,
            nombre=self.faker.first_name(),
            apellido=self.faker.last_name(),
            edad="30",
            talla="1.75",
            peso="70",
            brazo="30",
            pecho="90",
            cintura="80",
            pierna="50"
        )
        self.assertEqual(resultado, "")  # No debe haber errores ya que la creo bien

    def test_nombre_apellido_vacios(self):
        """Debe fallar si nombre o apellido están vacíos."""
        resultado = self.logica.validar_crear_editar_persona(
            id_persona=1,
            nombre="",
            apellido="",
            edad="30",
            talla="1.75",
            peso="70",
            brazo="30",
            pecho="90",
            cintura="80",
            pierna="50"
        )
        self.assertIn("El nombre es obligatorio", resultado)
        self.assertIn("El apellido es obligatorio", resultado)

    def test_edad_invalida(self):
        """Debe fallar si la edad no es un número válido o es negativa."""
        resultado = self.logica.validar_crear_editar_persona(
            id_persona=1,
            nombre=self.faker.first_name(),
            apellido=self.faker.last_name(),
            edad="-5",
            talla="1.75",
            peso="70",
            brazo="30",
            pecho="90",
            cintura="80",
            pierna="50"
        )
        self.assertIn("La edad debe ser un número positivo mayor a 0.", resultado)

    def test_talla_peso_medidas_invalidas(self):
        """Debe fallar si talla, peso o medidas son inválidas."""
        resultado = self.logica.validar_crear_editar_persona(
            id_persona=1,
            nombre=self.faker.first_name(),
            apellido=self.faker.last_name(),
            edad="25",
            talla="cero",  # Inválido
            peso="-10",  # Inválido
            brazo="abc",  # Inválido
            pecho="0",  # Inválido
            cintura="-1",  # Inválido
            pierna="5.5"  # No es entero
        )
        self.assertIn("La talla debe ser un número decimal válido.", resultado)
        self.assertIn("El peso debe ser un número positivo mayor a 0.", resultado)
        self.assertIn("La medida de brazo debe ser un número entero válido.", resultado)
        self.assertIn("La medida de pecho debe ser un número positivo mayor a 0.", resultado)
        self.assertIn("La medida de cintura debe ser un número positivo mayor a 0.", resultado)
        self.assertIn("La medida de pierna debe ser un número entero válido.", resultado)


    def test_crear_persona_y_validar(self):
        """Debe crear una persona y luego encontrarla en la lista de personas."""
        datos_persona = {
            "nombre": self.faker.first_name(),
            "apellido": self.faker.last_name(),
            "edad": "25",
            "talla": "1.75",
            "peso": "70",
            "brazo": "30",
            "pecho": "90",
            "cintura": "80",
            "pierna": "50"
        }

        # Crear persona
        self.logica.crear_persona(**datos_persona)

        # Validar que la persona creada está en la base de datos
        personas = self.logica.dar_personas()
        persona_creada = next((p for p in personas if (p["nombre"] == datos_persona["nombre"] and p["apellido"] == datos_persona["apellido"]) ), None)

        self.assertIsNotNone(persona_creada)
        self.assertEqual(persona_creada["nombre"], datos_persona["nombre"])
        self.assertEqual(persona_creada["apellido"], datos_persona["apellido"])
        self.assertEqual(persona_creada["edad"], int(datos_persona["edad"]))
        self.assertEqual(persona_creada["talla"], float(datos_persona["talla"]))

    # Pruebas unitarias HU003 - Editar  persona
    def test_editar_persona_no_existe(self):
        """Debe intentar editar una persona inexistente sin generar error."""
        try:
            self.logica.editar_persona(9999, "Test", "Apellido", "30", "1.75", "70", "30", "90", "80", "50")
        except Exception as e:
            self.fail(f"Editar persona inexistente lanzó una excepción: {e}")

    def test_editar_persona (self):
        """Test de edición de personas"""
        personas = self.logica.dar_personas()
        if personas:
            id_primera_persona = personas[0]["id"]

        persona_antes = self.logica.dar_persona(id_primera_persona)

        if not persona_antes:
            self.fail("No existe una persona con id=1 para editar.")

        # Generar nuevos datos con Faker
        nuevos_datos = {
            "nombre": self.faker.first_name(),
            "apellido": self.faker.last_name(),
            "edad": self.faker.random_int(min=18, max=80),
            "talla": round(self.faker.random_number(digits=2) / 100 + 1.5, 2),
            "peso": self.faker.random_int(min=50, max=100),
            "brazo": self.faker.random_int(min=20, max=40),
            "pecho": self.faker.random_int(min=80, max=120),
            "cintura": self.faker.random_int(min=60, max=100),
            "pierna": self.faker.random_int(min=30, max=60),
        }

        # Editar la persona con id=1
        self.logica.editar_persona(
            id_primera_persona, nuevos_datos["nombre"], nuevos_datos["apellido"], nuevos_datos["edad"],
            nuevos_datos["talla"], nuevos_datos["peso"], nuevos_datos["brazo"],
            nuevos_datos["pecho"], nuevos_datos["cintura"], nuevos_datos["pierna"]
        )

        # Volver a obtener la persona con dar_persona(1) (después de editar)
        persona_despues = self.logica.dar_persona(id_primera_persona)

        # Comparar y validar que los datos cambiaron
        self.assertIsNotNone(persona_despues, "No se encontró la persona editada en `dar_persona(1)`.")
        self.assertNotEqual(persona_despues, persona_antes, "Los datos no fueron actualizados.")

        self.assertEqual(persona_despues["nombre"], nuevos_datos["nombre"])
        self.assertEqual(persona_despues["apellido"], nuevos_datos["apellido"])
        self.assertEqual(persona_despues["edad"], nuevos_datos["edad"])
        self.assertEqual(persona_despues["talla"], nuevos_datos["talla"])
        self.assertEqual(persona_despues["peso"], nuevos_datos["peso"])
        self.assertEqual(persona_despues["brazo"], nuevos_datos["brazo"])
        self.assertEqual(persona_despues["pecho"], nuevos_datos["pecho"])
        self.assertEqual(persona_despues["cintura"], nuevos_datos["cintura"])
        self.assertEqual(persona_despues["pierna"], nuevos_datos["pierna"])

    # Pruebas unitarias HU005 - Eliminar persona
    def test_eliminar_persona(self):
        """Test eliminar persona y verifica que fue eliminada correctamente."""
        # Valido Personas en la Base de Datos
        personas_antes = self.logica.dar_personas()
        if personas_antes:
            id_primera_persona = personas_antes[0]["id"]
        else:
            id_primera_persona = None  # Si no hay personas, no hay nada que eliminar

        if id_primera_persona:
            self.logica.eliminar_persona(id_primera_persona)
            personas_despues = self.logica.dar_personas()
            self.assertEqual(len(personas_despues), len(personas_antes) - 1, "No se eliminó correctamente la persona")

    # Pruebas unitarias HU009 - Eliminar Ejercicio - validar_crear_editar_ejercicio

    def test_validacion_exitosa_ejercicio(self):
        nombre = self.faker.word()
        descripcion = self.faker.sentence()
        enlace = "https://www.youtube.com/watch?v=" + self.faker.lexify(text="???????")
        calorias = str(self.faker.random_int(min=1, max=500))

        resultado = self.logica.validar_crear_editar_ejercicio(nombre, descripcion, enlace, calorias)
        self.assertEqual(resultado, "")

    def test_ejercicio_itens_no_vacio(self):
        nombre_valido = self.faker.word().capitalize()
        descripcion_valida = self.faker.paragraph()
        youtube_valido = "https://youtu.be/" + self.faker.lexify(text="????????")
        calorias_validas = str(self.faker.random_int(min=5, max=500))

        #Nombre
        resultado = self.logica.validar_crear_editar_ejercicio("", descripcion_valida, youtube_valido, calorias_validas)
        self.assertIn("El nombre del ejercicio no puede estar vacío.", resultado)
        #Descripcion
        resultado = self.logica.validar_crear_editar_ejercicio(nombre_valido, "", youtube_valido, calorias_validas)
        self.assertIn("La descripción del ejercicio no puede estar vacía.", resultado)
        #Enlace YT
        resultado = self.logica.validar_crear_editar_ejercicio(nombre_valido, descripcion_valida, "https://google.com/video", calorias_validas)
        self.assertIn("El enlace debe ser un video válido de YouTube.", resultado)
        #Calorias
        resultado = self.logica.validar_crear_editar_ejercicio(nombre_valido, descripcion_valida, youtube_valido, "abc")
        self.assertIn("Las calorías deben ser un número entero.", resultado)

    def test_calorias_negativas(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        youtube = "https://youtu.be/" + self.faker.lexify(text="????????")
        calorias_negativas = str(-self.faker.random_int(min=1, max=500))

        resultado = self.logica.validar_crear_editar_ejercicio(nombre, descripcion, youtube, calorias_negativas)
        self.assertIn("Las calorías deben ser un número positivo.", resultado)

    def test_crear_ejercicio_campos_vacios(self):
        with self.assertRaises(ValueError):
            self.logica.crear_ejercicio(
                "",
                "",
                "",
                0
            )

    def test_crear_ejercicio_campos_solo_espacios(self):
        with self.assertRaises(ValueError):
            self.logica.crear_ejercicio(
                "   ",
                "     ",
                "https://www.youtube.com/watch?v=" + self.faker.lexify(text="????????"),
                str(self.faker.random_int(min=5, max=500))
            )

    def test_crear_ejercicio_url_invalida(self):
        nombre = self.faker.word().capitalize()
        descripcion = self.faker.paragraph()
        calorias = str(self.faker.random_int(min=5, max=500))
        urls_invalidas = [
            "",
            "http://" + self.faker.domain_name(),
            "https://www.youtube.com/",
            "https://www.youtube.com/watch",
        ]
        
        for url in urls_invalidas:
            with self.assertRaises(ValueError):
                self.logica.crear_ejercicio(
                    nombre,
                    descripcion,
                    url,
                    calorias
                )

    def test_eliminar_ejercicio(self):
        #Crear ejercicio de prueba
        self.logica.crear_ejercicio("Sentarse", self.faker.sentence(), "https://www.youtube.com/watch?v=ID1057594393",str(self.faker.random_int(min=1, max=500)))
        # Buscar el ejercicio en la DB
        ejercicios = self.logica.dar_ejercicios()
        # Buscar el ejercicio por nombre (No tomando el último por prbar)
        ejercicio_encontrado = next((e for e in ejercicios if e["nombre"] == "Sentarse"), None)

        # Validar que se encontró antes de intentar eliminarlo
        if ejercicio_encontrado:
            id_ejercicio = ejercicio_encontrado["id"]
            self.logica.eliminar_ejercicio(id_ejercicio)

        # Obtener la lista de ejercicios después de eliminar
        ejercicios_despues = self.logica.dar_ejercicios()

        id_encontrado = -1
        for ejercicio in ejercicios_despues:
            if ejercicio["id"] == id_ejercicio:
                id_encontrado = 1

        self.assertEqual(id_encontrado, -1) # No debe encontrar el ejercicio "sentarse

    def test_editar_ejercicio(self):
        #Crear ejercicio de prueba
        self.logica.crear_ejercicio(self.faker.word(), self.faker.sentence(), "https://www.youtube.com/watch?v=ID555222555", str(self.faker.random_int(min=1, max=500)))
        # Buscar el ejercicio en la DB
        ejercicios = self.logica.dar_ejercicios()
        # Buscar el ejercicio por nombre (No tomando el último por prbar)
        ejercicio_encontrado = next((e for e in ejercicios if e["youtube"] == "https://www.youtube.com/watch?v=ID555222555"), None)

        # Validar que se encontró antes de intentar eliminarlo
        if ejercicio_encontrado:
            id_ejercicio = ejercicio_encontrado["id"]

        # Datos nuevos para la edición
        nuevo_nombre = "Programar en la tarde"
        nueva_descripcion = self.faker.sentence()
        nuevo_enlace = "https://www.youtube.com/watch?v=xyz1234"
        nuevas_calorias = str(self.faker.random_int(min=1, max=500))

        # Editar el ejercicio
        self.logica.editar_ejercicio(id_ejercicio, nuevo_nombre, nueva_descripcion, nuevo_enlace, nuevas_calorias)

        # Obtener el ejercicio actualizado
        ejercicios = self.logica.dar_ejercicios()
        # Buscar el ejercicio por nombre (No tomando el último por prbar)
        ejercicio_encontrado = next((e for e in ejercicios if e["id"] == id_ejercicio), None)

        # Validar que los cambios se aplicaron
        self.assertEqual(ejercicio_encontrado['nombre'], nuevo_nombre)
        self.assertEqual(ejercicio_encontrado['descripcion'], nueva_descripcion)
        self.assertEqual(ejercicio_encontrado['youtube'], nuevo_enlace)
        self.assertEqual(int(ejercicio_encontrado['calorias']), int(nuevas_calorias))

        self.logica.eliminar_ejercicio(id_ejercicio)

    # Pruebas unitarias HU004 - Terminar Entrenamiento Persona
    
    def test_dejar_entrenar_persona(self):

        datos_persona = {
            "nombre": self.faker.first_name(),
            "apellido": self.faker.last_name(),
            "edad": "25",
            "talla": "1.75",
            "peso": "70",
            "brazo": "30",
            "pecho": "90",
            "cintura": "80",
            "pierna": "50",
            "fecha_retiro" : "",
            "razon_retiro" : ""
        }

        # Crear persona
        self.logica.crear_persona(**datos_persona)

        # Validar que la persona creada está en la base de datos
        personas = self.logica.dar_personas()
        persona_creada = next((p for p in personas if (p["nombre"] == datos_persona["nombre"] and p["apellido"] == datos_persona["apellido"]) ), None)
        id_persona = persona_creada["id"]
        #self.logica.validar_dejar_de_entrenar_persona(id_persona, self.faker.date(), self.faker.sentence())
        self.logica.dejar_de_entrenar_persona(id_persona, self.faker.date(), self.faker.sentence())
        persona_actualizada = self.logica.dar_persona(id_persona)

        self.assertNotEqual(persona_creada["fecha_retiro"], persona_actualizada["fecha_retiro"])
        self.assertNotEqual(persona_creada["razon_retiro"], persona_actualizada["razon_retiro"])