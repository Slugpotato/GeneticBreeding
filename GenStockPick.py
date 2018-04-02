from random import random, randint
import sys
import matplotlib.pyplot as plt
from openpyxl import load_workbook

retain = 0.500
random_select = 0.05
mutate = 0.001

def main(argv=None):
    if argv is None:
        argv = sys.argv

    stockDict = allStocks()
    numOfStocks = len(stockDict)

    # indiList = individual(stockDict, 1, numOfStocks)
    # print("indiList is ", indiList)
    # print("indiList is of length ", len(indiList))

    # popList = population(10, stockDict, 1, numOfStocks)
    # print("popList is ", popList)
    # print("popList is of length ", len(popList))

    # fitnessScore = fitness(indiList, 100)
    # print("fitnessScore is ", fitnessScore)

    # gradeScore = grade(popList, 100)
    # print("gradeScore is ", gradeScore)

    # evolveFunc = evolve(popList, 100, retain, random_select, mutate)
    # print("my evolveFunc is ", evolveFunc)
    # print("evolveFunc is of length ", len(evolveFunc))

    budget = 1147
    p_count = 100

    p = population(p_count, stockDict, 1, numOfStocks)
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
    letter5 = ''

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

        # Look at the cell with A as the column and the count as the number
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

    for x in givenPopulation:
        myGraded.append((fitness(x, budget), x))

    myGraded2 = []

    for x in sorted(myGraded):
        myGraded2.append(x[1])

    myRetainLength = int(len(myGraded2) * retain)

    myParents = myGraded2[:myRetainLength]

    # Randomly add other individuals to promote genetic diversity
    for x in myGraded2[myRetainLength:]:

        randomNum = random()
        if random_select > randomNum:
            myParents.append(x)

    # Mutate some individuals
    for x in myParents:
        randomNum2 = random()

        if mutate > randomNum2:

            pos_to_mutate = randint(0, len(x) - 1)

            stockDict = allStocks()

            x[pos_to_mutate] = stockDict[randint(0, len(stockDict) - 1)]


    # Breed parents to create children
    parents_length = len(myParents)
    desired_length = len(givenPopulation) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = myParents[male]
            female = myParents[female]
            half = len(male) / 2
            child = male[:int(half)] + female[int(half):]
            children.append(child)

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

    return mySummed / (len(givenPopulation) * 1.0)

#### Given an individual list and a budget
#### Returns the sum of the individual list subtracted from the target sum
def fitness(givenIndividual, budget):

    totalPrice = 0
    totalPercent = 0
    numberOfStocks = len(givenIndividual)

    for stocks in givenIndividual:
        totalPrice = totalPrice + float(stocks[1])
        totalPercent = totalPercent + float(stocks[2])

    fitnessLvl = abs(budget - totalPrice + numberOfStocks - totalPercent)

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