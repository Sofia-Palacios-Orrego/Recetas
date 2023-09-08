from app_recetas.config.mysqlconnection import connectToMySQL
from flask import flash
from app_recetas import BASE_DE_DATOS
from app_recetas.modelos.modelo_usuarios import Usuario


class Receta:
    def __init__( self, data ):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.duration = data["duration"]
        self.instrucciones = data["instrucciones"]
        self.fecha_elaboracion = data['fecha_elaboracion']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        self.id_usuario = data['id_usuario']
        self.usuario = None



    @classmethod
    def crear_uno( cls, data ):
        query = """
                INSERT INTO recetas ( nombre, descripcion, duration, instrucciones, fecha_elaboracion, id_usuario )
                VALUES ( %(nombre)s, %(descripcion)s, %(duration)s, %(instrucciones)s, %(fecha_elaboracion)s, %(id_usuario)s );
                """
        id_receta = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        return id_receta
    



    @classmethod
    def eliminar_uno( cls, data ):
        query = """
                DELETE FROM recetas
                WHERE id = %(id)s;
                """
        return connectToMySQL( BASE_DE_DATOS ).query_db( query, data )



    @classmethod
    def seleccionar_recetas_con_usuarios( cls ):   #join regular pq todas las recetas tienen que tener usuario
        query = """
                SELECT *
                FROM recetas r 
                JOIN usuarios u
                ON r.id_usuario = u.id;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query )
        lista_recetas = []
        for renglon in resultado:       #se recorre el resultado
            receta_actual = Receta( renglon )
            datos_usuario = {
                "id" : renglon["u.id"],
                "first_name" : renglon["first_name"],
                "last_name" : renglon["last_name"],
                "email" : renglon["email"],
                "password" : renglon["password"],
                "fecha_creacion" : renglon["u.fecha_creacion"],
                "fecha_actualizacion" : renglon["u.fecha_actualizacion"]
            }
            usuario = Usuario( datos_usuario )  #se crea la instancia de usuario
            receta_actual.usuario = usuario          #ahora se le agrega a la receta
            lista_recetas.append( receta_actual )       #se agrega la instancia de recetas a la lista de recetas
        return lista_recetas
    



    @classmethod
    def seleccionar_receta_con_usuario( cls, data ):
        query = """
                SELECT *
                FROM recetas r 
                JOIN usuarios u
                ON r.id_usuario = u.id
                WHERE r.id = %(id)s;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        renglon =  resultado[0]  #ahora creamos una instancia no una lista como antes, pero el resultado igualmente trae una lista a pesar de ser una receta por lo que se usa renglon con indice 0 
        receta = Receta(renglon)
        datos_usuario = {
            "id" : renglon["u.id"],
            "first_name" : renglon["first_name"],
            "last_name" : renglon["last_name"],
            "email" : renglon["email"],
            "password" : renglon["password"],
            "fecha_creacion" : renglon["u.fecha_creacion"],
            "fecha_actualizacion" : renglon["u.fecha_actualizacion"]
        }
        receta.usuario = Usuario (datos_usuario)
        return receta     #ya no devolvemos una lista, sino que un objeto. Tenemos un objeto de la receta e internamente el objeto del usuario
    


    @classmethod
    def seleccionar_uno( cls, data ):
        query = """
                SELECT * FROM recetas
                WHERE id = %(id)s;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        receta = Receta (resultado[0])
        return receta
    


    @classmethod
    def editar_uno( cls, data ):
        query = """
                UPDATE recetas
                SET nombre = %(nombre)s, descripcion =%(descripcion)s, duration=%(duration)s, instrucciones =%(instrucciones)s, fecha_elaboracion=%(fecha_elaboracion)s
                WHERE id = %(id)s;
                """
        return connectToMySQL( BASE_DE_DATOS ).query_db( query, data )



    @staticmethod
    def validar_recetas( data ):
        es_valido = True

        if len( data['nombre'] ) < 3:
            es_valido = False
            flash( "El nombre de la receta debe tener al menos 3 caracteres", "error_nombre" )
        if len( data['descripcion'] ) < 3:
            es_valido = False
            flash( "La descripción debe tener al menos 3 caracteres", "error_descripcion" )
        if len( data['instrucciones'] ) < 3:
            es_valido = False
            flash( "Las instrucciones deben tener al menos 3 caracteres", "error_instrucciones" )
        if data['ciudad']  == "":
                es_valido = False
                flash( "Debes proporcionar la ciudad de origen del grupo.", "error_ciudad" )
        return es_valido

