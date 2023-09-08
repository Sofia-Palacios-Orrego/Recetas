from flask import render_template, session, request, redirect, flash
from app_recetas import app
from flask_bcrypt import Bcrypt
from app_recetas.modelos.modelo_usuarios import Usuario

bcrypt = Bcrypt( app )

@app.route( '/', methods = ['GET'] )
def desplegar_login_registro():
    return render_template( 'registration_form.html' )


@app.route( '/nuevo/usuario', methods = ['POST'] )
def crear_usuario():
    data = {
            **request.form,        #copia todo el diccionario de request.form y lo pega en un nuevo diccionario (incluye el password no encriptado)
        }
    
    existing_user = Usuario.obtener_uno_con_email(data)
    if Usuario.validar_registro( data, existing_user ) == False:   #validar diccionario "data" creado a partir del request.form y si ya existe ese email en los datos
        return redirect ('/')
    else:
        password_encriptado = bcrypt.generate_password_hash( data['password'] ) #esta linea genera el password encriptado
        data['password'] = password_encriptado     #reescribe el password no encriptado y lo envia al diccionario "data" de arriba
        id_usuario = Usuario.crear_uno( data ) #el id que nos devuelve el query le ponemos "id_uduario"

        session['first_name'] = data['first_name']
        session['last_name'] = data['last_name']
        session['id_usuario'] = id_usuario
        return redirect( '/recetas' )



@app.route( '/login', methods = ['POST'] )  #user's email and password are extracted from the form data 
def procesa_login():
    data = {
        "email" : request.form['email_login'],
    }
    usuario_existe = Usuario.obtener_uno_con_email( data )    #method is called to retrieve the user's information based on the provided email
    
    if usuario_existe == None:
        flash ( "Este usuario no existe.", "error_email_login")
        return redirect('/') 
    else:
        if not bcrypt.check_password_hash( usuario_existe.password, request.form['password_login'] ):  #compara el password encriptado hash con el que esta ingresando el usuario. Parametros:  1. es el que esta encriptado y en la base de datos 2.es el que viene en el formulario 
            flash( "Credenciales incorrectas.", "error_password_login") 
            return redirect('/') 
        else: #If the passwords match, the user is considered authenticated, and their session data (name, email, and ID) is stored using the Flask session object.
            session['first_name'] = usuario_existe.first_name    
            session['last_name'] = usuario_existe.last_name
            session['id_usuario'] = usuario_existe.id
            return redirect( '/recetas' )


@app.route( '/logout', methods = ['POST'] )
def procesa_logout():
    session.clear()
    return redirect( '/' )