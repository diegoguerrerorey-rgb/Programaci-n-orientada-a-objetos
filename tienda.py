# mi proyecto final de poo2
# sistema de inventario para una tienda
# hecho en python

import csv
import os
from abc import ABC, abstractmethod  # esto es para las clases abstractas que vimos en clase

# --------------------------------------------------
# interfaces - son como contratos que obligan a implementar metodos
# --------------------------------------------------

# esta interfaz obliga a que se pueda guardar y cargar
class Persistible(ABC):
    @abstractmethod
    def guardar(self):
        pass

    @abstractmethod
    def cargar(self):
        pass

# esta otra interfaz es para el reporte
class Reportable(ABC):
    @abstractmethod
    def generar_reporte(self):
        pass


# --------------------------------------------------
# clase abstracta Producto (la clase padre de todo)
# --------------------------------------------------

class Producto(ABC):

    # constructor con los atributos basicos de cualquier producto
    def __init__(self, codigo, nombre, precio, cantidad):
        self.__codigo = codigo       # privado con doble guion bajo
        self.__nombre = nombre
        self.__precio = float(precio)
        self.__cantidad = int(cantidad)

    # getters para acceder a los atributos privados
    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_precio(self):
        return self.__precio

    def get_cantidad(self):
        return self.__cantidad

    # setters para modificar los atributos
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_precio(self, precio):
        self.__precio = float(precio)

    def set_cantidad(self, cantidad):
        self.__cantidad = int(cantidad)

    # este metodo es abstracto, cada subclase lo implementa diferente (polimorfismo)
    @abstractmethod
    def tipo(self):
        pass

    # para imprimir el producto bonito
    def __str__(self):
        return "[" + self.tipo() + "] " + self.__codigo + " | " + self.__nombre + " | $" + str(int(self.__precio)) + " | cantidad: " + str(self.__cantidad)


# --------------------------------------------------
# subclases que heredan de Producto
# --------------------------------------------------

# producto tipo alimento, tiene fecha de vencimiento
class ProductoAlimenticio(Producto):

    def __init__(self, codigo, nombre, precio, cantidad, fecha_venc):
        super().__init__(codigo, nombre, precio, cantidad)  # llama al constructor del padre
        self.fecha_venc = fecha_venc

    # implementacion del metodo abstracto tipo()
    def tipo(self):
        return "ALIMENTO"

    def __str__(self):
        return super().__str__() + " | vence: " + self.fecha_venc


# producto electronico, tiene garantia
class ProductoElectronico(Producto):

    def __init__(self, codigo, nombre, precio, cantidad, garantia_meses):
        super().__init__(codigo, nombre, precio, cantidad)
        self.garantia_meses = int(garantia_meses)

    def tipo(self):
        return "ELECTRONICO"

    def __str__(self):
        return super().__str__() + " | garantia: " + str(self.garantia_meses) + " meses"


# producto de ropa, tiene talla
class ProductoRopa(Producto):

    def __init__(self, codigo, nombre, precio, cantidad, talla):
        super().__init__(codigo, nombre, precio, cantidad)
        self.talla = talla

    def tipo(self):
        return "ROPA"

    def __str__(self):
        return super().__str__() + " | talla: " + self.talla


# --------------------------------------------------
# clase Inventario - aqui se maneja todo
# implementa las dos interfaces de arriba
# --------------------------------------------------

