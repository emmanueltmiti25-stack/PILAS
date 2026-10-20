"""Ejercicio 9 - Operador unario negativo: -3 + 2 * -(4 - 1)."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "~": 3, "^": 4}   # '~' = menos unario
DERECHA = {"^", "~"}
BINARIOS = {"+", "-", "*", "/", "^"}


def marcar_unarios(tokens):
    res, prev = [], None
    for t in tokens:
        es_unario = t == "-" and (prev is None or prev in BINARIOS or prev == "(")
        res.append("~" if es_unario else t)
        prev = t
    return res


def a_postfija(expr):
    tokens = re.findall(r"\d+\.?\d*|[-+*/^()]", expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Carácter inválido en la expresión")
    salida, ops = [], Pila()
    for t in marcar_unarios(tokens):
        if t == "~":
            ops.push(t)                      # prefijo: no desapila nada
        elif t in PREC:
            while (not ops.esta_vacia() and ops.peek() != "("
                   and (PREC[ops.peek()] > PREC[t]
                        or (PREC[ops.peek()] == PREC[t] and t not in DERECHA))):
                salida.append(ops.pop())
            ops.push(t)
        elif t == "(":
            ops.push(t)
        elif t == ")":
            while not ops.esta_vacia() and ops.peek() != "(":
                salida.append(ops.pop())
            if ops.esta_vacia():
                raise ValueError("Paréntesis desbalanceados")
            ops.pop()
        else:
            salida.append(t)
    while not ops.esta_vacia():
        op = ops.pop()
        if op == "(":
            raise ValueError("Paréntesis desbalanceados")
        salida.append(op)
    return salida


def evaluar(expr):
    pila = Pila()
    for t in a_postfija(expr):
        if t == "~":
            pila.push(-pila.pop())
        elif t in BINARIOS:
            b, a = pila.pop(), pila.pop()
            pila.push({"+": a + b, "-": a - b, "*": a * b,
                       "/": a / b, "^": a ** b}[t])
        else:
            pila.push(float(t))
    return pila.pop()


if __name__ == "__main__":
    print("EJERCICIO 9: operador unario negativo\n")
    pruebas = [("-3 + 2", -1), ("-3 + 2 * -(4 - 1)", -9), ("2 ^ -1", 0.5),
               ("-2 ^ 2", -4), ("3 - -2", 5), ("-(-5)", 5)]
    for expr, esperado in pruebas:
        r = evaluar(expr)
        assert abs(r - esperado) < 1e-9
        print(f"  {expr:<20} postfija: {' '.join(a_postfija(expr)):<20} = {r:g}  OK")
