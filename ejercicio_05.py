"""Ejercicio 5 - Validar que los delimitadores ( ) [ ] { } de una expresión estén balanceados."""
from pila import Pila

PARES = {")": "(", "]": "[", "}": "{"}


def balanceada(texto):
    pila = Pila()
    for i, c in enumerate(texto):
        if c in "([{":
            pila.push((c, i))
        elif c in PARES:
            if pila.esta_vacia():
                return False, f"'{c}' sin apertura (posición {i})"
            apertura, pos = pila.pop()
            if apertura != PARES[c]:
                return False, f"'{apertura}' (pos {pos}) no coincide con '{c}' (pos {i})"
    if not pila.esta_vacia():
        c, pos = pila.peek()
        return False, f"'{c}' sin cierre (posición {pos})"
    return True, "balanceada"


if __name__ == "__main__":
    print("EJERCICIO 5: balanceo de paréntesis, corchetes y llaves\n")
    pruebas = [("{[()]}", True), ("a * (b + [c - d])", True), ("", True),
               ("([)]", False), ("((", False), ("}{", False), ("3 + 4)", False)]
    for expr, esperado in pruebas:
        ok, msg = balanceada(expr)
        assert ok == esperado
        print(f"  {expr!r:<22} -> {msg}")
