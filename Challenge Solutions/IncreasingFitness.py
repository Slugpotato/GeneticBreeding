

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
    myParents = myGraded2[myRetainLength:]

    # Randomly add other individuals from the culled list to promote genetic diversity
    for x in myGraded2[:myRetainLength]:

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


#### Given an individual list and a budget
#### Returns the sum of the individual list subtracted from the target sum
def fitness(givenIndividual, budget):

    totalPrice = 0
    totalPercent = 0
    numberOfStocks = len(givenIndividual)

    for stocks in givenIndividual:
        totalPrice = totalPrice + float(stocks[1])
        totalPercent = totalPercent + float(stocks[2])

    # fitnessLvl = abs(budget - totalPrice + numberOfStocks - totalPercent)
    fitnessLvl = (budget - abs(budget - totalPrice - numberOfStocks - totalPercent))/budget

    if fitnessLvl < 0:
        fitnessLvl = 0

    return fitnessLvl