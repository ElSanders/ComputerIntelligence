import numpy as np
import math
import sys
import matplotlib.pyplot as plt

cantParticulas = 100
#Valores correctos
correct = [-3.271085446759225, 2.9946329498568343, 14.999975823810116, 34.999999890807594, 62.99999999950683,
               98.99999999999777, 143, 195, 255, 323]
#Calcular el error
def error(vals):
    er = 0
    global correct
    for i in range(0,10):
        #Porcentaje de error promedio
        er += (abs((vals[i]-correct[i])/correct[i]))
    return er*10 #100/10

def func(coef):
    #Evalúa la función usando los coeficientes ingresados
    res = []
    for x in range(0,10):
        try:
            a = coef[0]*x**2-coef[1]**((math.exp(-coef[2]*x))/2)
            if(str(a) != "NaN"):
                res.append(a)
            else:
                #Si es NaN o tiene Overflow, se agrega un valor numérico 10 veces menor al máximo de un float
                #Para evitar errores de evaluación (es cerca de infinito, entonces no pasan de todos modos)
                #Pero así no rompe el ciclo.
                res.append(sys.float_info.max / 10)
        except OverflowError:
            res.append(sys.float_info.max/10)
    return res

#Algoritmo
particulas = []
mejores = []
velocidades = [np.random.random(3) for i in range(cantParticulas)]
for i in range(cantParticulas):
    particulas.append(np.random.uniform(0,10,3))
er = []
for i in range(cantParticulas):
    er.append(error(func(particulas[i])))
globalBest = particulas[er.index(min(er))]
alpha = 2
beta = 2
localBests = particulas.copy()
#20 iteraciones
for iterations in range(20):
    #Se agrega el mejor valor actual
    mejores.append([iterations,error(func(globalBest))])
    e1 = np.random.random(3)
    e2 = np.random.random(3)
    for i in range(cantParticulas):
        #Calcular velocidad
        velocidades[i]=velocidades[i]+alpha*e1*(globalBest-particulas[i])+beta*e2*(localBests[i]-particulas[i])
        #Actualizar posición
        particulas[i] = particulas[i]+velocidades[i]
        #Evaluar y encontrar mejor local
        if(error(func(particulas[i]))<(error(func(localBests[i])))):
            localBests[i]=particulas[i]
    # Encontrar el mejor global
    for i in range(len(localBests)):
        if (error(func(localBests[i])) < error(func(globalBest))):
            globalBest = localBests[i]
#Imprimir resultados
print("Mejor solución: a1=",globalBest[0],"a2= ",globalBest[1],"a3= ",globalBest[2])
print("Valores obtenidos:","                 ", "Valores esperados:")
for i in range(len(correct)):
    print(func(globalBest)[i],"                 ",correct[i])
#Graficar curva de mejor resultado 
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
for i,j in zip(mejores[:-1],mejores[1:]):
    ax.plot([i[0], j[0]], [i[1], j[1]], 'g')
plt.show()