class Inventario(Persistible, Reportable):

    # la ruta del archivo donde se guardan los datos
    ARCHIVO = os.path.join(os.path.dirname(__file__), '..', 'datos', 'inventario.csv')

    def __init__(self):
        self.productos = []  # lista donde guardo todos los productos (como un ArrayList)
        self.cargar()  # cuando arranca el programa carga los datos guardados

    # guardar todos los productos en el csv
    def guardar(self):
        try:
            # creo la carpeta datos si no existe
            os.makedirs(os.path.dirname(self.ARCHIVO), exist_ok=True)
            archivo = open(self.ARCHIVO, 'w', newline='', encoding='utf-8')
            writer = csv.writer(archivo)
            writer.writerow(['tipo', 'codigo', 'nombre', 'precio', 'cantidad', 'extra'])

            for p in self.productos:
                if isinstance(p, ProductoAlimenticio):
                    writer.writerow(['ALIMENTO', p.get_codigo(), p.get_nombre(), p.get_precio(), p.get_cantidad(), p.fecha_venc])
                elif isinstance(p, ProductoElectronico):
                    writer.writerow(['ELECTRONICO', p.get_codigo(), p.get_nombre(), p.get_precio(), p.get_cantidad(), p.garantia_meses])
                elif isinstance(p, ProductoRopa):
                    writer.writerow(['ROPA', p.get_codigo(), p.get_nombre(), p.get_precio(), p.get_cantidad(), p.talla])

            archivo.close()
            print("datos guardados!")
        except Exception as e:
            print("error al guardar:", e)

    # cargar productos desde el csv
    def cargar(self):
        try:
            # si no existe el archivo no hace nada
            if not os.path.exists(self.ARCHIVO):
                return

            archivo = open(self.ARCHIVO, 'r', encoding='utf-8')
            reader = csv.DictReader(archivo)

            for fila in reader:
                t = fila['tipo']
                if t == 'ALIMENTO':
                    prod = ProductoAlimenticio(fila['codigo'], fila['nombre'], fila['precio'], fila['cantidad'], fila['extra'])
                    self.productos.append(prod)
                elif t == 'ELECTRONICO':
                    prod = ProductoElectronico(fila['codigo'], fila['nombre'], fila['precio'], fila['cantidad'], fila['extra'])
                    self.productos.append(prod)
                elif t == 'ROPA':
                    prod = ProductoRopa(fila['codigo'], fila['nombre'], fila['precio'], fila['cantidad'], fila['extra'])
                    self.productos.append(prod)

            archivo.close()
        except Exception as e:
            print("no se pudieron cargar datos:", e)

    # agregar un producto nuevo a la lista
    def agregar_producto(self, p):
        try:
            # primero verifico que no exista ya ese codigo
            if self.buscar_por_codigo(p.get_codigo()) != None:
                print("ese codigo ya existe!")
                return
            self.productos.append(p)
            self.guardar()
            print("producto agregado correctamente")
        except Exception as e:
            print("error:", e)

    # busca un producto por codigo, retorna None si no lo encuentra
    def buscar_por_codigo(self, codigo):
        encontrado = None
        for p in self.productos:
            if p.get_codigo() == codigo:
                encontrado = p
        return encontrado

    # eliminar un producto
    def eliminar_producto(self, codigo):
        try:
            p = self.buscar_por_codigo(codigo)
            if p != None:
                self.productos.remove(p)
                self.guardar()
                print("producto eliminado")
            else:
                print("no se encontro el producto con ese codigo")
        except Exception as e:
            print("error al eliminar:", e)

    # actualizar la cantidad de un producto
    def actualizar_stock(self, codigo, nueva_cantidad):
        try:
            p = self.buscar_por_codigo(codigo)
            if p != None:
                p.set_cantidad(int(nueva_cantidad))
                self.guardar()
                print("stock actualizado!")
            else:
                print("no existe ese codigo")
        except ValueError:
            print("la cantidad debe ser un numero")
        except Exception as e:
            print("error:", e)

    # mostrar todos los productos
    def listar_todos(self):
        if len(self.productos) == 0:
            print("no hay productos en el inventario")
        else:
            print("\n====== INVENTARIO ======")
            for p in self.productos:
                print(p)
            print("========================")
            print("total de productos:", len(self.productos))

    # reporte con el valor total
    def generar_reporte(self):
        total = 0
        print("\n====== REPORTE DE VALOR ======")
        for p in self.productos:
            subtotal = p.get_precio() * p.get_cantidad()
            total = total + subtotal
            print(p.get_nombre(), "->", "$" + str(int(subtotal)))
        print("------------------------------")
        print("TOTAL DEL INVENTARIO: $" + str(int(total)))
        print("==============================\n")


