import sys

print('Ingrese argumentos:')

nombre = input()
nombre = nombre.split(' ')
nombre = [i.title().replace('_', ' ') for i in nombre]
print(nombre)

