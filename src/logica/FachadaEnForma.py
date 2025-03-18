'''
Esta clase es la fachada con los métodos a implementar en la lógica
'''
from src.modelo.ejercicio   import Ejercicio
from src.modelo.persona     import Persona
from src.modelo.entrenamiento import Entrenamiento

from src.modelo.declarative_base import Session, testDB, Base

# Herencia mientras se hacen los otros metodos
from src.logica.LogicaMock import LogicaMock

class FachadaEnForma():

    def __init__(self):
        
        # Logica aplicación Mock - Mientras se implementan todos los metodos
        self.logica = LogicaMock()

        # Inicializar la testDB (Posteriormente se carga la de producción)
        self.session = Session()

        # Se cargan las personas a la memoria
        self.personas = self.session.query(Persona).all()

    def dar_personas(self):
        ''' Retorna la lista de personas registradas en el sistema
        Retorna:
            (list): La lista con los dict o los objetos de personas
        '''
        personas = self.session.query(Persona).all()
        return  [ {k: v for k, v in persona.__dict__.items() if k != "_sa_instance_state"} for persona in personas ]

    def dar_persona(self, id_persona):
        ''' Retorna una persona a partir de su identificador
        Parámetros:
            id_persona (int): El identificador de la persona a retornar
        Retorna:
            (dict): La persona identificada con el id_persona recibido como parámetro
        '''
        persona = self.session.query(Persona).filter(Persona.id == id_persona).first()
        if persona:
            return {k: v for k, v in persona.__dict__.items() if k != "_sa_instance_state"}
    
        return {}  # Retorna dict vacio si no encuentra la persona        

    def validar_crear_editar_persona(self, id_persona, nombre, apellido, edad, talla, peso, brazo, pecho, cintura,
                                     pierna):
        ''' Valida que una persona se pueda crear o editar
        Parámetros:
            nombre (string): El nombre de la persona
            apellido (string): El apellido de la persona
            edad (string): La edad de la persona
            talla (string): La talla de la persona
            peso (string): El peso de la persona en Kg
            brazo (string): La medida del diametro del brazo de la persona en cm
            pecho (string): La medida del pecho de la persona en cm
            cintura (string): La medida de la cintura de la persona en cm
            pierna (string): La medida del diametro de la pierna de la persona en cm
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        errores = []

        # Validar nombre y apellido
        if not nombre or not isinstance(nombre, str) or nombre.strip() == "":
            errores.append("El nombre es obligatorio y debe ser un string válido.")
        if not apellido or not isinstance(apellido, str) or apellido.strip() == "":
            errores.append("El apellido es obligatorio y debe ser un string válido.")

        # Validar edad
        try:
            edad = int(edad)
            if edad <= 0:
                errores.append("La edad debe ser un número positivo mayor a 0.")
        except ValueError:
            errores.append("La edad debe ser un número entero válido.")

        # Validar talla (puede ser decimal)
        try:
            talla = float(talla)
            if talla <= 0:
                errores.append("La talla debe ser un número positivo mayor a 0.")
        except ValueError:
            errores.append("La talla debe ser un número decimal válido.")

        # Validar peso
        try:
            peso = int(peso)
            if peso <= 0:
                errores.append("El peso debe ser un número positivo mayor a 0.")
        except ValueError:
            errores.append("El peso debe ser un número entero válido.")

        # Validar medidas corporales
        for atributo, valor in [("brazo", brazo), ("pecho", pecho), ("cintura", cintura), ("pierna", pierna)]:
            try:
                valor = int(valor)
                if valor <= 0:
                    errores.append(f"La medida de {atributo} debe ser un número positivo mayor a 0.")
            except ValueError:
                errores.append(f"La medida de {atributo} debe ser un número entero válido.")

        # Retornar errores si existen
        return "\n".join(errores) if errores else ""

    def crear_persona(self, nombre, apellido, edad, talla, peso, brazo, pecho, cintura, pierna, fecha_retiro = "", razon_retiro = ""):
        ''' Crea una persona
        Parámetros:
            nombre (string): El nombre de la persona
            apellido (string): El apellido de la persona
            edad (string): La edad de la persona
            talla (string): La talla de la persona
            peso (string): El peso de la persona en Kg
            brazo (string): La medida del diametro del brazo de la persona en cm
            pecho (string): La medida del pecho de la persona en cm
            cintura (string): La medida de la cintura de la persona en cm
            pierna (string): La medida del diametro de la pierna de la persona en cm
        '''
        # Convertir valores a su tipo correcto
        edad = int(edad)
        talla = float(talla)
        peso = int(peso)
        brazo = int(brazo)
        pecho = int(pecho)
        cintura = int(cintura)
        pierna = int(pierna)

        # Crear instancia de Persona
        nueva_persona = Persona(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            talla=talla,
            peso=peso,
            brazo=brazo,
            pecho=pecho,
            cintura=cintura,
            pierna=pierna,
            fecha_retiro = fecha_retiro,
            razon_retiro = razon_retiro
        )

        # Guardar en la base de datos
        self.session.add(nueva_persona)
        self.session.commit()

    def editar_persona(self, id_persona, nombre, apellido, edad, talla, peso, brazo, pecho, cintura, pierna):
        ''' Edita una persona
        Parámetros:
            id_persona(int): El identificador de la persona que se va a editar
            nombre (string): El nombre de la persona
            apellido (string): El apellido de la persona
            edad (string): La edad de la persona
            talla (string): La talla de la persona
            peso (string): El peso de la persona en Kg
            brazo (string): La medida del diametro del brazo de la persona en cm
            pecho (string): La medida del pecho de la persona en cm
            cintura (string): La medida de la cintura de la persona en cm
            pierna (string): La medida del diametro de la pierna de la persona en cm
        '''
        persona = self.session.query(Persona).filter(Persona.id == id_persona).first()
        
        if not persona:
            return  # Si la persona no existe, simplemente no hace nada

        # Actualizar los valores
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = int(edad)
        persona.talla = float(talla)
        persona.peso = int(peso)
        persona.brazo = int(brazo)
        persona.pecho = int(pecho)
        persona.cintura = int(cintura)
        persona.pierna = int(pierna)

        self.session.commit()  # Guarda los cambios

    def eliminar_persona(self, id_persona):
        ''' Elimina una persona de la lista de personas
        Parámetros:
            id_persona (int): El identificador de la persona que se desea eliminar
        '''

        persona = self.session.query(Persona).filter(Persona.id == id_persona).first()

        if persona:
            self.session.delete(persona)
            self.session.commit()

    def dar_ejercicios(self):
        ''' Retorna la lista de ejercicios
        Retorna:
            (list): La lista con los dict o los objetos de los ejercicios
        '''
        ejercicios = self.session.query(Ejercicio).all()
        return  [ {k: v for k, v in ejercicio.__dict__.items() if k != "_sa_instance_state"} for ejercicio in ejercicios ]


    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        ''' Valida que un ejercicio se pueda crear o editar
        Parámetros:
            nombre (string): El nombre del ejercicio
            descripcion (string): La descripción del ejercicio
            enlace (string): El enlace al video del ejercicio en YouTube
            calorias (string): El número de calorias consumidas por repetición del ejercicio
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        errores = []

        # Validar nombre
        if not nombre or not nombre.strip():
            errores.append("El nombre del ejercicio no puede estar vacío.")

        # Validar descripción
        if not descripcion or not descripcion.strip():
            errores.append("La descripción del ejercicio no puede estar vacía.")

        # Validar enlace (Debe contener 'youtube.com' o 'youtu.be')
        if not enlace or ("youtube.com" not in enlace and "youtu.be" not in enlace):
            errores.append("El enlace debe ser un video válido de YouTube.")

        # Validar calorías (Debe ser un número entero positivo)
        try:
            calorias = int(calorias)
            if calorias <= 0:
                errores.append("Las calorías deben ser un número positivo.")
        except ValueError:
            errores.append("Las calorías deben ser un número entero.")

        # Retornar errores como una cadena unida por saltos de línea, o una cadena vacía si no hay errores
        return "\n".join(errores) if errores else ""

    def crear_ejercicio(self, nombre, descripcion, enlace, calorias):
        ''' Crea un ejercicio
        Parámetros:
            nombre (string): El nombre del ejercicio
            descripcion (string): La descripción del ejercicio
            enlace (string): El enlace al video del ejercicio en YouTube
            calorias (int): El número de calorias consumidas por repetición del ejercicio
        Raises:
            ValueError: Si alguno de los campos está vacío o es inválido
        '''
        # Validar campos vacíos
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre del ejercicio no puede estar vacío")
            
        if not descripcion or descripcion.strip() == "":
            raise ValueError("La descripción del ejercicio no puede estar vacía")
            
        if not enlace or enlace.strip() == "":
            raise ValueError("El enlace de YouTube no puede estar vacío")

        enlace = enlace.strip()
        if not enlace.startswith("https://www.youtube.com/watch?v=") or \
           len(enlace) <= len("https://www.youtube.com/watch?v="):
            raise ValueError("El enlace debe ser una URL válida de YouTube (formato: https://www.youtube.com/watch?v=ID)")

        calorias = int(calorias)    
        if not isinstance(calorias, (int, float)) or calorias <= 0 :
            raise ValueError("Las calorías deben ser un número positivo")

        # Crear el ejercicio con los campos validados
        ejercicio = Ejercicio(
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            youtube=enlace,
            calorias=calorias
        )
        
        self.session.add(ejercicio)
        self.session.commit()

    def editar_ejercicio(self, id_ejercicio, nombre, descripcion, enlace, calorias):
        ''' Edita un ejercicio
        Parámetros:
            id_ejercicio(int): El identificador del ejercicio que se va a editar
            nombre (string): El nombre del ejercicio
            descripcion (string): La descripción del ejercicio
            enlace (string): El enlace al video del ejercicio en YouTube
            calorias (string): El número de calorias consumidas por repetición del ejercicio
        '''
        ejercicio = self.session.query(Ejercicio).filter(Ejercicio.id == id_ejercicio).first()
        if ejercicio:
            ejercicio.nombre = nombre
            ejercicio.descripcion = descripcion
            ejercicio.youtube = enlace
            ejercicio.calorias = calorias
            self.session.commit()

    def eliminar_ejercicio(self, id_ejercicio):
        ''' Elimina un ejercicio de la lista de ejercicios
        Parámetros:
            id_ejercicio (int): El identificador del ejercicio que se desea eliminar
        '''
        ejercicio = self.session.query(Ejercicio).filter(Ejercicio.id == id_ejercicio).first()
        if ejercicio:
            self.session.delete(ejercicio)
            self.session.commit()

    def dar_entrenamientos(self, id_persona):
        ''' Retorna la lista de entrenamientos de una persona
        Parámetros:
            id_persona (int): El identificador de la persona a consultar
        Retorna:
            (list): La lista con los dict o los objetos de los entrenamientos realizados por una persona
        '''
        persona = self.session.query(Persona).filter(Persona.id == id_persona).first()
        if not persona:
            return []  # Retornar una lista vacía en lugar de None o un dict
        
        entrenamientos = persona.entrenamientos.copy()
        return [
                    {
                        **{k: v for k, v in entrenamiento.__dict__.items() if k != "_sa_instance_state"},
                        "ejercicio": entrenamiento.ejercicio.nombre if entrenamiento.ejercicio else None
                    }
                    for entrenamiento in entrenamientos
                ]
        #return   [ {k: v for k, v in entrenamiento.__dict__.items() if k != "_sa_instance_state"} for entrenamiento in entrenamientos ]


    def validar_crear_editar_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        ''' Valida que se pueda crear o editar un entrenamiento
        Parámetros:
            persona (dict): dict con los datos de la persona
            ejercicio (string): El nombre del ejercicio realizado por la persona
            fecha (string): La fecha de realización del ejercicio
            repeticiones (string): El número de repeticiones hechas del ejercicio
            tiempo (string): El tiempo gastado
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        errores = []

        if not ejercicio or not isinstance(ejercicio, str) or ejercicio.strip() == "":
            errores.append("El nombre del ejercicio no puede estar vacío.")

        if not fecha or not isinstance(fecha, str):
            errores.append("La fecha debe ser una cadena de texto válida.")

        if not repeticiones or not isinstance(repeticiones, str) or int(repeticiones) <= 0:
            errores.append("Las repeticiones deben ser un número entero positivo.")

        if not tiempo or not isinstance(tiempo, str) or int(tiempo) <= 0:
            errores.append("El tiempo debe ser un número entero positivo.")

        return "\n".join(errores) if errores else ""

    def crear_entrenamiento(self, persona_dict, ejercicio, fecha, repeticiones, tiempo):
        ''' Crea un entrenamiento
        Parámetros:
            persona (dict): dict con los datos de la persona
            ejercicio (string): El nombre del ejercicio realizado por la persona
            fecha (string): La fecha de realización del ejercicio
            repeticiones (string): El número de repeticiones hechas del ejercicio
            tiempo (string): El tiempo gastado
        '''

        ejercicioEntrenamiento = self.session.query(Ejercicio).filter(Ejercicio.nombre == ejercicio).first()
        persona_query = self.session.query(Persona).filter(Persona.id == persona_dict['id']).first()
        entrenamiento = Entrenamiento(fecha = fecha, repeticiones = repeticiones, tiempo = tiempo, persona = persona_query, ejercicio = ejercicioEntrenamiento)

        self.session.add(entrenamiento)
        self.session.commit()


    def editar_entrenamiento(self, id_entrenamiento, persona, ejercicio, fecha, repeticiones, tiempo):
        ''' Edita un entrenamiento
        Parámetros:
            id_entrenamiento(int): El identificador del entrenamiento que se va a editar
            persona (dict): dict con los datos de la persona
            ejercicio (string): El nombre del ejercicio realizado por la persona
            fecha (string): La fecha de realización del ejercicio
            repeticiones (string): El número de repeticiones hechas del ejercicio
            tiempo (string): El tiempo gastado
        '''
        entrenamiento = self.session.query(Entrenamiento).filter(Entrenamiento.id == id_entrenamiento).first()
    
        if entrenamiento:
            entrenamiento.ejercicio = self.session.query(Ejercicio).filter(Ejercicio.nombre == ejercicio).first()
            entrenamiento.fecha = fecha
            entrenamiento.repeticiones = repeticiones
            entrenamiento.tiempo = tiempo

            self.session.commit()  # Guarda los cambios en la base de datos

    def eliminar_entrenamiento(self, id_entrenamiento, persona):
        ''' Elimina un entrenamiento de la lista de entrenamientos realizados por una persona
        Parámetros:
            id_entrenamiento (int): El identificador del entrenamiento que se desea eliminar
            persona (dict): dict con los datos de la persona
        '''

        # La relacion de persona no es usada, porque si se elimina persona, se borran los entrenamientos
        # Pero si se borra el entrenamiento no pasa nada con la persona

        entrenamiento = self.session.query(Entrenamiento).filter(Entrenamiento.id == id_entrenamiento).first()
    
        if entrenamiento:
            self.session.delete(entrenamiento)
            self.session.commit()  # Guarda los cambios en la base de datos

    def validar_dejar_de_entrenar_persona(self, id_persona, fecha, razon):
        ''' Valida que se pueda dejar de entrenar a una persona
        Parámetros:
            id_persona (int): El identificador de la persona que se desea dejar de entrenar
            fecha (string): La fecha en que dejó de entrenar
            razon (string): La descripción del motivo por el cual dejó de entrenar
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        errores = []

        # Validar que la fecha no esté vacía y sea válida
        if not isinstance(fecha, str):
            errores.append("La fecha debe ser una cadena de texto.")
    
        if not isinstance(fecha, str) or not razon.strip():
            errores.append("La razón debe ser una cadena de texto no vacía.")

        if not isinstance(razon, str) or not razon.strip():
            errores.append("La razón debe ser una cadena de texto no vacía.")

        return "\n".join(errores) if errores else ""  # Si todo es válido, retorna una cadena vacía

    def dejar_de_entrenar_persona(self, id_persona, fecha, razon):
        ''' Deja de entrenar a una persona
        Parámetros:
            id_persona (int): El identificador de la persona que se desea dejar de entrenar
            fecha (string): La fecha en que dejó de entrenar
            razon (string): La descripción del motivo por el cual dejó de entrenar
        '''
        persona = self.session.query(Persona).filter(Persona.id == id_persona).first()
        if persona:
            persona.fecha_retiro = fecha
            persona.razon_retiro = razon
            self.session.commit()

    def dar_reporte(self, id_persona):
        ''' Genera la información para el reporte de entrenamientos de una persona
        Parámetros:
            id_persona (int): El identificador de la persona
        Retorna:
            (dict): Un mapa con la información del reporte
        '''

        persona = self.session.query(Persona).filter(Persona.id == id_persona).first()

        entrenamientos_agrupados = {}
        total_calorias = 0
        total_repeticiones = 0
        
        for entrenamiento in persona.entrenamientos:
            fecha = entrenamiento.fecha
            repeticiones = entrenamiento.repeticiones
            calorias = entrenamiento.ejercicio.calorias * repeticiones

            total_calorias += calorias
            total_repeticiones += repeticiones
 
            if fecha not in entrenamientos_agrupados:
                entrenamientos_agrupados[fecha] = {
                    'fecha': fecha,
                    'repeticiones': repeticiones,
                    'calorias': calorias
                }
            else:
                entrenamientos_agrupados[fecha]['repeticiones'] += repeticiones
                entrenamientos_agrupados[fecha]['calorias'] += calorias

        entrenamientos_lista = list(entrenamientos_agrupados.values())

        imc = persona.peso / (persona.talla ** 2)

        nivel = ""

        if (imc < 18.5):
            nivel = "Bajo peso"
        elif (imc < 25):
            nivel = "Peso saludable"
        elif (imc < 30):
            nivel = "Sobrepeso"
        else:
            nivel = "Obesidad"

        estadistica = {'persona':persona.nombre, 'imc':imc, 'clasificacion': nivel, 'entrenamientos': entrenamientos_lista, 'total_repeticiones': total_repeticiones, 'total_calorias': total_calorias}

        persona = {k: v for k, v in persona.__dict__.items() if k != "_sa_instance_state"}

        return {'persona': persona, 'estadisticas': estadistica} 