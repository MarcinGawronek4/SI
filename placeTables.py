import copy
import random
from math import sqrt

import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

import constants

mutationRate = 0.05
RNG = random


def geneticAlgorithm(stoly, n_populacja, eliteSize, mutationRate, generations):
    pop = generatePop(n_populacja, stoly)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)

    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute


def randompos():
    return RNG.randint(0, constants.MAP_HEIGHT - 1)


def manh(t1, t2):
    # return abs(istate[0] - fstate[0]) + abs(istate[1] - fstate[1])
    return abs(t1.x - t2.x) + abs(t1.y - t2.y)


def distance(t1, t2):
    return int(sqrt((abs(t1.x - t2.x) ** 2) + (abs(t1.y - t2.y) ** 2)))


def symetrytable(table):
    # x = -(table.x - (constants.MAP_HEIGHT / 2)) + (constants.MAP_HEIGHT / 2)
    # y = -(table.y - (constants.MAP_HEIGHT / 2)) + (constants.MAP_HEIGHT / 2)
    x= constants.MAP_HEIGHT-table.x-1
    y= constants.MAP_HEIGHT-table.y-1
    return wtable(x, y)


def rankRoutes(population):
    fitnessResults = {}
    print(len(population))
    for i in range(0, len(population)):
        fitnessResults[i] = population[i].scoreFitness()
        # print(i)
        # print(population[i])
        # print(fitnessResults[i])
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


def mutatePopulation(population, mutationRate):
    mutatedPop = []

    for ind in range(0, len(population)):
        # mutatedInd = mutate(population[ind], mutationRate)
        # print(len(population))
        # print(ind)
        mutatedInd = copy.copy(population[ind])
        if RNG.random() < mutationRate:
            mutatedInd.mutation()
        # if False:
        #     mutatedInd.mutation()
        mutatedPop.append(mutatedInd)
    return mutatedPop


def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    print("lenght " + str(length))
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, eliteSize):
        children.append(matingpool[i])

    for i in range(0, length):
        child = pool[i]
        child = copy.copy(child)
        parent = copy.copy(pool[len(matingpool) - i - 1])
        child.crossover(parent)

        children.append(child)
    # child = breed(pool[i], pool[len(matingpool)-i-1])
    # children.append(child)
    print("returned breed " + str(len(children)))
    return children


def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    # a=popRanked
    # print("popRanked " + str(len(popRanked)))
    # print(popRanked[20])
    selectionResults = selection(popRanked, eliteSize)
    # print("2 " + str(len(selectionResults)))
    # print(selectionResults[20])
    matingpool = matingPool(currentGen, selectionResults)
    # print("3 " + str(len(matingpool)))
    # print(matingpool[20])
    children = breedPopulation(matingpool, eliteSize)
    # print("4 " + str(len(children)))
    # print(children[21])
    nextGeneration = mutatePopulation(children, mutationRate)
    # print("5 " + str(len(nextGeneration)))
    # print(nextGeneration[20])
    return nextGeneration