# --------------------------------------------------
# funciones del menu
# --------------------------------------------------

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# funcion para pedir numeros sin que el programa se caiga
def pedir_numero(mensaje, tipo=float):
    while True:
        try:
            valor = tipo(input(mensaje))
            return valor
        except ValueError:
            print("por favor ingrese un numero valido")

def menu_agregar(inv):
    print("\nque tipo de producto es?")
    print("1. Alimento")
    print("2. Electronico")
    print("3. Ropa")
    op = input("opcion: ")

    try:
        codigo = input("codigo del producto: ")
        nombre = input("nombre: ")
        precio = pedir_numero("precio: ", float)
        cantidad = pedir_numero("cantidad: ", int)

        if op == '1':
            fecha = input("fecha de vencimiento (ejemplo: 2026-06): ")
            nuevo = ProductoAlimenticio(codigo, nombre, precio, cantidad, fecha)
        elif op == '2':
            garantia = pedir_numero("meses de garantia: ", int)
            nuevo = ProductoElectronico(codigo, nombre, precio, cantidad, garantia)
        elif op == '3':
            talla = input("talla (S/M/L/XL): ").upper()
            nuevo = ProductoRopa(codigo, nombre, precio, cantidad, talla)
        else:
            print("opcion no valida")
            return

        inv.agregar_producto(nuevo)

    except Exception as e:
        print("ocurrio un error:", e)


# --------------------------------------------------
# programa principal
# --------------------------------------------------

def main():
    inv = Inventario()

    # si el inventario esta vacio pongo unos productos de ejemplo
    if len(inv.productos) == 0:
        inv.productos.append(ProductoAlimenticio('A001', 'Arroz Diana 1kg', 4500, 100, '2026-06'))
        inv.productos.append(ProductoAlimenticio('A002', 'Leche Alpina 1L', 3200, 60, '2025-09'))
        inv.productos.append(ProductoElectronico('E001', 'Audifono Bluetooth', 85000, 20, 12))
        inv.productos.append(ProductoElectronico('E002', 'Cable USB-C', 15000, 50, 6))
        inv.productos.append(ProductoRopa('R001', 'Camiseta Blanca', 25000, 30, 'M'))
        inv.productos.append(ProductoRopa('R002', 'Jean Azul', 75000, 15, 'L'))
        inv.guardar()

    while True:
        limpiar_pantalla()
        print("\n================================")
        print("  TIENDA EL BUEN PRECIO")
        print("  Sistema de Inventario")
        print("================================")
        print("1. ver todos los productos")
        print("2. buscar producto")
        print("3. agregar producto")
        print("4. actualizar stock")
        print("5. eliminar producto")
        print("6. ver reporte de valor")
        print("0. salir")
        print("================================")

        opcion = input("que desea hacer: ")

        if opcion == '1':
            inv.listar_todos()

        elif opcion == '2':
            codigo = input("ingrese el codigo: ")
            resultado = inv.buscar_por_codigo(codigo)
            if resultado != None:
                print("encontrado:", resultado)
            else:
                print("no se encontro ningun producto con ese codigo")

        elif opcion == '3':
            menu_agregar(inv)

        elif opcion == '4':
            codigo = input("codigo del producto: ")
            nueva = pedir_numero("nueva cantidad: ", int)
            inv.actualizar_stock(codigo, nueva)

        elif opcion == '5':
            codigo = input("codigo a eliminar: ")
            inv.eliminar_producto(codigo)

        elif opcion == '6':
            inv.generar_reporte()

        elif opcion == '0':
            print("hasta luego!")
            break

        else:
            print("esa opcion no existe")

        input("\npresione enter para continuar...")


# esto hace que el programa arranque desde aqui
if __name__ == '__main__':
    main()
