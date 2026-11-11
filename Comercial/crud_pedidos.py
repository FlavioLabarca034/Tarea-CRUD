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
        self.cursor.execute(
            "SELECT stock FROM productos WHERE id_producto = %s",
            (id_producto)
        )
        cant_actual = self.cursor.fetchone()
        if(int(cantidad) < 0):
            print("Error: no se puede ingresar una cantidad negativa. Por favor ingrese una cantidad positiva.")
            return
        if(int(cantidad) > cant_actual[0]):
            print("Error: no se puede ingresar una cantidad mayor que la del producto. Por favor ingrese un valor menor.")
            return
        try:
            self.cursor.execute(
                "INSERT INTO pedidos (id_cliente, id_producto, cantidad) VALUES (%s, %s, %s)",
                (id_cliente, id_producto, cantidad)
            )
            self.conexion.commit()
            print(f"Pedido de {cantidad} unidades insertado correctamente")
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
        print(f"{'ID':<4}{'ID Cliente':<4}{'ID Producto':<4}{'Cantidad':<4}")
        print("-" * 69)
        for f in filas:
            print(f"{f[0]:<4}{f[1]:<4}   {f[2]:<4}         {f[3]:<4}")
 
    # -- UPDATE: modificar la cantidad de un pedido --
    def modificar(self, id_pedido, nueva_cantidad):
        if(int(nueva_cantidad) < 0):
            print("Error: no se puede ingresar una cantidad negativa. Por favor ingrese una cantidad positiva.")
            return
        self.cursor.execute(
            "SELECT id_producto FROM pedidos WHERE id_pedido = %s",
            (id_pedido)
        )
        resultado = 1
        id_producto = self.cursor.fetchone()
        self.cursor.execute(
            "SELECT stock FROM productos WHERE id_producto = %s",
            (id_producto[0],)
        )
        cant_actual = self.cursor.fetchone()
        if(int(nueva_cantidad) > cant_actual[0]):
            print("Error: la nueva cantidad es mayor que el stock actual del producto. Por favor ingrese un valor menor.")
            return
        self.cursor.execute(
            "UPDATE pedidos SET cantidad = %s WHERE id_pedido = %s",
            (nueva_cantidad, id_pedido)
        )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Cantidad actualizada ({self.cursor.rowcount} fila modificada)")
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