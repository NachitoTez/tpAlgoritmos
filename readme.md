# Grupo 13 Sistema de Control de Tráfico Aéreo

## Integrantes:

- Guido Leonel Contartese L.U 1192909
- Ignacio Ramirez L.U 1172556
- Frank Ali Lopez Jimenez L.U 1190169

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
- def registracion() -> Que permita registrarse al sistema como usuario o admin, en el caso de querer registrarse como admin se debe ingresar la contraseña que es la misma para todos. GUIDO **CORRECTA, A VERIFICAR SI ES NECESARIO USAR REGEX PARA VALIDAR CONTRASEÑAS**
- def administrador () -> La misma se ejecutaria al seleccionarse desde el ingreso en el main, para poder validarse
  se debera registrar como el mismo validandolo en el sistema segun los usuarios y contraseñas almacenadas. GUIDO

  - def validar_usuario(admin) -> En la misma se pedira el ingreso de usuario y contraseña y cotejandolo con el archivo json que tendremos con todos los users y contraseñas de admin, devolviendo un booleano segun corresponda de la validacion con la base de datos del sistema. GUIDO **LISTA**
    - def ingreso_vuelo() -> En el mismo el administrador podrá agregar en la base de datos existente de vuelos
      registrados uno nuevo con su numero de vuelo, aerolinea, aeropuertos de origen, aeropuerto de destino, horario de salida y/o horario de llegada según corresponda.GUIDO **A TERMINAR**
    - def validacion_numeroVuelo(numero) auxiliar validacion -> Devolverá un booleano segun el ingreso del
      numero de vuelo asistema del administrador verificando que arranque con 2 letras y consecuentemente 5 numeros EJ: (XX11111). GUIDO
    - def modificacion_vuelo(numero_vuelo) -> En la misma una vez obteniendo los datos registrados en el sistema
      del dicho numero de vuelo se podrán hacer los cambios necesarios segun requiera el administrador. NACHO **LISTA**
    - def eliminar_vuelo(numero_vuelo) - > En el caso de que sea necesaria la eliminacion del sistema un
      vuelo según corresponda. NACHO **LISTA**
    - def consultar_vuelos() -> Que permita ver un listado de todos los vuelos registrados en el sistema. Y
      ademas permita las opciones si se quiere filtrar segun una aerolinea/dia/aeropuerto. NACHO **LISTA**
    - def agregar_aeropuerto(lugar_origen, lugar_destino) -> Agrega un aeropuerto a la lista de aeropuertos.
    - def eliminar_aeropuerto(lugar_origen, lugar_destino) -> Elimina un aeropuerto de la lista de aeropuertos.

- def consultante() -> en la misma se desplegará un listado de opciones que podra seleccionar/consultar el usuario.
- def validar_usuario(consultante) -> Cotejara con un archivo json con toda la gente registrada como consultante  
   para validar que este en el sistema. GUIDO **LISTA**

  - def menu_opciones() -> contendra las opciones para poder ir a cualquiera de las funciones de debajo. Frank
    '- def consultar_informacion_de_avion() -> Permite ver toda la informacion de los aviones comerciales mas a detalle Frank
    - def consultar_vuelos(criterio) -> Mostrara los dintintos estados de todos los vuelos, asi como el punto de partita y la llegada del mismo, con tiempo estimado (arribos, partidas, a definir mas) Frank
    - def consultar_vuelos_asientos_disponibles() -> Una vez ingresados los datos aeropuertos de origen y destino y dia de viaje el sistema muestre los vuelos que tenga asientos disponibles de compra. Frank
    - def consultar_estado_vuelo(numero_vuelo) -> Que devuelva el estado del mismo (En horario/Atrasado/Cancelado/Pre embarque/Embarcando/Despegado) Frank
    - def dibujar_mapa(lugar_origen, lugar_destino) -> Que muestre por consola un minimapa a escala del recorrido del avion.

  ¿Implementar alguna libreria relacionada a tiempo para poder limpiar la base de datos de vuelos realizados pasados los dias de que esten completados?
