from deap import base, creator, algorithms, tools, gp
import multiprocessing
import operator
import numpy as np

#Datos de entrada
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
#Datos de salida
z = [90, 82, 74, 66, 58, 50, 42, 34, 26, 18]

#Función de evaluación (Error cuadrático medio)
def evaluation(individual, input1,input2, outputs):
    func = tb.Compile(expr=individual)
    error = 0
    for i in range(len(input1)):
        error+=(outputs[i]-func(input1[i],input2[i]))**2
    error = error/len(z)
    return error,

#Primitive Set
ps = gp.PrimitiveSet("main", 2) #2 argumentos
ps.addPrimitive(operator.add, 2) #Operaciones
ps.addPrimitive(operator.mul, 2)
ps.addPrimitive(operator.sub, 2)
ps.renameArguments(ARG0='x') #Renombrar argumentos de entrada
ps.renameArguments(ARG1='y')
ps.addEphemeralConstant('R', lambda: np.random.randint(0,10))


#Creator
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=ps)

#Toolbox
tb = base.Toolbox()
tb.register("Expression", gp.genHalfAndHalf, pset=ps, min_=2, max_=5)
tb.register("select", tools.selTournament, tournsize=3)
tb.register("mate", gp.cxOnePoint)
tb.register("mutate", gp.mutNodeReplacement, pset=ps)
tb.register("Compile", gp.compile, pset=ps)
tb.register("individual", tools.initIterate, creator.Individual, tb.Expression)
tb.register("Population", tools.initRepeat, list, tb.individual)
tb.register("evaluate", evaluation, input1=x,input2=y, outputs=z)#Función de evaluación

#Stats
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register('avg', np.mean)
stats.register('std', np.std)
stats.register('min', np.min)
stats.register('max', np.max)


#Hall of fame
hall = tools.HallOfFame(1) #Un solo valor, para que saque un solo resultado

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    tb.register("map", pool.map)
    pop = tb.Population(n=100)
    pop2, log = algorithms.eaMuPlusLambda(population=pop,toolbox=tb, mu=len(pop), lambda_=len(pop), cxpb=0.5, mutpb=0.1, ngen=50, stats=stats, halloffame=hall, verbose=True)
    print("Función LISP:")
    print(hall[0])
    print("Error cuadrático medio:")
    print(tb.evaluate(hall[0], input1=x,input2=y, outputs=z))