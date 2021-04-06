import numpy as np
import matplotlib.pyplot as plt

#Cantidad de ciudades
cantCiudades = 10;
#Coordenadas de las ciudades
#Este arreglo sirve como el órden en el que se recorren las ciudades
ciudades = np.random.randint(1,20,size = (cantCiudades,2))
#Distancia entre dos ciudades
def distancia(a,b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
#Distancia total recorrida
def disTotal(coords):
    L = 0
    for i,j in zip(coords[:-1],coords[1:]):
        L+= distancia(i,j)
    L +=distancia(coords[0],coords[-1])
    return L

#Crear figura con primera ruta, mejor ruta y curva de mejor encontrado
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(131)
ax1.title.set_text("Primera ruta")
ax2 = fig.add_subplot(132)
ax2.title.set_text("Mejor ruta")
ax3 = fig.add_subplot(133)
ax3.title.set_text("Curva de mejor encontrado")


#Graficar la primera ruta
for i,j in zip(ciudades[:-1],ciudades[1:]):
    ax1.plot([i[0],j[0]],[i[1],j[1]],'r')
ax1.plot([ciudades[0][0], ciudades[-1][0]],[ciudades[0][1],ciudades[-1][1]],'r')
#Graficar puntos de las ciudades
for i in ciudades:
    ax1.plot(i[0],i[1],'ko')

#Temperatura inicial
Temperatura = 30
#Factor de reducción de temperatura
reduccion = 0.9
#U o Distancia total de recorrido
u = disTotal(ciudades)
#Arreglo para registrar los mejores valores
mejores = []
mejores.append(u)
#50 iteraciones parecen ser suficientes para dar un buen resultado
for i in range(50):
    print(i, "Distancia Recorrida =",u)
    #Se van guardando los mejores valores
    #A partir de la segunda iteración, se checa si el valor propuesto es mejor que el anterior
    if i>0:
        x = mejores.pop()
        if(u < x):
            #Si es mejor, se agrega
            mejores.append(x)
            mejores.append(u)
        else:
            #Si no es mejor, se vuelve a agregar el mejor actual
            mejores.append(x)
            mejores.append(x)
    #Se reduce la temperatura
    Temperatura = Temperatura*reduccion
    #Se intenta generar cambios de órden del recorrido
    for j in range(cantCiudades):
        #Se eligen dos ciudades al azar
        cUno,cDos = np.random.randint(0,len(ciudades),size = 2)
        #Intercambian el órden en el que se visitan
        aux = ciudades[cUno].copy()
        ciudades[cUno] = ciudades[cDos]
        ciudades[cDos] = aux
        #Se vuelve a calcular la distancia total
        v = disTotal(ciudades)
        #Algoritmo de Metrópolis
        if v<=u:
            #Si la distancia es menor o igual a la iteración anterior, se cambian
            u = v
        else:
            #Si no es menor, se compara la distribución de Boltzmann y se puede elegir un resultado mayor
            x = np.random.random()
            if x < np.exp(-(v-u)/Temperatura):
                u=v
            else:
                #Si no se elige, se regresan las ciudades a su orden original
                aux = ciudades[cUno].copy()
                ciudades[cUno] = ciudades[cDos]
                ciudades[cDos] = aux

#Se separan las mejores soluciones en vectores de igual tamaño
n = 5
mejores = [mejores[i * n:(i + 1) * n] for i in range((len(mejores) + n - 1) // n)]
print(mejores)
#Se calcula el promedio y la desviación estándar
avg = np.average(mejores, axis=1)
std = np.std(mejores,axis = 1)
arriba = avg + std
abajo = avg - std

#Graficar la curva de mejor solución
ax3.plot(arriba,color = 'r')
ax3.plot(avg,color="blue")
ax3.plot(abajo,color='g')

#Graficar la mejor ruta
for i,j in zip(ciudades[:-1],ciudades[1:]):
    ax2.plot([i[0],j[0]],[i[1],j[1]],'g')
ax2.plot([ciudades[0][0], ciudades[-1][0]],[ciudades[0][1],ciudades[-1][1]],'g')
#Graficar los puntos de las ciudades
for i in ciudades:
    ax2.plot(i[0],i[1],'ko')
plt.show()