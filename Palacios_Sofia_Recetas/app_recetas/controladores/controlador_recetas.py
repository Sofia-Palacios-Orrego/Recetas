from flask import render_template, session, request, redirect, flash
from app_recetas import app
#from flask_bcrypt import Bcrypt
from app_recetas.modelos.modelo_recetas import Receta



@app.route('/recetas', methods=['GET'])
def desplegar_recetas():
    if "id_usuario" not in session:
        return redirect ('/')
    else:
        lista_recetas = Receta.seleccionar_recetas_con_usuarios()
        return render_template("recetas.html", lista_recetas=lista_recetas)



@app.route('/formulario/receta', methods=['GET'])
def desplegar_formulario_receta ():
    if "id_usuario" not in session:
        return redirect ('/')
    else:
        return render_template('formulario_receta.html')



@app.route('/nueva/receta', methods=['POST'])
def crear_receta ():
    data = {        #creamos diccionarios y copias lo de la form y agregamos el id del usuario que esta en sesion
        **request.form,
            "id_usuario": session["id_usuario"]
    }
    if Receta.validar_recetas (data) == False:
        return redirect ('/formulario/receta')
    else:
        Receta.crear_uno(data)
        return redirect ('/recetas')




@app.route('/eliminar/receta/<int:id>', methods=['POST'])
def eliminar_receta (id):
    data= {
        "id": id
    }
    Receta.eliminar_uno(data)
    return redirect('/recetas')



@app.route('/receta/<int:id>', methods=['GET'])
def desplegar_informacion_receta (id):
    if "id_usuario" not in session:
        return redirect ('/')
    else:
        data= {
            "id": id
        }
        receta = Receta.seleccionar_receta_con_usuario (data)
        return render_template('info_receta.html', receta=receta)



@app.route('/formulario/editar/receta/<int:id>', methods=['GET'])
def desplegar_formulario_editar_receta (id):
    if "id_usuario" not in session:
        return redirect ('/')
    else:
        data= {
            "id": id
        }
        receta = Receta.seleccionar_uno(data)
        return render_template('editar_receta.html', receta=receta)


@app.route('/editar/receta/<int:id>', methods=['POST'])
def editar_receta (id):
    if Receta.validar_recetas (request.form) == False:
        return redirect('/cuenta/usuario')
    else:
        data= {
            **request.form,
            "id": id
        }
        Receta.editar_uno(data)
        return redirect ('/recetas')





