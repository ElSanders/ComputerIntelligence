from sys import maxsize
from deap import base, creator, tools
from deap import algorithms
import numpy as np
from numpy.core.fromnumeric import argmax
from numpy.core.shape_base import block
import pandas as pd
import matplotlib.pyplot as plt

#Data for model
location_stats = pd.read_csv("data/destinations.csv", index_col="Name")
user_taste = []

#Evaluation function, determines how likely a selection of places will be a good recommendation for the user
def evaluation(recommendations):
    likelihood, numer, A, B = 0.0, 0.0, 0.0, 0.0
    for i in range(len(recommendations)):
        if(recommendations[i]):
            for j,k in zip(user_taste,location_stats.values.tolist()[i]):
                numer += j*k
                A += j*j
                B += k*k
            likelihood += 1/abs((numer)/(np.sqrt(A)*np.sqrt(B)))
    return likelihood,

#Creating model and toolbox
creator.create("UrbisModel",base.Fitness,weights=(1.0,))
creator.create("Individual",list,fitness = creator.UrbisModel)
toolbox = base.Toolbox()
toolbox.register("select",tools.selRoulette)
toolbox.register("mate",tools.cxTwoPoint)
toolbox.register("mutate",tools.mutFlipBit, indpb= np.random.random())
toolbox.register("evaluate",evaluation)
toolbox.register("attribute",np.random.randint,low=0,high=2)
toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.attribute,n=10)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)
pop = toolbox.population(n=1000)
stats = tools.Statistics(key=lambda ind:ind.fitness.values)
stats.register("max",np.max)
stats.register("mean",np.mean)
stats.register("std",np.std)

#DataFrame to store model evolution
data = pd.DataFrame()

if __name__ == "__main__":
    #Get user data
    usersdF = pd.read_csv("data/users.csv", index_col="Name")
    user_name = input("Name:")
    user_taste = usersdF.loc[user_name]
    
    #Prepare plot
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    
    #Get best recommendations
    best_recommendations = []
    for i in range(10):
        mu = np.random.random()
        pop,log = algorithms.eaMuCommaLambda(pop,toolbox,10,10,mu,1-mu,100,stats = stats,verbose=False)
        best_recommendations.append(pop[argmax(map(evaluation,pop))])
        df = pd.DataFrame(log)
        data= data.append(df)
    
    #Get data for plot
    data = data.reset_index(drop=True)
    dfAverages = data.groupby(['gen']).agg({'max': ['mean', 'std']})
    data_by_gen = data['gen'].unique()
    averages = dfAverages['max']['mean'].values
    desviacion = dfAverages['max']['std'].values
    
    #Prepare plot
    ax.set_title("Evolution of model")
    ax.set_ylabel("Taste match")
    ax.set_xlabel("Generation")
    ax.plot(data_by_gen, averages, color='r')
    ax.plot(data_by_gen, averages - desviacion, linestyle='--', color='b')
    ax.plot(data_by_gen, averages + desviacion, linestyle='--', color='g')
    
    #Find best recommendations selection
    best_rec = best_recommendations[0]
    for rec in best_recommendations:
        if evaluation(rec) > evaluation(best_rec):
            best_rec = rec

    #Start adventure mode
    print("Welcome to Urbis Adventure mode!")
    adventure = []
    max_size = 0

    #Get array of recommended locations
    for i in range(len(best_rec)):
        if(best_rec[i]):
            adventure.append(i)
            max_size+=1
    size = max_size + 1
    
    #Select adventure length
    while(size > max_size):
        size = int(input(f"How long do you want your adventure to be? (max {max_size}) "))
    print("These are the places you will visit in this advenutre:")
    
    #Get random selection of best places for user
    places = np.random.choice(adventure, size=size, replace=False)
    for i in range(size):
        print("    ",i,location_stats.index[places[i]])
    
    #Pick first place to go
    step = [int(input("Where will you head first?"))]
    
    #Go to next place
    while(len(step) != size):
        for i in range(size):
            if(i not in step):
                print("    ",i,location_stats.index[places[i]])
        step.append(int(input("Where will you go next?")))
    input("Please submit a selfie to verify completion! ")
    print("Urbis Adventure finished! We hope you enjoyed your time with us, please come back soon!")

    #Show plot of model
    plt.show(block=True)