"""Ejercicio 6 - Evaluar una expresión PREFIJA (notación polaca): se recorre de derecha a izquierda."""
from pila import Pila

OPS = ("+", "-", "*", "/", "^")


def evaluar_prefija(expr):
    pila = Pila()
    for t in reversed(expr.split()):
        if t in OPS:
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            a = pila.pop()          # primer operando (izquierdo)
            b = pila.pop()          # segundo operando (derecho)
            if t == "/" and b == 0:
                raise ZeroDivisionError("División entre cero")
            pila.push({"+": a + b, "-": a - b, "*": a * b,
                       "/": a / b if b else 0, "^": a ** b}[t])
        else:
            pila.push(float(t))
    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.pop()


if __name__ == "__main__":
    print("EJERCICIO 6: evaluación de expresiones prefijas\n")
    pruebas = [("+ 3 * 4 2", 11), ("* + 3 4 2", 14), ("- / 10 2 3", 2),
               ("^ 2 ^ 3 2", 512), ("/ * 20 + 3 2 5", 20)]
    for expr, esperado in pruebas:
        r = evaluar_prefija(expr)
        assert abs(r - esperado) < 1e-9
        print(f"  {expr:<18} = {r:g}  (esperado {esperado})  OK")
