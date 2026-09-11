import itertools

# 1. Definimos las variables proposicionales
# 'repeat' indica cuántas variables tenemos (en este caso 2: P y Q)
variables = ["P", "Q"]
combinaciones = list(itertools.product([True, False], repeat=len(variables)))

# 2. Imprimimos la cabecera de la tabla
print(f"{'P':<6} | {'Q':<6} | {'P ∧ Q':<8} | {'P → Q':<8}")
print("-" * 36)

# 3. Evaluamos cada combinación de valores
for p, q in combinaciones:
  # Operadores lógicos en Python:
  # Conjunción (AND): and
  # Disyunción (OR): or
  # Negación (NOT): not
  # Implicación (P -> Q equivale a: not P or Q)

  conjuancion = p and q
  implicacion = (not p) or q

  # Formateamos la salida para que se vea alineada
  print(f"{str(p):<6} | {str(q):<6} | {str(conjuancion):<8} | {str(implicacion):<8}")