from app_recetas import app
from app_recetas.controladores import controlador_usuarios
from app_recetas.controladores import controlador_recetas


if __name__ == "__main__":
    app.run( debug = True, port = 5001 )