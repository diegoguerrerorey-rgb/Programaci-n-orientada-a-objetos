# ============================================================
#  SISTEMA DE INVENTARIO - TIENDA EL BUEN PRECIO
#  Trabajo Final POO 2 - CUN
#  Tecnologia: Python 3
# ============================================================

import csv
import os
from abc import ABC, abstractmethod   # Para Clases Abstractas e Interfaces

# ============================================================
# INTERFACES (simuladas con ABC en Python)
# ============================================================

class Persistible(ABC):
    """Interfaz que obliga a guardar y cargar datos."""
    @abstractmethod
    def guardar(self):
        pass

    @abstractmethod
    def cargar(self):
        pass


class Reportable(ABC):
    """Interfaz que obliga a generar reportes."""
    @abstractmethod
    def generar_reporte(self):
        pass


# ============================================================
# CLASE ABSTRACTA BASE
# ============================================================

class Producto(ABC):
    """Clase abstracta que representa un producto generico."""

    def __init__(self, codigo, nombre, precio, cantidad):
        self.__codigo   = codigo       # Encapsulamiento (privado)
        self.__nombre   = nombre
        self.__precio   = float(precio)
        self.__cantidad = int(cantidad)

    # --- Getters ---
    def get_codigo(self):   return self.__codigo
    def get_nombre(self):   return self.__nombre
    def get_precio(self):   return self.__precio
    def get_cantidad(self): return self.__cantidad

    # --- Setters ---
    def set_precio(self, precio):     self.__precio   = float(precio)
    def set_cantidad(self, cantidad): self.__cantidad = int(cantidad)
    def set_nombre(self, nombre):     self.__nombre   = nombre

    @abstractmethod
    def tipo(self):
        """Cada subclase debe indicar su tipo."""
        pass

    def __str__(self):
        return (f"[{self.tipo()}] Cod:{self.__codigo} | {self.__nombre} "
                f"| ${self.__precio:,.0f} | Stock:{self.__cantidad}")


# ============================================================
# SUBCLASES (Herencia + Polimorfismo)
# ============================================================

class ProductoAlimenticio(Producto):
    """Hereda de Producto. Agrega fecha de vencimiento."""

    def __init__(self, codigo, nombre, precio, cantidad, fecha_venc):
        super().__init__(codigo, nombre, precio, cantidad)
        self.fecha_venc = fecha_venc

    def tipo(self):   # Override del metodo abstracto (equivalente a @Override en Java)
        return "ALIMENTO"

    def __str__(self):
        return super().__str__() + f" | Vence:{self.fecha_venc}"


class ProductoElectronico(Producto):
    """Hereda de Producto. Agrega garantia en meses."""

    def __init__(self, codigo, nombre, precio, cantidad, garantia_meses):
        super().__init__(codigo, nombre, precio, cantidad)
        self.garantia_meses = int(garantia_meses)

    def tipo(self):   # Override del metodo abstracto
        return "ELECTRONICO"

    def __str__(self):
        return super().__str__() + f" | Garantia:{self.garantia_meses} meses"


class ProductoRopa(Producto):
    """Hereda de Producto. Agrega talla."""

    def __init__(self, codigo, nombre, precio, cantidad, talla):
        super().__init__(codigo, nombre, precio, cantidad)
        self.talla = talla

    def tipo(self):   # Override del metodo abstracto
        return "ROPA"

    def __str__(self):
        return super().__str__() + f" | Talla:{self.talla}"


# ============================================================
# CLASE INVENTARIO - Implementa las interfaces
# ============================================================

