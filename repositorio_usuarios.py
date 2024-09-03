#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente.
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo seguiría funcionando igual

usuarios_consultantes= [["guido", "holabebe"], ["matias", "123456"]]
usuarios_admin = [["nacho", "playstation"], ["yiya", "654321"]]
codigos_admin = [415465, 11123, 999846] #Codigos que debe tener al momento de registrarse un nuevo admin para validar el registro


def get_usuarios_consultantes():
    return usuarios_consultantes

def get_usuarios_admin():
    return usuarios_admin

def get_codigos_admin():
    return codigos_admin