from __future__ import print_function
import random


N = 8
blueprint = [i for i in range(N)]
popSize = 700
population = []
crossoverPercent = 0.5
mutationRate = 0.85

class Board:
    def __init__(self, state):
        self.state = state
        self.grid = [[0 for i in range(len(state))] for _ in range(len(state))]
        for col, row in enumerate(self.state):
            self.grid[row][col] = 1
        self.fitness = None


    def display(self):
        for row in range(N):
            for col in range(N):
                if self.grid[row][col] == 1:
                    print("Q", end = " ")
                else:
                    print(".", end = " ")     
            print("\n")

    def calcFitness(self):
        fitness = 0
        for row, col in enumerate(self.state):
        #Check row and column attacks
            for i in range(N):
                if self.grid[col][i] == 1 and i != row:
                    fitness += 1
                elif self.grid[i][row] == 1 and i != col:
                    fitness += 1
        #Check the diagonal attacks
                for j in range(N):
                    if (i+j == row+col or i-j == row-col) and self.grid[j][i] == 1 and (i != row and j != col):
                        fitness += 1
        self.fitness = fitness
            

def generatePop(states):
    global population
    population = [Board(state) for state in states]
    for element in population:
        element.calcFitness()

def sortPop():
    global population
    population.sort(key = lambda x : x.fitness)

def crossover(percent):
    global population
    newPop = population[:int(popSize * percent)]
    for i in range(popSize - len(newPop)):
        index1 = random.randint(0, len(newPop) - 1)
        index2 = random.randint(0, len(newPop) - 1)
        while index2 == index1:
            index2 = random.randint(0, len(newPop) - 1)
        parent1 = population[index1]
        parent2 = population[index2]
    
        p = random.randint(0, N - 1)
        childState = parent1.state[:p]
        notInChildState = [x for x in parent2.state if not x in childState]
        childState.extend(notInChildState)
        newPop.append(Board(childState))
    population = newPop
    for element in population:
        element.calcFitness()
    return

def mutate():
    global population
    for element in population:
        if random.random() >= mutationRate:
            p1 = random.randint(0, N - 1)
            p2 = random.randint(0, N - 1)
            while p2 == p1:
                p2 = random.randint(0, N - 1)
            element.state[p1], element.state[p2] = element.state[p2], element.state[p1]
        element.calcFitness()
    return 


def main():
    global population
    states = [random.sample(blueprint, N) for i in range(popSize)]
    generatePop(states)

    generationCount = 30
    num = 0
    best = random.choice(population)
    bestFitness = float('inf')
    while True:
        count = 0
        print("Generation : {}".format(num))
        best.display()
        num += 1
        if num > generationCount:
            print("Generation count exceeded! Might wanna change the population size!")
            break
        count = 0
        sortPop()
        crossover(crossoverPercent)
        mutate()
        
        for element in population:
            if element.fitness == 0:
                best = element
                bestFitness = element.fitness
                count += 1
            elif element.fitness < bestFitness:
                best = element
                bestFitness = element.fitness
        if count > 0:
            break
    print("------Answer achieved after : {} generations-------".format(num))
    best.display()
main()