import random as random
#Un Padre Varios Hijos

def func(x):
    return x**3-2*x**2+1

def ms(h):
    hijos = [0 for i in range(0,h)] #inicializados en 0
    valHijos = [0 for i in range(0, h)]
    padre = random.uniform(0,5)
    K=0
    it = int(input("Cantidad de iteraciones: "))
    while(K<it):
        for i in range(0,h):
            hijos[i]= padre + random.random()*(-1)**round(random.random())
            valHijos[i]=func(hijos[i])
        mejorHijo=min(valHijos)
        mejorHijo=hijos[valHijos.index(mejorHijo)]
        padre = mejorHijo
        K+=1
    return padre

for i in range(0,4):
    x = int(input("Cantidad de hijos: "))
    result = ms(x)
    print("Valor mínimo:",func(result),"en el punto: ",result)
