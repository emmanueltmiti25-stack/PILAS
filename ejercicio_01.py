"""Ejercicio 1 - Evaluar una expresión POSTFIJA (notación polaca inversa)."""
from pila import Pila


def aplicar(op, a, b):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("División entre cero")
        return a / b
    if op == "^": return a ** b
    raise ValueError(f"Operador desconocido: {op}")


def evaluar_postfija(expr):
    pila = Pila()
    for t in expr.split():
        if t in ("+", "-", "*", "/", "^"):
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            b = pila.pop()
            a = pila.pop()
            pila.push(aplicar(t, a, b))
        else:
            pila.push(float(t))
    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.pop()


if __name__ == "__main__":
    print("EJERCICIO 1: evaluación de expresiones postfijas\n")
    pruebas = [("3 4 2 * +", 11), ("3 4 + 2 *", 14), ("5 1 2 + 4 * + 3 -", 14),
               ("10 2 / 3 -", 2), ("2 3 2 ^ ^", 512)]
    for expr, esperado in pruebas:
        r = evaluar_postfija(expr)
        assert abs(r - esperado) < 1e-9
        print(f"  {expr:<22} = {r:g}   (esperado {esperado})  OK")
