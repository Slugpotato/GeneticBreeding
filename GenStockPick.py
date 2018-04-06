from random import random, randint
import sys
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import unittest

retain = 0.500
random_select = 0.05
mutate = 0.001

def main(argv=None):
    if argv is None:
        argv = sys.argv

    listOfStocks = allStocks()
    numOfStocks = len(listOfStocks)

    # print(listOfStocks)

    # indiList = individual(listOfStocks, 1, numOfStocks)
    # print("indiList is ", indiList)
    # print("indiList is of length ", len(indiList))

    # popList = population(10, listOfStocks, 1, numOfStocks)
    # print("popList is ", popList)
    # print("popList is of length ", len(popList))

    # fitnessScore = fitness(indiList, 100)
    # print("fitnessScore is ", fitnessScore)

    # gradeScore = grade(popList, 100)
    # print("gradeScore is ", gradeScore)

    # evolveFunc = evolve(popList, 100, retain, random_select, mutate)
    # print("my evolveFunc is ", evolveFunc)
    # print("evolveFunc is of length ", len(evolveFunc))

    budget = 1000
    p_count = 100

    p = population(p_count, listOfStocks, 1, numOfStocks)
    fitness_history = [grade(p, budget), ]
    for i in range(1, 100):
        p = evolve(p, budget, retain, random_select, mutate)
        fitness_history.append(grade(p, budget))
        # print("I is currently ", i)

    finalList = p[0]
    finalPrice = 0
    for indi in finalList:
        finalPrice = finalPrice + indi[1]


    i = 0
    xAxis = []
    for datum in fitness_history:
        i = i + 1
        xAxis.append(i)

    print("fitness_history is ", fitness_history)
    plt.plot(xAxis, fitness_history, 'r--', )
    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    print('\n')
    print("p[0] is ", p[0])
    print("And final price is: ", finalPrice)
    plt.show()



def allStocks():
    # print("Gathering prospective stocks\n")

    ####################################################
    ## Creating excel document here and include columns
    ####################################################
    wb = load_workbook('futureStocks.xlsx')

    ####################################################
    ## Declaring the letters to be used in the writing to the excel sheet
    ####################################################

    letter = 'A'
    letter2 = 'B'
    letter3 = 'C'
    letter4 = 'E'

    ####################################################
    ## While i is not greater than number of elements find a break up title into cells.
    ####################################################

    count = 1
    stockList = []

    # Go through every stock in column A starting with A1 until the cell value is none
    while True:
        sheet = wb.get_sheet_by_name('Sheet1')
        ws = wb.active

        # Start count at 1 and iterate
        count = count + 1

        # Look at the cells in each column, using count as the row number
        stock = sheet[letter + str(count)]

        currPrice = sheet[letter2 + str(count)]

        dividendPer = sheet[letter3 + str(count)]

        fiveYearPer = sheet[letter4 + str(count)]

        if stock.value == None or currPrice.value == None or dividendPer.value == None \
                or fiveYearPer.value == None:
            break

        combinedPer = (5 * float(dividendPer.value)) + float(fiveYearPer.value)
        combinedPer = round(combinedPer, 3)

        tempPrice = currPrice.value

        if type(tempPrice) is str:
            tempPrice = tempPrice.replace("$", "")

            print("tempPrice is now ", tempPrice)

        stockList.append([stock.value, tempPrice, combinedPer])

    return stockList

#### Evolution...muahahaha
def evolve(givenPopulation, budget, retain, random_select, mutate):

    myGraded = []

    # Iterate through population and determine fitness of individuals
    # Append fitness and individual to myGraded list
    for x in givenPopulation:
        myGraded.append((fitness(x, budget), x))

    myGraded2 = []

    # Sort through population by fitness and add to new list
    for x in sorted(myGraded):
        myGraded2.append(x[1])

    # Determine index of retained list, given retain percentage
    myRetainLength = int(len(myGraded2) * retain)

    # Keep percentage of fittest individuals
    myParents = myGraded2[:myRetainLength]

    # Randomly add other individuals from the culled list to promote genetic diversity
    for x in myGraded2[myRetainLength:]:

        randomNum = random()

        # Everytime the random number is less than the random_select variable, add individual
        if random_select > randomNum:
            myParents.append(x)

    # Mutate some individuals in the parent list
    for x in myParents:
        randomNum2 = random()

        # Every time the random number generated is less than the mutate percentage, replace
        # one of the stocks in that parent individual with a random stock
        if mutate > randomNum2:
            pos_to_mutate = randint(0, len(x) - 1)
            listOfStocks = allStocks()
            x[pos_to_mutate] = listOfStocks[randint(0, len(listOfStocks) - 1)]


    # Refill population given surviving parents
    parents_length = len(myParents)
    desired_length = len(givenPopulation) - parents_length
    children = []

    # Breed parents to create children
    while len(children) < desired_length:

        # Choose two parents
        parent1 = randint(0, parents_length - 1)
        parent2 = randint(0, parents_length - 1)

        # Make sure they are not the same parent
        if parent1 != parent2:
            parent1 = myParents[parent1]
            parent2 = myParents[parent2]

            # Create a child by adding the first half of the first parent and the second half
            # of the second parent
            half = len(parent1) / 2
            child = parent1[int(half):] + parent2[:int(half)]
            children.append(child)

    # Add children to parents and return the population of the next generation
    myParents.extend(children)
    return myParents

#### Given a population list of individual lists and a budget,
#### this computes the fitness of each individual in the population and sums these together.
#### Returns the average of the sum of fitness scores
def grade(givenPopulation, budget):

    mySummed = 0

    for x in givenPopulation:
        tempFitness = fitness(x, budget)
        mySummed = tempFitness + mySummed

    return mySummed / len(givenPopulation)

#### Given an individual list and a budget
#### Returns the sum of the individual list subtracted from the target sum
def fitness(givenIndividual, budget):

    totalPrice = 0
    totalPercent = 0
    numberOfStocks = len(givenIndividual)

    for stocks in givenIndividual:
        totalPrice = totalPrice + float(stocks[1])
        totalPercent = totalPercent + float(stocks[2])

    fitnessLvl = abs(budget - totalPrice - numberOfStocks - totalPercent)

    return fitnessLvl


#### Population of individual lists, count is number of individual lists.
####  Returns a list of individual lists
def population(count, stockList, minLen, maxLen):
    # Create a number of individuals (i.e. a population).
    #
    # count: the number of individuals in the population
    # stockList: list of all stocks
    # minLen: the minimum length of an individual list
    # maxLen: the maximum length of an individual list

    tempPop = []

    for x in range(count):
        tempPop.append(individual(stockList, minLen, maxLen))

    return tempPop


#### Individual list of random stocks
#### Returns list of stocks, picked from all stocks, with a length in the range between min to max.
def individual(stockList, minLen, maxLen):

    tempIndi = []

    length = randint(minLen, maxLen)
    for x in range(length):
        tempIndi.append(stockList[randint(1, (len(stockList) - 1))])

    return tempIndi



if __name__ == '__main__':
    main()