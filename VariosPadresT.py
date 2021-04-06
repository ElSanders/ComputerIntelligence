import random as random
#Varios Padres Varios Hijos Con Traslape

def func(x):
    return x**3-2*x**2+1

def ms(h,p):
    hijos = [0 for i in range(0,h)] #inicializados en 0
    valHijos = [0 for i in range(0, h)]  # inicializados en 0
    padres =  [random.uniform(0,5) for i in range(0,p)]
    valPadres = [func(padres[i]) for i in range(0, p)]
    K=0
    it = int(input("Cantidad de iteraciones: "))
    while(K<it):
        for i in range(0,p):
            for j in range(0,h):
                hijos[j]= padres[i] + random.random()*(-1)**round(random.random())
                valHijos[j]=func(hijos[j])

            mejorHijo=min(valHijos+valPadres)
            if(mejorHijo in valHijos):
                mejorHijo = hijos[valHijos.index(mejorHijo)]
            else:
                mejorHijo = padres[valPadres.index(mejorHijo)]
            padres[i] = mejorHijo
            valPadres[i]=func(padres[i])
        K+=1
    padreMejor = min(valPadres)
    return padres[valPadres.index(padreMejor)]

for i in range(0,4):
    x = int(input("Cantidad de hijos: "))
    y = int(input("Cantidad de padres: "))
    result = ms(x,y)
    print("Valor mínimo:",func(result),"en el punto: ",result)
