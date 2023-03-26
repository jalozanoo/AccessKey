# Extension to give a requested password. 
# def print_sorted_list used from 
# https://www.3engine.net/wp/2019/03/como-imprimir-una-lista-de-forma-mas-agradable-en-python-por-linea-de-comandos/
# Modified by: Jhonatan Lozano
import os
from parse import *

def print_sorted_list(data, columns, gap=2):
    if data:
        gap = 4
        ljusts = {}
        for count, item in enumerate(sorted(data), 1):
            column = count % columns
            ljusts[column] = len(item) if (column not in ljusts) else max(ljusts[column], len(item))
        for count, item in enumerate(sorted(data), 1):
            print ("\n" if (count % columns == 0) or (count == len(data)) else "" , end=item.ljust(ljusts[count % columns] + gap) )

def give(D):
  os.system("cls")
  D_keys = D.keys()
  print("Tiene accesos de estas instancias: \n")
  print_sorted_list(list(D_keys), columns=4)
  
  while 1:
    key = input("\nSeleccione una de las anteriores opciones => ")
    if key in D:
      if "/" in str(D[key]):
        user_key = parse("{user}/{key}",D[key])
        print("\n El acceso a "+key+" es -> Usuario: "+user_key['user']+" Contraseña: "+user_key['key']+'\n')
      else:  
        print("\n La contraseña del acceso a "+key+" es: "+str(D[key])+'\n')
      break
    else:
      print("Seleccione una opción válida.\n")
