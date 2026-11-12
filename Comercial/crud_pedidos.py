import psycopg2
 
class GestorClientes:
    """Clase que agrupa todas las operaciones sobre la tabla pedidos."""
 
    # -- Constructor: se conecta a la base al crear el objeto --
    def __init__(self, host, port, dbname, user, password):
        self.conexion = psycopg2.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
        self.cursor = self.conexion.cursor()
        print("Conexion exitosa a la base de datos")
 
    # -- CREATE: insertar un pedido nuevo --
    def crear(self, id_cliente, id_producto, cantidad):

        #Se obtiene el stock total del producto y se lo asigna a la variable "cant_actual"
        self.cursor.execute(
            "SELECT stock FROM productos WHERE id_producto = %s",
            (id_producto,)
        )
        cant_actual = self.cursor.fetchone()
        #Se revisa si la cantidad actual tiene el valor "None", lo cual pasa si se ingresa un ID del producto invalido.
        if(cant_actual == None):
            print("Error: no se reconoce el ID del producto. Por favor ingrese un valor que se encuentre dentro de la lista.")
            return

        #Se verifica si la cantidad ingresada no es negativa
        if(int(cantidad) < 0):
            print("Error: no se puede ingresar una cantidad negativa. Por favor ingrese una cantidad positiva.")
            return

        #Se verifica si la cantidad ingresada es mayor que la cantidad actual disponible del producto (se añade un "[0]" ya que la variable "cant_actual" es una tupla)
        if(int(cantidad) > cant_actual[0]):
            print("Error: no se puede ingresar una cantidad mayor que la del producto. Por favor ingrese un valor menor.")
            return

        #Se crea la variable "cant_nueva" la cual es la resta entre la cantidad actual del producto y la cantidad ingresada
        cant_nueva = cant_actual[0] - int(cantidad)

        try:
            self.cursor.execute(
                "INSERT INTO pedidos (id_cliente, id_producto, cantidad) VALUES (%s, %s, %s)",
                (id_cliente, id_producto, cantidad)
            )

            #Se actualiza el stock actual del producto
            self.cursor.execute(
                "UPDATE productos SET stock = %s WHERE id_producto = %s",
                (cant_nueva, id_producto)
            )

            self.conexion.commit()
            print(f"Pedido de {cantidad} unidades insertado correctamente")
            print("Stock del producto actualizado.")
        except psycopg2.Error as e:
            # Se deshace el cambio si hay valores repetidos u otras fallas
            self.conexion.rollback()
            print("No se pudo insertar el pedido:", e)
 
    # -- READ: listar todos los pedidos --
    def listar(self):
        self.cursor.execute(
            "SELECT id_pedido, id_cliente, id_producto, cantidad FROM pedidos ORDER BY id_pedido"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay pedidos cargados")
            return
        print(f"{'ID':<4}{'ID Cliente':<20}{'ID Producto':<25}{'Cantidad':<20}")
        print("-" * 69)
        for f in filas:
            print(f"{f[0]:<4}{f[1]:<20}{f[2]:<25}{f[3]:<20}")
 
    # -- UPDATE: modificar la cantidad de un pedido --
    def modificar(self, id_pedido, nueva_cantidad):
        #Se verifica si la nueva cantidad es un numero negativo
        if(int(nueva_cantidad) < 0):
            print("Error: no se puede ingresar una cantidad negativa. Por favor ingrese una cantidad positiva.")
            return
        
        #Se obtiene el id del producto del pedido actual y se lo asigna a la variable "id_producto"
        self.cursor.execute(
            "SELECT id_producto FROM pedidos WHERE id_pedido = %s",
            (id_pedido,)
        )
        
        id_producto = self.cursor.fetchone()

        #Se verifica si el id del producto es "None", es decir, el ID del pedido es invalido
        if(id_producto == None):
            print("Error: No se reconoce el ID del pedido. Por favor ingrese un valor que se encuentre dentro de la lista.")
            return

        #Se obtiene el stock total del producto mediante la variable "id_producto" recien obtenida, y se lo asigna a la variable "cant_actual"
        self.cursor.execute(
            "SELECT stock FROM productos WHERE id_producto = %s",
            (id_producto[0],)
        )
        cant_actual = self.cursor.fetchone()

        #Se obtiene la cantidad antigua del pedido y se lo asigna a la variable "cant_vieja"
        self.cursor.execute(
            "SELECT cantidad FROM pedidos WHERE id_pedido = %s",
            (id_pedido,)
        )
        cant_vieja = self.cursor.fetchone()

        #Se crea la variable "diferencia" la cual es la resta entre la cantidad vieja y la nueva
        diferencia = cant_vieja[0] - int(nueva_cantidad)

        #Se crea variable "stock nuevo" la cual es la suma (o resta) entre la cantidad actual y la diferencia
        stock_nuevo = cant_actual[0] + diferencia

        #Se verifica si el stock nuevo es negativo. Es decir, que la cantidad modificada supere a la cantidad actual
        if(stock_nuevo < 0):
            print("Error: la nueva cantidad es mayor que el stock actual del producto. Por favor ingrese un valor menor.")
            return

        self.cursor.execute(
            "UPDATE pedidos SET cantidad = %s WHERE id_pedido = %s",
            (nueva_cantidad, id_pedido)
        )

        #Se actualiza el stock del producto con el stock nuevo
        self.cursor.execute(
            "UPDATE productos SET stock = %s WHERE id_producto = %s",
            (stock_nuevo, id_producto)
        )

        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Cantidad actualizada ({self.cursor.rowcount} fila modificada)")
            print("Stock del producto actualizado.")
        else:
            print("No se encontro ningun pedido con ese id")
 
    # -- DELETE: borrar un pedido --
    def borrar(self, id_pedido):
        self.cursor.execute(
            "DELETE FROM pedidos WHERE id_pedido = %s",
            (id_pedido,)
            )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Pedido borrado ({self.cursor.rowcount} fila eliminada)")
        else:
            print("No se encontro ningun pedido con ese id")
 
    # -- Cerrar la conexion --
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        print("Conexion cerrada. Hasta luego!")
 
 
# ------------------------------------------------------------
#  Funcion que muestra el menu de opciones
# ------------------------------------------------------------
def mostrar_menu():
    print("\n===== GESTION DE PEDIDO =====")
    print("1. Agregar pedido")
    print("2. Listar pedidos")
    print("3. Modificar cantidad de un pedido")
    print("4. Borrar pedido")
    print("5. Salir")
    print("===============================")
 
 
# ------------------------------------------------------------
#  Programa principal
# ------------------------------------------------------------
def main():
    # Creamos el objeto gestor (se conecta a la base)
    gestor = GestorClientes(
        host="localhost",
        port=5432,
        dbname="comercio",
        user="postgres",
        password="Marlenesita004"
    )
 
    while True:
        mostrar_menu()
        opcion = input("Elija una opcion (1-5): ")
 
        if opcion == "1":
            id_cliente = input("ID del cliente: ")
            id_producto = input("ID del producto: ")
            cantidad = input("Cantidad del producto: ")
            gestor.crear(id_cliente, id_producto, cantidad)
 
        elif opcion == "2":
            gestor.listar()
 
        elif opcion == "3":
            id_pedido = input("Id del pedido a modificar: ")
            nueva_cantidad = input("Nueva cantidad: ")
            gestor.modificar(id_pedido, nueva_cantidad)
 
        elif opcion == "4":
            id_cliente = input("Id del pedido a borrar: ")
            gestor.borrar(id_cliente)
 
        elif opcion == "5":
            gestor.cerrar()
            break
 
        else:
            print("Opcion invalida. Intente de nuevo.")
 
 
# Punto de entrada del programa
if __name__ == "__main__":
    main()