class Inventario(Persistible, Reportable):
    """Gestiona la coleccion de productos. Usa ArrayList (lista de Python)."""

    ARCHIVO_CSV = os.path.join(os.path.dirname(__file__), '..', 'datos', 'inventario.csv')

    def __init__(self):
        self.productos = []   # Coleccion dinamica (equivalente a ArrayList)
        self.cargar()         # Al iniciar, carga datos guardados

    # ---------- PERSISTENCIA ----------

    def guardar(self):
        """Guarda todos los productos en un archivo CSV."""
        try:
            os.makedirs(os.path.dirname(self.ARCHIVO_CSV), exist_ok=True)
            with open(self.ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['tipo', 'codigo', 'nombre', 'precio', 'cantidad', 'extra'])
                for p in self.productos:
                    if isinstance(p, ProductoAlimenticio):
                        writer.writerow(['ALIMENTO', p.get_codigo(), p.get_nombre(),
                                         p.get_precio(), p.get_cantidad(), p.fecha_venc])
                    elif isinstance(p, ProductoElectronico):
                        writer.writerow(['ELECTRONICO', p.get_codigo(), p.get_nombre(),
                                         p.get_precio(), p.get_cantidad(), p.garantia_meses])
                    elif isinstance(p, ProductoRopa):
                        writer.writerow(['ROPA', p.get_codigo(), p.get_nombre(),
                                         p.get_precio(), p.get_cantidad(), p.talla])
            print("  ✅ Datos guardados correctamente.")
        except Exception as e:
            print(f"  ❌ Error al guardar: {e}")

    def cargar(self):
        """Carga productos desde el archivo CSV al iniciar."""
        try:
            if not os.path.exists(self.ARCHIVO_CSV):
                return
            with open(self.ARCHIVO_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tipo = row['tipo']
                    if tipo == 'ALIMENTO':
                        self.productos.append(ProductoAlimenticio(
                            row['codigo'], row['nombre'], row['precio'],
                            row['cantidad'], row['extra']))
                    elif tipo == 'ELECTRONICO':
                        self.productos.append(ProductoElectronico(
                            row['codigo'], row['nombre'], row['precio'],
                            row['cantidad'], row['extra']))
                    elif tipo == 'ROPA':
                        self.productos.append(ProductoRopa(
                            row['codigo'], row['nombre'], row['precio'],
                            row['cantidad'], row['extra']))
        except Exception as e:
            print(f"  ⚠️  No se pudieron cargar datos previos: {e}")

    # ---------- CRUD ----------

    def agregar_producto(self, producto):
        """Agrega un nuevo producto al inventario."""
        try:
            # Verificar que el codigo no exista ya
            if self.buscar_por_codigo(producto.get_codigo()):
                print(f"  ⚠️  Ya existe un producto con codigo {producto.get_codigo()}.")
                return False
            self.productos.append(producto)
            self.guardar()
            print(f"  ✅ Producto '{producto.get_nombre()}' agregado.")
            return True
        except Exception as e:
            print(f"  ❌ Error al agregar: {e}")
            return False

    def buscar_por_codigo(self, codigo):
        """Busca un producto por su codigo. Retorna el producto o None."""
        for p in self.productos:
            if p.get_codigo() == codigo:
                return p
        return None

    def eliminar_producto(self, codigo):
        """Elimina un producto del inventario."""
        try:
            producto = self.buscar_por_codigo(codigo)
            if producto:
                self.productos.remove(producto)
                self.guardar()
                print(f"  ✅ Producto '{producto.get_nombre()}' eliminado.")
            else:
                print(f"  ⚠️  No existe producto con codigo {codigo}.")
        except Exception as e:
            print(f"  ❌ Error al eliminar: {e}")

    def actualizar_stock(self, codigo, nueva_cantidad):
        """Actualiza la cantidad en stock de un producto."""
        try:
            producto = self.buscar_por_codigo(codigo)
            if producto:
                producto.set_cantidad(int(nueva_cantidad))
                self.guardar()
                print(f"  ✅ Stock de '{producto.get_nombre()}' actualizado a {nueva_cantidad}.")
            else:
                print(f"  ⚠️  No existe producto con codigo {codigo}.")
        except ValueError:
            print("  ❌ La cantidad debe ser un numero entero.")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    def listar_todos(self):
        """Muestra todos los productos del inventario."""
        if not self.productos:
            print("  📭 El inventario esta vacio.")
        else:
            print(f"\n  {'='*65}")
            print(f"  {'INVENTARIO COMPLETO':^65}")
            print(f"  {'='*65}")
            for p in self.productos:
                print(f"  {p}")
            print(f"  {'='*65}")
            print(f"  Total de productos: {len(self.productos)}")

    # ---------- REPORTE ----------

    def generar_reporte(self):
        """Genera un reporte de valor total del inventario."""
        total = 0
        print(f"\n  {'='*65}")
        print(f"  {'REPORTE DE INVENTARIO - TIENDA EL BUEN PRECIO':^65}")
        print(f"  {'='*65}")
        print(f"  {'TIPO':<15} {'NOMBRE':<20} {'PRECIO':>10} {'CANT':>6} {'SUBTOTAL':>12}")
        print(f"  {'-'*65}")
        for p in self.productos:
            sub = p.get_precio() * p.get_cantidad()
            total += sub
            print(f"  {p.tipo():<15} {p.get_nombre():<20} ${p.get_precio():>9,.0f} {p.get_cantidad():>6} ${sub:>11,.0f}")
        print(f"  {'='*65}")
        print(f"  {'VALOR TOTAL DEL INVENTARIO:':>50} ${total:>11,.0f}")
        print(f"  {'='*65}\n")


# ============================================================
# MENU PRINCIPAL
# ============================================================

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pedir_numero(mensaje, tipo=float):
    """Pide un numero al usuario con manejo de excepciones."""
    while True:
        try:
            return tipo(input(mensaje))
        except ValueError:
            print("  ❌ Por favor ingrese un numero valido.")

def menu_agregar(inv):
    print("\n  ¿Que tipo de producto desea agregar?")
    print("  1. Alimento")
    print("  2. Electronico")
    print("  3. Ropa")
    op = input("  Opcion: ").strip()

    try:
        codigo   = input("  Codigo unico: ").strip()
        nombre   = input("  Nombre: ").strip()
        precio   = pedir_numero("  Precio: $", float)
        cantidad = pedir_numero("  Cantidad en stock: ", int)

        if op == '1':
            venc = input("  Fecha de vencimiento (ej: 2025-12): ").strip()
            prod = ProductoAlimenticio(codigo, nombre, precio, cantidad, venc)
        elif op == '2':
            gar = pedir_numero("  Meses de garantia: ", int)
            prod = ProductoElectronico(codigo, nombre, precio, cantidad, gar)
        elif op == '3':
            talla = input("  Talla (XS/S/M/L/XL): ").strip().upper()
            prod = ProductoRopa(codigo, nombre, precio, cantidad, talla)
        else:
            print("  ❌ Opcion no valida.")
            return

        inv.agregar_producto(prod)

    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")

def main():
    inv = Inventario()

    # Cargar datos de ejemplo si el inventario esta vacio
    if not inv.productos:
        inv.productos.append(ProductoAlimenticio('A001', 'Arroz Diana 1kg', 4500, 100, '2026-06'))
        inv.productos.append(ProductoAlimenticio('A002', 'Leche Alpina 1L', 3200, 60,  '2025-09'))
        inv.productos.append(ProductoElectronico('E001', 'Audifono Bluetooth', 85000, 20, 12))
        inv.productos.append(ProductoElectronico('E002', 'Cable USB-C',        15000, 50,  6))
        inv.productos.append(ProductoRopa('R001', 'Camiseta Blanca', 25000, 30, 'M'))
        inv.productos.append(ProductoRopa('R002', 'Jean Azul',       75000, 15, 'L'))
        inv.guardar()

    while True:
        limpiar()
        print("\n" + "="*55)
        print("    🏪  TIENDA EL BUEN PRECIO - Sistema de Inventario")
        print("="*55)
        print("  1. Ver todos los productos")
        print("  2. Buscar producto por codigo")
        print("  3. Agregar nuevo producto")
        print("  4. Actualizar stock")
        print("  5. Eliminar producto")
        print("  6. Generar reporte de valor")
        print("  0. Salir")
        print("="*55)

        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == '1':
            inv.listar_todos()

        elif opcion == '2':
            cod = input("  Ingrese el codigo a buscar: ").strip()
            p = inv.buscar_por_codigo(cod)
            if p:
                print(f"\n  ✅ Encontrado: {p}")
            else:
                print("  ⚠️  Producto no encontrado.")

        elif opcion == '3':
            menu_agregar(inv)

        elif opcion == '4':
            cod = input("  Codigo del producto: ").strip()
            cant = pedir_numero("  Nueva cantidad: ", int)
            inv.actualizar_stock(cod, cant)

        elif opcion == '5':
            cod = input("  Codigo del producto a eliminar: ").strip()
            inv.eliminar_producto(cod)

        elif opcion == '6':
            inv.generar_reporte()

        elif opcion == '0':
            print("\n  👋 Hasta luego!\n")
            break
        else:
            print("  ❌ Opcion no valida.")

        input("\n  Presione ENTER para continuar...")


# Punto de entrada del programa
if __name__ == '__main__':
    main()
