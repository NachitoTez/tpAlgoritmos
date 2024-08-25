# Grupo 13 Sistema de Control de Tráfico Aéreo
## Integrantes:
-   Guido Leonel Contartese L.U 1192909
### Contenido a implementar:
- Listas: Para manejar aviones en tránsito, aeropuertos y pilotos.
- Matrices/Diccionarios: Para representar el espacio aéreo y la posición de los aviones en diferentes altitudes y zonas.
- Archivos: Para registrar vuelos, incidentes y rutas aéreas.
- Funciones Lambda: Poder hacer el filtrado de vuelos segun aerolineas/destinos/origen.
- Recursividad: Para coordinar las rutas de los aviones evitando colisiones y optimizando las trayectorias.
- Excepciones: Para manejar datos erroneos ingresados por el usuario del sistema.

### Posible Esquematización del sistema:

- def main() -> Funcion que nos servirá como menu principal de nuestros sistema mostrando como una primera seleccion
                para el usuario identificarse en el mismo como administrador o consultante.
- def administrador () -> La misma se ejecutaria al seleccionarse desde el ingreso en el main, para poder validarse
                          se debera registrar como el mismo validandolo en el sistema segun los usuarios y contraseñas almacenadas. 
    - def validar_Administrador() -> En la misma se pedira el ingreso de usuario y contraseña, devolviendo un booleano
                                    segun corresponda de la validacion con la base de datos del sistema.
    - def ingreso_vuelo() -> En el mismo el administrador podrá agregar en la base de datos existente de vuelos 
                             registrados uno nuevo con su numero de vuelo, aerolinea, aeropuertos de origen, aeropuerto de destino, horario de salida y/o horario de llegada según corresponda.
    - def validacion_numeroVuelo(numero) -> Devolverá un booleano segun el ingreso del numero de vuelo al sistema
                                            del administrador verificando que arranque con 2 letras y consecuentemente 5 numeros EJ: (XX11111).
    - def modificacion_vuelo(numero_vuelo) -> En la misma una vez obteniendo los datos registrados en el sistema
                                              del dicho numero de vuelo se podrán hacer los cambios necesarios segun requiera.
    - def eliminar_vuelo(numero_vuelo) - > En el caso de que sea necesaria la eliminacion del sistema un 
                                           vuelo según corresponda.
    - def consultar_vuelos() -> Que permita ver un listado de todos los vuelos registrados en el sistema. Y ademas
                                permita las opciones si se quiere filtrar segun una aerolinea/dia/aeropuerto.
- def consultante() -> en la misma se desplegará un listado de opciones que podra seleccionar/consultar el usuario.
    - def consultar_vuelos_arribos() -> Que permita ver un listado de todos los vuelos registrados que ingresan, filtrando por aerolinea/dia/aeropuerto.
    - def consultar_vuelos_partidas() -> Que permita ver un listado de todos los vuelos registrados que parten, filtrando por aerolinea/dia/aeropuerto.
    - def consultar_vuelos_asientos_disponibles() -> Una vez ingresados los datos aeropuertos de origen y destino y
                                                    dia de viaje el sistema muestre los vuelos que tenga asientos disponibles de compra. 
    
                            

