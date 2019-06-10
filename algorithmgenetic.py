from numpy import random
from random import choice


def Genetic(money, payment):
    population = initPopulation(1500, money)
    iteration = 0
    population.sort(key=lambda x: -fitness(x, money, payment))
    while (iteration <= 500):
        newPopulation = []
        for x in range(0, len(population), 2):
            parent1 = population[x]
            v = x+1
            if(random.randint(0, 10) > 5):
                v = random.randint(1, 13)
                while v==x:
                    v=random.randint(1,13)

            parent2 = population[v]
            child1, child2 = crossover(parent1, parent2)
            mutation(child1, money)
            mutation(child2, money)
            newPopulation.append(child1)
            newPopulation.append(child2)
        for t in newPopulation:
            if (t not in population):
                population.append(t)
        population.sort(key=lambda x: -fitness(x, money, payment))
        best = population[0]
        print("Fitness: ",fitness(best,money,payment), best)
        #print(best)
        delete = len(newPopulation)
        del population[delete:]
        iteration = iteration + 1
        #if(fitness(best,money,payment)>100):
            #iteration = 81

    return set(best)


def mutation(changes, money):
    z=0
    for i in money:
        if (random.randint(0, 100) <= 50):
            j = random.randint(0, i[1])
            changes[money.index(i)] = (i[0], j)

            
def crossover(parent1, parent2):
    child1=[]
    child2=[]
    #print(parent1, parent2)
    for i in parent1:
        a = tuple(i)
        k = tuple(choice(parent2))
        child1.append((a[0],k[1]))
    for m in parent2:
        b = tuple(m)
        o = tuple(choice(parent1))
        child2.append((b[0],o[1]))
    return (child1, child2)


def initPopulation(n, money):
    population = []
    for i in range(n):
        individual = []
        for j,k in money:
            individual.append((j,random.randint(0, k))) 
        #print (individual)
        if individual not in population:
            population.append(individual)
    return population


def fitness(change, money, payment):
    fitness = 0
    if(sum(i*j for i,j in change)<=payment):
        fitness = sum(i*j for i,j in change)/payment
        if(fitness==1):
            fitness += ((sum(j for i,j in money)- sum(j for i,j in change))/sum(j for i,j in money))
        return fitness
    else:
        return 0           

        
                    
def get_money(payment):
  money = [(200,3),(100,5),(50,3),(20,8),(10,10),(5,20),(2,10),(1,12),(0.5,20),(0.2,15),(0.1,7),(0.05,23),(0.01,17)]  
  Genetic(money, payment)
 
