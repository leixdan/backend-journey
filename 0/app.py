#def top_palabras(texto):
    # normalización de texto a minúsculas eliminando signos que no sean texto
    # Declaración de los dict cuenta_hola y cuenta_mundo en 0
    # Declaración del contador en 0
    # Ciclo que lee 'texto' hasta un espacio en una variable local 'palabra'
    # Condicional que compara 'palabra' con alguna de la lista
    # Condicional que si es == a alguna de la lista suma el contador respectivo
    # Return: lista de tuplas ('hola',n) y ()'mundo',n).

#top_palabras("Hola mundo. Hola, MUNDO! Hola Python")
# [('hola', 3), ('mundo', 2)]

frase = 'Tren al sur'
print(frase)
frase = frase.split()
print(type(frase))
palabra = 'al'
count = 0
for p in frase:
    if p == palabra:
        print(f"La encontré, es '{p}'")
        count += 1

print(count)