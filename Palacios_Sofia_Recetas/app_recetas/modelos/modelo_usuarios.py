from app_recetas.config.mysqlconnection import connectToMySQL
from flask import flash, session
from app_recetas import BASE_DE_DATOS, EMAIL_REGEX, NOMBRE_REGEX



class Usuario:
    def __init__( self, data ):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        #self.recetas = []



    @classmethod
    def crear_uno( cls, data ):
        query = """
                INSERT INTO usuarios ( first_name, last_name, email, password )
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
                """
        id_usuario = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        return id_usuario
    
    @classmethod
    def selecciona_uno( cls, data ):
        query = """
                SELECT *
                FROM usuarios
                WHERE id = %(id)s;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        usuario_actual = Usuario( resultado[0] )
        return usuario_actual
    
    @classmethod
    def obtener_uno_con_email( cls, data ):    #en modelo ERD indicamos que el campo de email es unico, por eso es posible el siguiente query 
        query = """
                SELECT *
                FROM usuarios
                WHERE email = %(email)s;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )  #regresara dos posibles resultados: 1.objeto/instancia pq existe el usuario 2.una lista vacia
        if len( resultado ) == 0:
            return None
        else:
            return Usuario( resultado[0] )


    @staticmethod
    def validar_registro( data, existing_user ):
        es_valido = True

        if len( data['first_name'] ) < 2:
            es_valido = False
            flash( "Tu nombre debe tener al menos dos caracteres.", "error_nombre" )
        if not NOMBRE_REGEX.match( data['first_name'] ):
            es_valido = False
            flash( "Por favor porporciona un nombre válido (solo letras)", "error_nombre" )
        if len( data['last_name'] ) < 2:
            es_valido = False
            flash( "Tu apellido debe tener al menos dos caracteres.", "error_apellido" )
        if not NOMBRE_REGEX.match( data['last_name'] ):
            es_valido = False
            flash( "Por favor porporciona un apellido válido (solo letras)", "error_apellido" )
        if len( data['password'] ) < 8:
            es_valido = False
            flash( "Tu contraseña necesita tener al menos 8 caracteres.", "error_password" )
        if data['password'] != data['confirmar_password']:
            es_valido = False
            flash( "Las contraseñas no coincided.", "error_password" )
        if not EMAIL_REGEX.match( data['email'] ):
            es_valido = False
            flash( "Por favor porporciona un email válido", "error_email" )
        if existing_user is not None:
            flash("El usuario ya existe en la base de datos.", "error_email")
        return es_valido
    
    @staticmethod
    def validar_login( data ):
        es_valido = True
        if data == None:
            flash( "Este correo no existe.", "error_email_login" )
            es_valido = False
        
        return es_valido
    
    @staticmethod 
    def valida_sesion():
        if 'id' in session:
            return True
        else:
            return False