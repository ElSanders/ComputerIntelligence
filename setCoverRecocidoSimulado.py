import numpy as np
import matplotlib.pyplot as plt
#Se le pregunta al usuario si usar un set random o uno que garantiza por lo menos una combinación perfecta
option = input("a) Usar Set Random\nb) Usar Set Sesgado (Garantiza por lo menos una solución perfecta)\n")
if(option == 'a'):
    universeSize = int(input("Tamaño de Set: "))
    nBoxes = int(input("Número de Cajas: "))
    #Se genera el universo al azar con números entre 0 y universeSize+100
    universe = np.random.default_rng().choice(universeSize+100,size=universeSize,replace=False)
    universe.sort()
    #Se genera la cantidad de cajas pedidas con números en el universo
    boxes = []
    for i in range(nBoxes):
        box = list(np.random.choice(universe,np.random.randint(low=1,high=universeSize//3),replace=False))
        boxes.append(box)
    #Como las cajas se generan aleatoriamente, hay una probabilidad de que no todos
    #los valores terminen en estas, por lo que se verifica que entre todas las cajas
    #haya por lo menos una iteración de cada número
    for i in universe:
        itemIncluded = False
        for j in boxes:
            if i in j:
                itemIncluded = True
        if(itemIncluded == False):
            boxes[np.random.randint(low=0,high=len(boxes))].append(i)
elif(option == 'b'):
    #Si se elige el set sesgado, se crea un universo de 1 a 20
    universeSize = 20
    nBoxes = 15
    universe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    #Las primeras 7 cajas contienen la combinación perfecta de la solución
    boxes = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20]]
    #El resto de las cajas se genera aleatoriamente
    for i in range(nBoxes-len(boxes)):
        box = list(np.random.choice(universe, np.random.randint(low=1, high=universeSize // 3), replace=False))
        boxes.append(box)
    for i in universe:
        itemIncluded = False
        for j in boxes:
            if i in j:
                itemIncluded = True
        if (itemIncluded == False):
            boxes[np.random.randint(low=0, high=len(boxes))].append(i)
    #El órden de las cajas es aleatorio
    np.random.shuffle(boxes)

else:
    quit()
#Se imprime el set y las cajas creadas
print("Set: ",universe)
print("Cajas: ",boxes)

#La función seeValues toma un vector de datos binarios que representan
#si una caja es elegida o no. Regresa un vector con los números contenidos
#en las cajas seleccionadas, ordenados de menor a mayor.
def seeValues(selection):
    currentValues = []
    for i in range(len(selection)):
        if selection[i] == 1:
            for j in boxes[i]:
                currentValues.append(j)
    currentValues.sort()
    return currentValues
#La función de evaluación recibe el mismo vector que seeValues y la llama al inicio.
def evaluation(selection):
    currentValues = seeValues(selection)
    #El resultado empieza en 0
    result = 0
    for i in universe:
        #Por cada número en el universo se cuenta cuántas veces existe en el set creado
        #por las cajas y se suma el excedente, si hay.
        if(currentValues.count(i)>1):
            result+=currentValues.count(i)-1
        elif(currentValues.count(i)==0):
            #Si algún valor no está en el set creado con las cajas, se penaliza con 10
            result+=10
    #Si la cantidad de excedentes es mayor que la cantidad de datos en el set original
    #la selección es muy mala, entonces se penaliza al multiplicarse por sí misma.
    if(result>=universeSize):
        result*=result
    currentValues.sort()
    return result
#Se inicializan las variables que se usarán en recocido simulado
tempReduction = 0.99
Temperature = 100
#Se genera el vector de datos binarios de manera aleatoria del tamaño de las cajas que representa la selección
selection = [np.random.randint(0,2)for i in range(nBoxes)]
#U se inicializa como la evaluación de la selección aleatoria
u = evaluation(selection)
lastEval = u
bestResults = []
bestResults.append(u)
bestSelection = selection
repeats = 0
iterations = 0
#El algoritmo termina si la misma evaluación se repite 10 veces
while(repeats<10):
    iterations+=1
    if(lastEval == u):
        repeats+=1
    else:
        repeats = 0
    lastEval = u
    #print(iterations,selection, u)
    #Se revisa si el resultado más reciente es mejor que el mejor hasta ahora y se agrega
    #al vector bestResults, si no, se agrega el mismo mejor valor hasta el momento.
    if iterations>0:
        x = bestResults.pop()
        if(u < x):
            bestResults.append(x)
            bestResults.append(u)
            bestSelection = selection.copy()
        else:
            bestResults.append(x)
            bestResults.append(x)
    #Se reduce la temperatura
    Temperature = Temperature*tempReduction
    for j in range(universeSize):
        #Se genera un vector de enteros que representan posiciones del vector selection
        changes = np.random.randint(0,len(selection),size = nBoxes//2)
        #Estas posiciones se cambian (se elige si no se había elegido y viceversa)
        aux = selection.copy()
        for i in changes:
            if(selection[i] == 1):
                selection[i] = 0
            else:
                selection[i] = 1
        #en v se guarda la evaluación de la nueva selección
        v = evaluation(selection)
        #si es mejor (menor) se sustituye v en u
        if v<=u:
            u = v
        else:
            #Si no es menor, se compara la distribución de Boltzmann y se puede elegir un resultado mayor
            x = np.random.random()
            if x < np.exp(-(v-u)/Temperature):
                u=v
            else:
                # Si no cambia, se mantiene la selección anterior
                selection = aux
#Resultados finales
print("*****************************************")
print("Resultados Finales")
print("*****************************************")
print("Mejor Selección de Cajas: ",end=" ")
#Se imprimen las posiciones de las cajas elegidas
for i in range(len(bestSelection)):
    if(bestSelection[i] == 1):
        print(i,end=", ")
print("")
#Se imprime el contenido de las cajas seleccionadas
print("Contenido de Cajas: ",end=" ")
for i in range(len(bestSelection)):
    if(bestSelection[i] == 1):
        print(boxes[i],end=", ")
print("")
#Se imprime el set original y el set obtenido por la selección de cajas
print("Set Original: ",*universe)
print("Set Obtenido: ",*seeValues(bestSelection))
print("Objetos de sobra: ",evaluation(bestSelection))
#Se grafica la curva de mejor resultado y el avance de mejores resultados (cómo fue cambiando el mejor resultado)
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.title.set_text("Curva de Mejor Resultado")
ax2 = fig.add_subplot(122)
ax2.title.set_text("Avance de Mejores Resultados")
ax2.plot(bestResults)
while(len(bestResults)%10 != 0):
    bestResults.append(bestResults[-1])
bestResults = np.array_split(bestResults,10)
avg = np.average(bestResults,axis=1)
std = np.std(bestResults,axis=1)
arriba = avg + std
abajo = avg - std
ax1.plot(arriba,color = 'r')
ax1.plot(avg,color="blue")
ax1.plot(abajo,color='g')
plt.show()