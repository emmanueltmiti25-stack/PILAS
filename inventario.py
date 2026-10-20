"""
Caso práctico: Sistema de inventario de una papelería.
Estructuras: lista (registro de productos), pila (historial para deshacer),
cola (pedidos pendientes, FIFO).
Algoritmos: ordenamiento burbuja y merge sort; búsqueda lineal y binaria.
"""
import random
import time


# ------------------------------------------------------------ estructuras
class Nodo:
    def __init__(self, dato, siguiente=None):
        self.dato, self.siguiente = dato, siguiente


class Pila:
    """LIFO con lista enlazada. push/pop/peek: O(1)."""
    def __init__(self):
        self._tope, self._n = None, 0

    def push(self, dato):
        self._tope = Nodo(dato, self._tope)
        self._n += 1

    def pop(self):
        if self._tope is None:
            raise IndexError("Pila vacía")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        self._n -= 1
        return dato

    def peek(self):
        if self._tope is None:
            raise IndexError("Pila vacía")
        return self._tope.dato

    def esta_vacia(self):
        return self._tope is None

    def tamanio(self):
        return self._n


class Cola:
    """FIFO con lista enlazada (frente y final). enqueue/dequeue: O(1)."""
    def __init__(self):
        self._frente = self._final = None
        self._n = 0

    def enqueue(self, dato):
        nodo = Nodo(dato)
        if self._final is None:
            self._frente = self._final = nodo
        else:
            self._final.siguiente = nodo
            self._final = nodo
        self._n += 1

    def dequeue(self):
        if self._frente is None:
            raise IndexError("Cola vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._n -= 1
        return dato

    def frente(self):
        if self._frente is None:
            raise IndexError("Cola vacía")
        return self._frente.dato

    def esta_vacia(self):
        return self._frente is None

    def tamanio(self):
        return self._n


class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo, self.nombre, self.precio, self.stock = codigo, nombre, precio, stock

    def __repr__(self):
        return f"Producto({self.codigo}, {self.nombre!r}, ${self.precio}, stock={self.stock})"


# ------------------------------------------------------------ algoritmos
def ordenar_burbuja(lista, clave):
    """Burbuja con bandera de corte. Devuelve (lista ordenada, comparaciones). O(n^2)."""
    a, comps = list(lista), 0
    for i in range(len(a) - 1):
        hubo_cambio = False
        for j in range(len(a) - 1 - i):
            comps += 1
            if clave(a[j]) > clave(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return a, comps


def ordenar_merge(lista, clave):
    """Merge sort. Devuelve (lista ordenada, comparaciones). O(n log n)."""
    comps = [0]

    def ordenar(a):
        if len(a) <= 1:
            return a
        medio = len(a) // 2
        izq, der = ordenar(a[:medio]), ordenar(a[medio:])
        res, i, j = [], 0, 0
        while i < len(izq) and j < len(der):
            comps[0] += 1
            if clave(izq[i]) <= clave(der[j]):
                res.append(izq[i]); i += 1
            else:
                res.append(der[j]); j += 1
        return res + izq[i:] + der[j:]

    return ordenar(list(lista)), comps[0]


def busqueda_lineal(lista, codigo):
    """Devuelve (índice o -1, comparaciones). O(n)."""
    for i, p in enumerate(lista):
        if p.codigo == codigo:
            return i, i + 1
    return -1, len(lista)


def busqueda_binaria(lista, codigo):
    """Requiere lista ordenada por código. Devuelve (índice o -1, comparaciones). O(log n)."""
    bajo, alto, comps = 0, len(lista) - 1, 0
    while bajo <= alto:
        medio = (bajo + alto) // 2
        comps += 1
        if lista[medio].codigo == codigo:
            return medio, comps
        if lista[medio].codigo < codigo:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1, comps


# ------------------------------------------------------------ sistema
class Inventario:
    def __init__(self):
        self.productos = []
        self.historial = Pila()     # operaciones para deshacer
        self.pedidos = Cola()       # pedidos en espera

    def agregar(self, producto):
        if busqueda_lineal(self.productos, producto.codigo)[0] != -1:
            raise ValueError(f"Código duplicado: {producto.codigo}")
        self.productos.append(producto)
        self.historial.push(("agregar", producto.codigo))

    def eliminar(self, codigo):
        idx, _ = busqueda_lineal(self.productos, codigo)
        if idx == -1:
            raise KeyError(f"No existe el código {codigo}")
        producto = self.productos.pop(idx)
        self.historial.push(("eliminar", producto, idx))

    def registrar_pedido(self, codigo, cantidad):
        self.pedidos.enqueue((codigo, cantidad))

    def procesar_pedido(self):
        codigo, cantidad = self.pedidos.dequeue()
        idx, _ = busqueda_lineal(self.productos, codigo)
        if idx == -1:
            return f"Pedido rechazado: no existe el código {codigo}"
        producto = self.productos[idx]
        if producto.stock < cantidad:
            return f"Pedido rechazado: stock insuficiente de {producto.nombre} ({producto.stock})"
        producto.stock -= cantidad
        self.historial.push(("venta", codigo, cantidad))
        return f"Pedido surtido: {cantidad} x {producto.nombre}"

    def deshacer(self):
        op = self.historial.pop()
        if op[0] == "agregar":
            idx, _ = busqueda_lineal(self.productos, op[1])
            self.productos.pop(idx)
        elif op[0] == "eliminar":
            self.productos.insert(op[2], op[1])
        elif op[0] == "venta":
            idx, _ = busqueda_lineal(self.productos, op[1])
            self.productos[idx].stock += op[2]
        return op[0]


# ------------------------------------------------------------ pruebas
def pruebas_funcionales():
    inv = Inventario()
    inv.agregar(Producto(103, "Cuaderno", 45.0, 20))
    inv.agregar(Producto(101, "Lápiz", 6.5, 100))
    inv.agregar(Producto(102, "Goma", 8.0, 50))
    print("  [1] Alta de 3 productos:", len(inv.productos), "en inventario")
    assert len(inv.productos) == 3

    try:
        inv.agregar(Producto(101, "Duplicado", 1, 1))
        raise AssertionError
    except ValueError as e:
        print("  [2] Código duplicado rechazado:", e)

    inv.registrar_pedido(101, 30)
    inv.registrar_pedido(103, 50)
    inv.registrar_pedido(999, 1)
    resultados = [inv.procesar_pedido() for _ in range(3)]
    for r in resultados:
        print("  [3] FIFO:", r)
    assert resultados[0].startswith("Pedido surtido")
    assert "stock insuficiente" in resultados[1] and "no existe" in resultados[2]
    assert inv.productos[1].stock == 70 and inv.pedidos.esta_vacia()

    print("  [4] Deshacer (LIFO):", inv.deshacer(), "-> stock del lápiz:", inv.productos[1].stock)
    assert inv.productos[1].stock == 100
    inv.eliminar(102)
    print("  [5] Eliminar goma -> productos:", len(inv.productos), "| deshacer:", inv.deshacer(),
          "-> productos:", len(inv.productos))
    assert len(inv.productos) == 3

    por_codigo, _ = ordenar_merge(inv.productos, lambda p: p.codigo)
    assert [p.codigo for p in por_codigo] == [101, 102, 103]
    assert busqueda_binaria(por_codigo, 102)[0] == 1 and busqueda_binaria(por_codigo, 500)[0] == -1
    print("  [6] Orden por código:", [p.codigo for p in por_codigo], "| binaria(102) -> índice 1, binaria(500) -> -1")


def generar(n, semilla=42):
    rnd = random.Random(semilla)
    codigos = rnd.sample(range(1, n * 10), n)
    return [Producto(c, f"P{c}", round(rnd.uniform(1, 500), 2), rnd.randint(0, 200)) for c in codigos]


def tiempo_ms(f, *args):
    t = time.perf_counter()
    r = f(*args)
    return r, (time.perf_counter() - t) * 1000


def pruebas_ordenamiento():
    print(f"  {'n':>6} | {'Burbuja comp.':>14} {'ms':>9} | {'Merge comp.':>12} {'ms':>8}")
    for n in (500, 1000, 2000, 4000):
        datos = generar(n)
        (b, cb), tb = tiempo_ms(ordenar_burbuja, datos, lambda p: p.precio)
        (m, cm), tm = tiempo_ms(ordenar_merge, datos, lambda p: p.precio)
        assert [p.precio for p in b] == [p.precio for p in m] == sorted(p.precio for p in datos)
        print(f"  {n:>6} | {cb:>14,} {tb:>9.1f} | {cm:>12,} {tm:>8.1f}")


def pruebas_busqueda():
    print(f"  {'n':>8} | {'Lineal (prom. comp.)':>21} | {'Binaria (prom. comp.)':>22}")
    for n in (1000, 10000, 100000):
        datos, _ = ordenar_merge(generar(n), lambda p: p.codigo)
        rnd = random.Random(7)
        consultas = [rnd.choice(datos).codigo for _ in range(500)]
        tl = sum(busqueda_lineal(datos, c)[1] for c in consultas) / 500
        tb = 0
        for c in consultas:
            i, k = busqueda_binaria(datos, c)
            assert i != -1 and datos[i].codigo == c
            tb += k
        print(f"  {n:>8,} | {tl:>21,.1f} | {tb / 500:>22.1f}")


if __name__ == "__main__":
    print("PRUEBAS FUNCIONALES")
    pruebas_funcionales()
    print("\nORDENAMIENTO (clave: precio; mismos datos en ambos algoritmos)")
    pruebas_ordenamiento()
    print("\nBÚSQUEDA (500 consultas de productos existentes)")
    pruebas_busqueda()
    print("\nTodas las pruebas pasaron.")
