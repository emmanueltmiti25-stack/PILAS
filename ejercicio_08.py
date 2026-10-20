"""Ejercicio 8 - Evaluar una expresión infija con VARIABLES (a * (b + c) - d / e)."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def a_postfija(expr):
    tokens = re.findall(r"\d+\.?\d*|[A-Za-z_]\w*|[-+*/^()]", expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Carácter inválido en la expresión")
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


def evaluar(expr, variables):
    pila = Pila()
    for t in a_postfija(expr):
        if t in PREC:
            b, a = pila.pop(), pila.pop()
            if t == "/" and b == 0:
                raise ZeroDivisionError("División entre cero")
            pila.push({"+": a + b, "-": a - b, "*": a * b,
                       "/": a / b if b else 0, "^": a ** b}[t])
        elif t[0].isdigit():
            pila.push(float(t))
        elif t in variables:
            pila.push(float(variables[t]))
        else:
            raise ValueError(f"Variable no definida: {t}")
    return pila.pop()


if __name__ == "__main__":
    print("EJERCICIO 8: evaluación con variables\n")
    pruebas = [("a * (b + c) - d / e", dict(a=2, b=3, c=4, d=10, e=5), 12),
               ("x ^ 2 + y ^ 2", dict(x=3, y=4), 25),
               ("(base * altura) / 2", dict(base=10, altura=6), 30),
               ("p * (1 + r) ^ n", dict(p=1000, r=0.1, n=2), 1210)]
    for expr, vars_, esperado in pruebas:
        r = evaluar(expr, vars_)
        assert abs(r - esperado) < 1e-9
        print(f"  {expr:<22} con {vars_} = {r:g}  OK")
    try:
        evaluar("a + z", {"a": 1})
    except ValueError as e:
        print(f"  'a + z' con a=1 -> error controlado: {e}")
