#Como todavía no sabemos trabajar con archivos, en este repositorio vamos a generar los datos de prueba temporalmente
#Para manipular los datos se van a llamar a funciones creadas en este repositorio, las cuales nos van a permitir no
#modificar la lógica de la funcion main/de la funcion que llame a los datos del repositorio.
#Una vez que cambiemos a archivos se reemplazan los datos de prueba con el acceso al archivo y todo sigue igual


#Esto estaría bueno que sea una tupla en un futuro
#vuelo = {id: number, aerolinea: string, modelo: string, capacidad: number, fecha_salida-llegada: number?, origen-destino: string, puerta_embarque: string, terminal: string, tripulacion: tupla, pasajeros: tupla?}
#Por ahora solo va a tener id, aerolinea, orige, destino, estado, fecha salida, fecha llegada (por ahora no consideramos zona hoaria)
vuelo1 = ["AA1234","Aerolineas Argentinas", "EZE","AEP","En horario", "11/11/2024-12:00", "11/11/2024-13:00"]
vuelo2 = ["BA4321", "British Airways", "EZE", "LHR", "Retrasado", "15/11/2024-18:00", "16/11/2024-09:00"]
vuelo3 = ["AF5678", "Air France", "EZE", "CDG", "Cancelado", "20/11/2024-13:00", "20/11/2024-22:00"]
vuelo4 = ["UA8765", "United Airlines", "EZE", "IAH", "En horario", "25/11/2024-23:30", "26/11/2024-07:30"]
vuelo5 = ["UA8765", "United Airlines", "EZE", "IAH", "Arribado", "25/11/2024-23:30", "26/11/2024-07:30"]
vuelos = [vuelo1, vuelo2, vuelo3, vuelo4, vuelo5]

def get_vuelos():
    return vuelos


#Por ahora estos son los unicos atributos modificables de un vuelo.
def modificar_estado_vuelos(id, estado):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[4] = estado
            return True
    return False

def modificar_destino_vuelos(id, destino):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[3] = destino
            return True
    return False

def modificar_fecha_salida_vuelos(id, fecha_salida):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[5] = fecha_salida
            return True
    return False

def modificar_fecha_llegada_vuelos(id, fecha_llegada):
    for vuelo in vuelos:
        if vuelo[0] == id:
            vuelo[6] = fecha_llegada
            return True
    return False

def eliminar_vuelo(id):
    for vuelo in vuelos:
        if vuelo[0] == id:
            del vuelo[0]
            return True
    return False
