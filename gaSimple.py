from deap import base, creator, tools
import random
from deap import algorithms
import numpy as np
import pandas as pd
import multiprocessing
import matplotlib.pyplot as plt

#La función de evaluación
def evaluacion(valores):
    maxW = 165
    price=0
    weight = 0
    w = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
    p = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
    for i in range(10):
        #Obtiene la sumatoria de pesos y precios
        price+= valores[i]*p[i]
        weight+= valores[i]*w[i]
    if(weight>maxW):
        #Divide entre 100 el precio si excede el precio para garantizar que no se elija
        price = price/100
    return price,
#Esta función de peso es sólo para mostrar el peso de las soluciones finales
def peso(valores):
    weight = 0
    w = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
    for i in range(10):
        weight += valores[i] * w[i]
    return weight
#Se quiere maximizar, por eso el peso es 1
creator.create("Knapsack",base.Fitness,weights=(1.0,))
creator.create("Individual",list,fitness = creator.Knapsack)
toolbox = base.Toolbox()
toolbox.register("select",tools.selRoulette)
toolbox.register("mate",tools.cxOnePoint)
#Probabilidad de 0.2 da cambiar un individuo dio buenos resultados
toolbox.register("mutate",tools.mutFlipBit, indpb= 0.2)
toolbox.register("evaluate",evaluacion)
#Creación de listas de 10 individuos binarios
toolbox.register("attribute",random.randint,a=0,b=1)
toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.attribute,n=10)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)
#Se crean 10 poblaciones de 10 cada uno
pop = toolbox.population(n=10)

stats = tools.Statistics(key=lambda ind:ind.fitness.values)
stats.register("min",np.min)
stats.register("max",np.max)
stats.register("mean",np.mean)
stats.register("std",np.std)

dfA = pd.DataFrame()
dfB = pd.DataFrame()
dfC = pd.DataFrame()

if __name__ == "__main__":
    #Creación de gráficas por imprimir
    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(131)
    ax1.title.set_text("eaSimple")
    ax2 = fig.add_subplot(132)
    ax2.title.set_text("eaMuPlusLambda")
    ax3 = fig.add_subplot(133)
    ax3.title.set_text("eaMuCommaLambda")
    pool = multiprocessing.Pool()
    toolbox.register("map",pool.map)
    #Algoritmo 1
    print("Ejecutando algoritmo eaSimple...")
    for i in range(10):
        pop,log = algorithms.eaSimple(pop,toolbox,1.0,0.5,100,stats = stats,verbose=False)
        df2 = pd.DataFrame(log)
        df2['algoritmo'] = 'eaSimple'
        df2['corrida'] = i
        dfA= dfA.append(df2)
    dfA = dfA.reset_index(drop = True)
    dfPromediosA = dfA.groupby(['algoritmo', 'gen']).agg({'max': ['mean', 'std']})
    x = dfA['gen'].unique()
    promedios = dfPromediosA['max']['mean'].values
    desviacion = dfPromediosA['max']['std'].values
    #Se guardan los valores pertinentes y se grafica
    ax1.plot(x, promedios, color='r')
    ax1.plot(x, promedios - desviacion, linestyle='--', color='b')
    ax1.plot(x, promedios + desviacion, linestyle='--', color='g')
    mejor = 0
    for i in range(len(pop)):
        if(evaluacion(pop[i])>evaluacion(pop[mejor])):
            mejor = i
    mejorSimple = pop[mejor]
    #Se guarda el mejor resultado del primer algoritmo
    #Algoritmo 2
    print("Ejecutando algoritmo eaMuPlusLambda...")
    for i in range(10):
        pop,log = algorithms.eaMuPlusLambda(pop,toolbox,10,10,0.5,0.5,100,stats = stats,verbose=False)
        df2 = pd.DataFrame(log)
        df2['algoritmo'] = 'eaMuPlusLambda'
        df2['corrida'] = i
        dfB= dfB.append(df2)
    dfB = dfB.reset_index(drop=True)
    dfPromediosB = dfB.groupby(['algoritmo', 'gen']).agg({'max': ['mean', 'std']})
    x = dfB['gen'].unique()
    promedios = dfPromediosB['max']['mean'].values
    desviacion = dfPromediosB['max']['std'].values
    #Se guardan los valores pertinentes y se grafica
    ax2.plot(x, promedios, color='r')
    ax2.plot(x, promedios - desviacion, linestyle='--', color='b')
    ax2.plot(x, promedios + desviacion, linestyle='--', color='g')
    mejor = 0
    for i in range(len(pop)):
        if (evaluacion(pop[i]) > evaluacion(pop[mejor])):
            mejor = i
    mejorPlus = pop[mejor]
    #Se guarda el mejor resultado del segundo algoritmo
    #Algoritmo 3
    print("Ejecutando algoritmo eaMuCommaLambda...")
    for i in range(10):
        pop,log = algorithms.eaMuCommaLambda(pop,toolbox,10,10,0.5,0.5,100,stats = stats,verbose=False)
        df2 = pd.DataFrame(log)
        df2['algoritmo'] = 'eaMuCommaLambda'
        df2['corrida'] = i
        dfC= dfC.append(df2)
    dfC = dfC.reset_index(drop=True)
    dfPromediosC = dfC.groupby(['algoritmo', 'gen']).agg({'max': ['mean', 'std']})
    x = dfC['gen'].unique()
    promedios = dfPromediosC['max']['mean'].values
    desviacion = dfPromediosC['max']['std'].values
    #Se guardan los valores pertinentes y se grafica
    ax3.plot(x, promedios, color='r')
    ax3.plot(x, promedios - desviacion, linestyle='--', color='b')
    ax3.plot(x, promedios + desviacion, linestyle='--', color='g')
    mejor = 0
    for i in range(len(pop)):
        if (evaluacion(pop[i]) > evaluacion(pop[mejor])):
            mejor = i
    # Se guarda el mejor resultado del segundo algoritmo
    mejorComma = pop[mejor]

    #Se imprimen los resultados pertinentes y mejores soluciones
    print("eaSimple")
    print(dfPromediosA.to_string())
    print("eaMuPlusLambda")
    print(dfPromediosB.to_string())
    print("eaMuCommaLambda")
    print(dfPromediosC.to_string())
    print("Mejor solución eaSimple:", mejorSimple)
    print("Precio:", evaluacion(mejorSimple)[0])
    print("Peso:", peso(mejorSimple))
    print("Mejor solución eaMuPlusLambda:", mejorPlus)
    print("Precio:", evaluacion(mejorPlus)[0])
    print("Peso:", peso(mejorPlus))
    print("Mejor solución eaMuCommaLambda:", mejorComma)
    print("Precio:", evaluacion(mejorComma)[0])
    print("Peso:", peso(mejorComma))
    plt.show()