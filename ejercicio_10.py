"""Ejercicio 10 - Evaluador completo con TRAZA paso a paso de la pila y manejo de errores."""
import re
from pila import Pila

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def tokenizar(expr):
    tokens = re.findall(r"\d+\.?\d*|[-+*/^()]", expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Carácter inválido en la expresión")
    return tokens


def a_postfija(tokens, traza=False):
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
        if traza:
            print(f"    {t:<5}| pila: {' '.join(ops.a_lista()):<10}| salida: {' '.join(salida)}")
    while not ops.esta_vacia():
        op = ops.pop()
        if op == "(":
            raise ValueError("Paréntesis desbalanceados: falta ')'")
        salida.append(op)
    if traza:
        print(f"    fin  | pila: {'':<10}| salida: {' '.join(salida)}")
    return salida


def evaluar_postfija(post, traza=False):
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
        if traza:
            print(f"    {t:<5}| pila: {[f'{x:g}' for x in pila.a_lista()]}")
    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.pop()


def evaluar(expr, traza=False):
    if traza:
        print("  Fase 1: infija -> postfija")
    post = a_postfija(tokenizar(expr), traza)
    if traza:
        print(f"  Fase 2: evaluación de [{' '.join(post)}]")
    return evaluar_postfija(post, traza)


if __name__ == "__main__":
    print("EJERCICIO 10: evaluador completo con traza y errores\n")
    expr = "((2 + 3) * (4 - 1)) ^ 2 / 5"
    print(f"  Expresión: {expr}")
    r = evaluar(expr, traza=True)
    assert r == 45
    print(f"  Resultado: {r:g}\n")
    print("  Manejo de errores:")
    for mala in ["(3 + 4", "3 + 4)", "5 / (2 - 2)", "3 + * 4", "3 $ 4", "3 4"]:
        try:
            evaluar(mala)
            raise AssertionError("debió fallar")
        except (ValueError, ZeroDivisionError, IndexError) as e:
            print(f"    {mala!r:<14} -> {type(e).__name__}: {e}")