class entity:
    def __init__(self, tables):
        self.tables = tables.copy()
        self.fitness = 0
        self.score = 0

    def __cmp__(self):
        return entity(copy.copy(self.tables))

    def __copy__(self):
        return entity(copy.copy(self.tables))

    # def copy(self):
    #     return entity(self.tables.copy())

    def mutation(self):
        # stlenght= len(self.tables)
        # ltables = len(self.tables) - 1
        # tomutate = self.tables[RNG.randint(0, ltables)]
        # newtable = wtable(randompos(), randompos())
        # options=[wtable(tomutate.x+x,tomutate.y+y) for x in range(-1, 2) for y in range(-1, 2)]
        done= False
        while not done:
            tomove = random.choice(self.tables)
            options=[wtable(tomove.x+x,tomove.y+y) for x in range(-1, 2) for y in range(-1, 2)]
            passed=[]
            for t in options:
                if not any(wtable(t.x+x,t.y+y)==st and st is not tomove for st in self.tables for x in range(-1, 2) for y in range(-1, 2)):
                    passed.append(t)
            newtable=None
            if passed:
                newtable=random.choice(passed)
                self.tables.remove(tomove)
                self.tables.append(newtable)
                done=True
        # [(t == t2) and not (t is t2)]
        # isok = any((t == t2) and not (t is t2) for t in self.tables for t2 in self.tables)
        # passed=[]
        # for t in options:
        #     if not any(wtable(t.x+x,t.y+y)==st and st is not tomutate for st in self.tables for x in range(-1, 2) for y in range(-1, 2)):
        #         passed.append(t)
        # print(passed)




        # ok = False
        # while not ok:
        #     if random.choice([True, False]):
        #         newtable.x = (newtable.x + 1) % 10
        #     else:
        #         newtable.y = (newtable.y + 1) % 10
        #     ok = True
        #     if any(wtable(newtable.x + x, newtable.y + y) == t for t in self.tables for x in range(-1, 2) for y in range(-1, 2)):
        #         print("mutate false")
        #         ok = False
        # self.tables.append(newtable)
        # self.tables.remove(tomutate)
        # isok2=any((t == t2) and not (t is t2) for t in self.tables for t2 in self.tables)
        # xddp=1
        # ndlenght= len(self.tables)
        # if stlenght!=ndlenght:
        #     print("mutate!!!")

    def totable(self):
        table = [[0 for x in range(constants.MAP_HEIGHT)] for y in range(constants.MAP_HEIGHT)]
        for t in self.tables:
            table[t.x][t.y] = 1
        return table

    def symetryscore(self):
        score = 0
        for t in self.tables:
            s = symetrytable(t)
            for d in self.tables:
                if d == s:
                    score = score + 1
        return score

    def manhatanscore(self):
        score = 0
        for t1 in self.tables:
            for t2 in self.tables:
                score = score + manh(t1, t2)
        return score

    def distancescore(self):
        score = 0
        for t1 in self.tables:
            for t2 in self.tables:
                score = score + distance(t1, t2)
        return score

    def getscore(self):
        print(str(len(self.tables)) + "score " + str(self.symetryscore()) + " " + str(self.distancescore()) + " " + str(
            self.manhatanscore()))
        if self.score == 0:
            # self.score = (self.symetryscore()*100 + self.distancescore()*30)/(self.manhatanscore())
            # self.score = (self.symetryscore() * 50) / (self.manhatanscore())
            self.score = 1/float(self.manhatanscore())
        return self.score

    def __repr__(self):
        table = [[0 for x in range(constants.MAP_HEIGHT)] for y in range(constants.MAP_HEIGHT)]
        for t in self.tables:
            table[t.x][t.y] = 1
        stringu = ""
        for r in table:
            stringu = stringu + str(r) + "\n"
        stringu = stringu + "\n" + str(self.tables) + "\n"
        return str(stringu)

    def scoreFitness(self):
        if self.fitness == 0:
            self.fitness = float(self.getscore())
        return self.fitness

    def crossover(self, other):
        # stlenght= len(self.tables)
        genes = 0
        while genes < 3:
            timeout = 0
            s = RNG.choice(self.tables)
            o = RNG.choice(other.tables)
            while any(
                    wtable(o.x + x, o.y + y) == t for x in range(-1, 2) for y in range(-1, 2) for t in
                    self.tables) and timeout < 50:
                o = RNG.choice(other.tables)
                timeout = timeout + 1
                # print(self.tables)
            if timeout < 49:
                self.tables.remove(s)
                self.tables.append(o)
            genes = genes + 1

            # ndlenght= len(self.tables)
            # if stlenght!=ndlenght:
            #     print("CORSOVER!!!")
            # other.tables.remove(o)
            # other.tables.append(s)
        # timeout = 0
        # s = None
        # o = None
        # ok = False
        # while not ok:
        #     ok = True
        #     print(ok)
        #     s = RNG.choices(self.tables)
        #     print(s)
        #     for t in other.tables:
        #         for t2 in s:
        #             if t == t2:
        #                 ok = False
        #                 break
        # ok = True
        # while not ok:
        #     ok = True
        #     o = RNG.choices(other.tables)
        #     for t in self.tables:
        #         for t2 in s:
        #             if t == t2:
        #                 ok = False
        #                 break
        # for t in s:
        #     self.tables.remove(t)
        # for t in o:
        #     other.tables.remove(t)
        # for t in s:
        #     other.tables.append(t)
        # for t in o:
        #     self.tables.append(t)


class wtable:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


def createEntity(n):
    tabletab = [wtable(randompos(), randompos())]

    while len(tabletab) < n:
        newtable = wtable(randompos(), randompos())
        # xd =[wtable(x,y)for x in range(-1, 2) for y in range(-1, 2)]
        # print(xd)
        ok = True
        for t in tabletab:
            if any(wtable(newtable.x + x, newtable.y + y) == t for x in range(-1, 2) for y in range(-1, 2) for t in
                   tabletab):
                ok = False
                break
        if ok:
            tabletab.append(newtable)
    return entity(tabletab)


def generatePop(n, k):
    finalist = []
    for i in range(0, n):
        finalist.append(createEntity(k))
    print(finalist)
    return finalist


def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = generatePop(popSize, population)
    print(pop)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])

    best = 0
    for i in range(1, len(pop)):
        if (pop[best].getscore() < pop[i].getscore()):
            best = i
    print(pop[best])
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()


# entity1 = entity([wtable(0, 1)])
# entity12 = copy.copy(entity1)
# entity12=entity1.copy()
# entity1.tables.append("asd")
# print(entity1.tables)
# print(entity12.tables)

# geneticAlgorithmPlot(population=10, popSize=200, eliteSize=25, mutationRate=0.02, generations=200)
#print(geneticAlgorithm(stoly=10,n_populacja=200,eliteSize=20,mutationRate=0.02,generations=80).totable())