"""Ejercicio 7 - Convertir una expresión INFIJA a PREFIJA (invertir, convertir, invertir)."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def infija_a_prefija(expr):
    tokens = re.findall(r"\d+\.?\d*|[A-Za-z_]\w*|[-+*/^()]", expr)[::-1]
    tokens = [")" if t == "(" else "(" if t == ")" else t for t in tokens]
    salida, ops = [], Pila()
    for t in tokens:
        if t in PREC:
            # al trabajar invertido, la regla de asociatividad se invierte
            while (not ops.esta_vacia() and ops.peek() != "("
                   and (PREC[ops.peek()] > PREC[t]
                        or (PREC[ops.peek()] == PREC[t] and t == "^"))):
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
    return " ".join(salida[::-1])


if __name__ == "__main__":
    print("EJERCICIO 7: conversión infija -> prefija\n")
    pruebas = [("A + B * C", "+ A * B C"), ("(A + B) * C", "* + A B C"),
               ("A - B - C", "- - A B C"), ("A ^ B ^ C", "^ A ^ B C"),
               ("A * (B + C) / D", "/ * A + B C D")]
    for infija, esperado in pruebas:
        r = infija_a_prefija(infija)
        assert r == esperado
        print(f"  {infija:<20} -> {r:<16} OK")
