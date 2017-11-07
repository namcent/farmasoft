#FarmaSoft

#Flujo del programa

El programa se desarrolla en el archivo app.py donde se encuentran las rutas y clases utilizadas. A partir del login y/o registro del usuario (chequeado con el archivo usuarios.csv) se visualiza la tabla de ultimas ventas (que toma los datos del archivo ventas.csv, previamente ordenado y chequeado en la clase de reader y helper) y las opciones de consultas, cada una en una ruta distinta que redirecciona a un template diferente, en algunos casos con el pedido de un parametro para realizar la peticion. En caso de inactividad del usuario o al salir del sistema y querer ingresar a alguna consulta se redirecciona al form del login.

#Estructura para representar la informacion del archivo

Se utilizaron archivos csv donde la informacion es volcada en tablas en el template.

#Modo de uso del programa

Al acceder al sistema se visualiza una bienvenida y se solicita al usuario que se loguee o registre para continuar.

Una vez logueado en el sistema se ven las últimas ventas y se visualizan las opciones de consulta en la lista del menu superior. Las mismas son búsquedas de Clientes por Producto (donde se debe ingresar el producto como parámetro para visualizar los clientes que adquirieron el mismo) , Productos por cliente (donde se debe ingresar el cliente como parámetro), Productos mas vendidos (donde se compara la cantidad de productos adquiridos) y Mejores Clientes (por cantidad de dinero gastada). 

El sistema además cuenta con un cierre de sesión automático si el usuario no realiza una acción durante los siguientes 5 minutos.

#Clases utilizadas

Se utilizo una clase para encontrar la ubicacion de cada elemento en el encabezado (Helper), se utilizo una clase para las excepciones (CSVException) y otra clase para la lectura y verificacion de los errores propiamente dicha (CSVReader). 
Hay dos clases mas en el archivo forms.py que son para el manejo de las validaciones del formulario de login (LoginForm) y el formulario de registro (RegistrarForm).
