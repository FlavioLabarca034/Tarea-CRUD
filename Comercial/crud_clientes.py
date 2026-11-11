import psycopg2
 
class GestorClientes:
    """Clase que agrupa todas las operaciones sobre la tabla clientes."""
 
    # -- Constructor: se conecta a la base al crear el objeto --
    def __init__(self, host, port, dbname, user, password):
        self.conexion = psycopg2.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
        self.cursor = self.conexion.cursor()
        print("Conexion exitosa a la base de datos")
 
    # -- CREATE: insertar un cliente nuevo --
    def crear(self, nombre, email, ciudad):
        try:
            self.cursor.execute(
                "INSERT INTO clientes (nombre, email, ciudad) VALUES (%s, %s, %s)",
                (nombre, email, ciudad)
            )
            self.conexion.commit()
            print(f"Cliente '{nombre}' insertado correctamente")
        except psycopg2.Error as e:
            # Si algo falla (por ejemplo, email repetido), deshacemos el cambio
            self.conexion.rollback()
            print("No se pudo insertar el cliente:", e)
 
    # -- READ: listar todos los clientes --
    def listar(self):
        self.cursor.execute(
            "SELECT id_cliente, nombre, email, ciudad FROM clientes ORDER BY id_cliente"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay clientes cargados")
            return
        print(f"{'ID':<4}{'Nombre':<20}{'Email':<25}{'Ciudad':<20}")
        print("-" * 69)
        for f in filas:
            print(f"{f[0]:<4}{f[1]:<20}{f[2]:<25}{f[3]:<20}")
 
    # -- UPDATE: modificar la ciudad de un cliente --
    def modificar(self, id_cliente, nueva_ciudad):
        self.cursor.execute(
            "UPDATE clientes SET ciudad = %s WHERE id_cliente = %s",
            (nueva_ciudad, id_cliente)
        )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Cliente actualizado ({self.cursor.rowcount} fila modificada)")
        else:
            print("No se encontro ningun cliente con ese id")
 
    # -- DELETE: borrar un cliente --
    def borrar(self, id_cliente):
        try:
            self.cursor.execute(
                "DELETE FROM clientes WHERE id_cliente = %s",
                (id_cliente,)
            )
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                print(f"Cliente borrado ({self.cursor.rowcount} fila eliminada)")
            else:
                print("No se encontro ningun cliente con ese id")
        except psycopg2.Error as e:
            # Un cliente con pedidos no se puede borrar (clave foranea)
            self.conexion.rollback()
            print("No se pudo borrar el cliente: tiene pedidos asociados.")
 
    # -- Cerrar la conexion --
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        print("Conexion cerrada. Hasta luego!")
 
 
# ------------------------------------------------------------
#  Funcion que muestra el menu de opciones
# ------------------------------------------------------------
def mostrar_menu():
    print("\n===== GESTION DE CLIENTES =====")
    print("1. Agregar cliente")
    print("2. Listar clientes")
    print("3. Modificar ciudad de un cliente")
    print("4. Borrar cliente")
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
            nombre = input("Nombre: ")
            email = input("Email: ")
            ciudad = input("Ciudad: ")
            gestor.crear(nombre, email, ciudad)
 
        elif opcion == "2":
            gestor.listar()
 
        elif opcion == "3":
            id_cliente = input("Id del cliente a modificar: ")
            nueva_ciudad = input("Nueva ciudad: ")
            gestor.modificar(id_cliente, nueva_ciudad)
 
        elif opcion == "4":
            id_cliente = input("Id del cliente a borrar: ")
            gestor.borrar(id_cliente)
 
        elif opcion == "5":
            gestor.cerrar()
            break
 
        else:
            print("Opcion invalida. Intente de nuevo.")
 
 
# Punto de entrada del programa
if __name__ == "__main__":
    main()