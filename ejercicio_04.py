"""Ejercicio 4 - Potencias y asociatividad: 2^3^2 = 2^(3^2) = 512 (derecha) y no (2^3)^2 = 64."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def a_postfija(expr, derecha=True):
    """derecha=True: '^' asocia por la derecha (convención matemática)."""
    tokens = re.findall(r"\d+\.?\d*|[-+*/^()]", expr)
    salida, ops = [], Pila()
    for t in tokens:
        if t in PREC:
            while (not ops.esta_vacia() and ops.peek() != "("
                   and (PREC[ops.peek()] > PREC[t]
                        or (PREC[ops.peek()] == PREC[t]
                            and not (t == "^" and derecha)))):
                salida.append(ops.pop())
            ops.push(t)
        elif t == "(":
            ops.push(t)
        elif t == ")":
            while ops.peek() != "(":
                salida.append(ops.pop())
            ops.pop()
        else:
            salida.append(t)
    while not ops.esta_vacia():
        salida.append(ops.pop())
    return salida


def evaluar(expr, derecha=True):
    pila = Pila()
    for t in a_postfija(expr, derecha):
        if t in PREC:
            b, a = pila.pop(), pila.pop()
            pila.push({"+": a + b, "-": a - b, "*": a * b,
                       "/": a / b if b else float("inf"), "^": a ** b}[t])
        else:
            pila.push(float(t))
    return pila.pop()


if __name__ == "__main__":
    print("EJERCICIO 4: potencias y asociatividad\n")
    print("  Comparación 2 ^ 3 ^ 2:")
    print(f"    asociatividad derecha  -> {' '.join(a_postfija('2 ^ 3 ^ 2'))}  = {evaluar('2 ^ 3 ^ 2'):g}")
    print(f"    asociatividad izquierda-> {' '.join(a_postfija('2 ^ 3 ^ 2', False))}  = {evaluar('2 ^ 3 ^ 2', False):g}\n")
    pruebas = [("2 ^ 3 ^ 2", 512), ("(2 ^ 3) ^ 2", 64), ("2 * 3 ^ 2", 18),
               ("2 ^ 2 * 3", 12), ("2 ^ (1 + 1) ^ 2", 16), ("9 ^ 0.5", 3)]
    for expr, esperado in pruebas:
        r = evaluar(expr)
        assert abs(r - esperado) < 1e-9
        print(f"  {expr:<20} = {r:g}  OK")
