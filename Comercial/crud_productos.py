import psycopg2
 
class GestorProductos:
    """Clase que agrupa todas las operaciones sobre la tabla productos."""
 
    # -- Constructor: se conecta a la base al crear el objeto --
    def __init__(self, host, port, dbname, user, password):
        self.conexion = psycopg2.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
        self.cursor = self.conexion.cursor()
        print("Conexion exitosa a la base de datos")
 
    # -- CREATE: insertar un producto nuevo --
    def crear(self, nombre, precio, stock):
        try:
            self.cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                (nombre, precio, stock)
            )

            #Se revisa si el stock o precio ingresado es negativo
            if(int(stock) < 0 or int(precio) < 0):
                print("No se puede ingresar un valor negativo. Por favor ingrese otro valor.")
                return

            self.conexion.commit()
            print(f"Producto '{nombre}' insertado correctamente")
        except psycopg2.Error as e:
            # Si algo falla (por ejemplo, email repetido), deshacemos el cambio
            self.conexion.rollback()
            print("No se pudo insertar el producto:", e)
 
    # -- READ: listar todos los productos --
    def listar(self):
        self.cursor.execute(
            "SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay productos cargados")
            return
        print(f"{'ID':<4}{'Nombre':<20}{'Precio':<25}{'Stock':<20}")
        print("-" * 69)
        for f in filas:
            print(f"{f[0]:<4}{f[1]:<20}{f[2]:<25}{f[3]:<20}")
 
    # -- UPDATE: modificar el stock de un producto --
    def modificar_stock(self, id_producto, nuevo_stock):
        if(int(nuevo_stock) < 0):
            print("No se puede ingresar un valor negativo. Ingrese otro valor.")
            return

        self.cursor.execute(
            "UPDATE productos SET stock = %s WHERE id_producto = %s",
            (nuevo_stock, id_producto)
        )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Producto actualizado ({self.cursor.rowcount} fila modificada)")
        else:
            print("No se encontro ningun producto con ese id")

    # -- UPDATE: modificar el precio de un producto --
    def modificar_precio(self, id_producto, nuevo_precio):
        if(int(nuevo_precio) < 0):
            print("No se puede ingresar un valor negativo. Ingrese otro valor.")
            return
        
        self.cursor.execute(
            "UPDATE productos SET precio = %s WHERE id_producto = %s",
            (nuevo_precio, id_producto)
        )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Producto actualizado ({self.cursor.rowcount} fila modificada)")
        else:
            print("No se encontro ningun producto con ese id")
 
    # -- DELETE: borrar un producto --
    def borrar(self, id_producto):
        try:
            self.cursor.execute(
                "DELETE FROM productos WHERE id_producto = %s",
                (id_producto,)
            )
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                print(f"Producto borrado ({self.cursor.rowcount} fila eliminada)")
            else:
                print("No se encontro ningun producto con ese id")
        except psycopg2.Error as e:
            # Un producto con pedidos no se puede borrar (clave foranea)
            self.conexion.rollback()
            print("No se pudo borrar el producto: tiene pedidos asociados.")
 
    # -- Cerrar la conexion --
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        print("Conexion cerrada. Hasta luego!")
 
 
# ------------------------------------------------------------
#  Funcion que muestra el menu de opciones
# ------------------------------------------------------------
def mostrar_menu():
    print("\n===== GESTION DE PRODUCTOS =====")
    print("1. Agregar Producto")
    print("2. Listar Productos")
    print("3. Modificar stock de un producto")
    print("4. Modificar precio de un producto")
    print("5. Borrar producto")
    print("6. Salir")
    print("===============================")
 
 
# ------------------------------------------------------------
#  Programa principal
# ------------------------------------------------------------
def main():
    # Creamos el objeto gestor (se conecta a la base)
    gestor = GestorProductos(
        host="localhost",
        port=5432,
        dbname="comercio",
        user="postgres",
        password="Marlenesita004"
    )
 
    while True:
        mostrar_menu()
        opcion = input("Elija una opcion (1-6): ")
 
        if opcion == "1":
            nombre = input("Nombre: ")
            precio = input("Precio: ")
            stock = input("Stock: ")
            gestor.crear(nombre, precio, stock)
 
        elif opcion == "2":
            gestor.listar()
 
        elif opcion == "3":
            id_producto = input("Id del producto a modificar: ")
            nuevo_stock = input("Nuevo stock: ")
            gestor.modificar_stock(id_producto, nuevo_stock)

        elif opcion == "4":
            id_producto = input("Id del producto a modificar: ")
            nuevo_precio = input("Nuevo precio: ")
            gestor.modificar_precio(id_producto, nuevo_precio)
 
        elif opcion == "5":
            id_producto = input("Id del producto a borrar: ")
            gestor.borrar(id_producto)
 
        elif opcion == "6":
            gestor.cerrar()
            break
 
        else:
            print("Opcion invalida. Intente de nuevo.")
 
 
# Punto de entrada del programa
if __name__ == "__main__":
    main()