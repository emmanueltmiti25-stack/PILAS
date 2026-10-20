"""Ejercicio 3 - Evaluar una expresión INFIJA con paréntesis (infija -> postfija -> resultado)."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def tokenizar(expr):
    tokens = re.findall(r"\d+\.?\d*|[-+*/^()]", expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Carácter inválido en la expresión")
    return tokens


def infija_a_postfija(tokens):
    salida, ops = [], Pila()
    for t in tokens:
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
    return salida


def evaluar_postfija(post):
    pila = Pila()
    for t in post:
        if t in PREC:
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            b, a = pila.pop(), pila.pop()
            if t == "/" and b == 0:
                raise ZeroDivisionError("División entre cero")
            pila.push({"+": a + b, "-": a - b, "*": a * b,
                       "/": a / b if b else 0, "^": a ** b}[t])
        else:
            pila.push(float(t))
    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.pop()


def evaluar(expr):
    return evaluar_postfija(infija_a_postfija(tokenizar(expr)))


if __name__ == "__main__":
    print("EJERCICIO 3: evaluación de expresiones infijas con paréntesis\n")
    pruebas = [("(8 - 3) * (2 + 6) / 4", 10),
               ("15 / (7 - (1 + 1)) * 3 - (2 + (1 + 1))", 5),
               ("100 - 20 * (3 + 2) / 5", 80),
               ("((2 + 3) * (4 - 1)) ^ 2 / 5", 45),
               ("(((7)))", 7)]
    for expr, esperado in pruebas:
        r = evaluar(expr)
        assert abs(r - esperado) < 1e-9
        print(f"  {expr:<42} = {r:g}  OK")
