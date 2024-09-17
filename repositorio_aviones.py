#Este repositorio almacenara los datos de los aviones, los cuales se podran utilizar para mostrar solo la info o poder utilizarlo para armar vuelos a los distintos vuelos
#avion = [nombre, capacidad de pasajero, maxima distancia, altura de vuelo maximo, velocidad maxima]
avion1 =["Boing 737", "230", "6,570 km", "12,497 m", "876 km/h"]
avion2 =["Airbus A320", "240", "6,300 km", "12,131 m", "871 km/h"]
avion3 =["Boeing 777", "396", "15,843 km", "13,140 m", "950 km/h"]
avion4 =["Airbus A350", "410", "16,100 km", "13,106 m", "903 km/h"]
avion5 =["Boeing 787", "330", "14,140 km", "13,137 m", "903 km/h"]
avion6 =["Airbus A380", "853", "15,200 km", "13,100 m", "1,020 km/h"]
avion7 =["Boeing 747", "524", "14,320 km", "13,716 m", "988 km/h"]

aviones = [avion1, avion2, avion3, avion4, avion5, avion6, avion7]


def get_aviones():
    return aviones

def avion_asignado(codigo):
    return aviones[codigo]