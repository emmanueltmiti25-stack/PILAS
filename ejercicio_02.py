"""Ejercicio 2 - Convertir una expresión INFIJA a POSTFIJA (Shunting-Yard)."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def tokenizar(expr):
    tokens = re.findall(r"\d+\.?\d*|[A-Za-z_]\w*|[-+*/^()]", expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Carácter inválido en la expresión")
    return tokens


def infija_a_postfija(expr):
    salida, ops = [], Pila()
    for t in tokenizar(expr):
        if t in PREC:
            while (not ops.esta_vacia() and ops.peek() != "("
                   and (PREC[ops.peek()] > PREC[t]
                        or (PREC[ops.peek()] == PREC[t] and t != "^"))):
                salida.append(ops.pop())
            ops.push(t)
        elif t == "(":
            ops.push(t)
        elif t == ")":
            while not ops.esta_vacia() and ops.peek() != "(":
                salida.append(ops.pop())
            if ops.esta_vacia():
                raise ValueError("Paréntesis desbalanceados: falta '('")
            ops.pop()
        else:
            salida.append(t)
    while not ops.esta_vacia():
        op = ops.pop()
        if op == "(":
            raise ValueError("Paréntesis desbalanceados: falta ')'")
        salida.append(op)
    return " ".join(salida)


if __name__ == "__main__":
    print("EJERCICIO 2: conversión infija -> postfija\n")
    pruebas = [("A + B * C", "A B C * +"), ("( A + B ) * ( C - D )", "A B + C D - *"),
               ("A ^ B ^ C", "A B C ^ ^"), ("A - B - C", "A B - C -"),
               ("10 / 2 - 3", "10 2 / 3 -"), ("A * ( B + C ) / D", "A B C + * D /")]
    for infija, esperado in pruebas:
        r = infija_a_postfija(infija)
        assert r == esperado
        print(f"  {infija:<24} -> {r:<18} OK")
