import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from functools import partial
import math


cities = 5
iteraciones = 10
hormigas = 5
alpha = 1
beta = 1

coordenadas = np.random.randint(1,20,size = (cities,2))
dm = distance_matrix(coordenadas,coordenadas)

tau = np.ones((cities,cities))

eta = np.asarray([1/dm[i,j] for i in range(cities) for j in range(cities)]).reshape(cities,cities)

eta = np.where(eta==np.inf,0,eta)

def distancia(solucion,dm):
    conexion = zip(solucion,solucion[1:]+[solucion[0]])
    L = 0
    for i,j in conexion:
        L+=dm[i,j]
    return L

def correrHormiga(actual,cities,alpha,beta,tau,eta):
    permitidos = list(range(cities))
    permitidos.remove(actual)
    ruta = [actual]
    while permitidos:
        p = np.zeros(cities)
        sumaP = 0
        for j in permitidos:
            a = min(actual,j)
            b = max(actual,j)
            p[j] = np.power(tau[actual,j],alpha) * np.power(eta[actual,j],beta)
            sumaP += p[j]
        p = p/sumaP

        r = np.random.rand()
        suma = 0
        for ciu in permitidos:


            prob = p[ciu]
            suma += prob
            if(r<=prob):
                actual=ciu
                ruta.append(actual)
                permitidos.remove(actual)
                break
    return ruta

def actualizarFeromonas(soluciones,evaluaciones,tau,Q,ro):
    tau = ro * tau
    for idx, solucion in enumerate(soluciones):
        conexiones = zip(solucion,solucion[1:]+[solucion[0]])
        for i,j in conexiones:
            minimo = min(i,j)
            maximo = max(i,j)
            tau[minimo,maximo] = tau[minimo,maximo]+Q/evaluaciones[idx]
    return tau



def evaluarTodo(solucion,matriz_distancias):
    distancia_parcial = partial(distancia,dm=matriz_distancias)
    evaluacion = list(map(distancia_parcial,solucion,))
    return evaluacion

def plotAnts(soluciones,cities,mejor,ultimoMejor):
    nSoluciones = len(soluciones)+1

    cx = cities[:,0]
    cy = cities[:,1]

    fig, axes = plt.subplots(math.ceil(nSoluciones/2),2,figsize=(10,15))
    for i,ax in enumerate(axes.flatten()):
        if i ==0:
            ax.scatter(cx,cy,c='r')
            ax.set_title('Mejor Solución')
            ax.plot(cx[mejor+[mejor[0]]],cy[mejor+[mejor[0]]],c='r')
            ax.set_aspect('auto')
        elif i == 1:
            ax.scatter(cx, cy, c='r')
            ax.set_title('Último Solución')
            ax.plot(cx[ultimoMejor + [ultimoMejor[0]]], cy[ultimoMejor + [ultimoMejor[0]]], c='g')
            ax.set_aspect('auto')
        else:
            sol = soluciones[i-2]
            ax.scatter(cx, cy, c='r')
            ax.set_title('Hormiga'+str(i))
            ax.plot(cx[sol + [sol[0]]], cy[sol + [sol[0]]], c='b')
            ax.set_aspect('auto')
    plt.show()

mejorEvaluacion = np.Inf
mejorSolucion = None
for cont in range(2):
    ciudades = np.random.randint(0,cities,hormigas)

    func = partial(correrHormiga,cities=cities,alpha=alpha,beta=beta,tau=tau,eta=eta)
    resultados = list(map(func,ciudades))
    print(resultados,end='\n'*2)
    evaluaciones = evaluarTodo(resultados,dm)
    mejorEvaluacionIter = min(evaluaciones)
    mejorSolucionIter = resultados[evaluaciones.index(mejorEvaluacionIter)]



    print(tau,end='\n'*2)

    tau= actualizarFeromonas(resultados,evaluaciones,tau,Q=10,ro=0.9)
    print(tau,end='\n'*2)

    if(mejorEvaluacion>mejorEvaluacionIter):
        mejorEvaluacion=mejorEvaluacionIter
        mejorSolucion = mejorSolucionIter

    plotAnts(resultados,coordenadas,mejorSolucion,mejorSolucionIter)