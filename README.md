# GeneticBreeding
Part 1 of the neuroevolution tutorial series. Focuses on the basics of genetic breeding algorithms.

Tutorial link: 
http://designingafuture.com/tutorials/neuroevolutionP1

==========================
Disclaimer:
==========================
I based this implementation of Genetic Breeding on this tutorial: 
https://lethain.com/genetic-algorithms-cool-name-damn-simple/ 

Based on this, I was able to adapt the concept of genetic breeding algorithms to first solve a unique problem I was having with my stock portfolio and then later optimize a neural network (part 2)

However, credit is definitely due to that initial tutorial and I definitely recommend checking it out!

==========================
Summary:
==========================

Genetic Algorithms:
https://en.wikipedia.org/wiki/Genetic_algorithm

At it's core, Genetic Algorithms are a optimization method that can be applied to a wide variety of problems. For my tutorial I chose to optimize a problem I was having with choosing stocks for my portfolio however you can apply this to whatever problems you need optimized! :D

The code takes in the stock related data from an excel file, (futureStocks.xlsx), and returns a set of stocks based predetermined weights we input beforehand. Parameters such as the percent of the population retained after each generation, probability of random mutations, population size and number of generations are all going to affect the optimality of the result. This code, by it's very nature, is non-deterministic. Which means the same output is not guaranteed with every execution. You can change this to be deterministic by seeding the random number generators, but by doing so, you would limit the potential reach/effectiveness of the algorithm.

 Genetic algorithims also have a tendency to converge at local maximas, so different runs may produce solutions closer to the global optimum. I recommend running the program a few times and using the most optimal solution from these runs. Depending on how important it is for your solution to be exactly correct, you can also play with a myriad of weights/parameters, (like those previously mentioned), to achieve a better solution.

 The specific problem that I chose to optimize through a genetic algorithm centers on picking a set of stocks that best meet my requirements. As a side note, I am in no way implying that any of these stocks are good investments or that the critera by which I measure them for this tutorial are even optimal investing strategies. That said, I wanted to find a list of stocks that came as close as possible to my overall budget while also valuing the dividend return and the past five years of growth. Additionaly I wanted to put extra weight on a set with a greater number of stocks over that of only a few, since this (at least in theory) increase the diverity of my portfolio. Sounds like a fun problem right? Hopefully you can see how one could use this technique to solve even more complex problems!

 Anyway, make sure to check out my tutorial here for a more in depth explanation on how this code works:
 http://designingafuture.com/tutorials/neuroevolutionP1

==========================
To run this code:
==========================

Each sub-function has an example call commented out in the main function, and in the future this will be moved to proper unit tests. You can run this code as is, just make sure the given excel file is in the same directory. 


Parameters to change/play around with are:

On line 7:

retain = 0.500

The percentage of each generation that is retained in order to repopulate the next generation.


On line 8:

random_select = 0.05

Probability of a random individual being added to a generation in order to promote genetic diversity. 


On line 9:

mutate = 0.001

Probability of individuals in the generation of having random mutations to their set of stocks.


On line 36:

budget = 1147

Total budget amount to buy stocks with.


On line 37:

p_count = 100

The initial population count, this is culled by the retained rate above after each generation and subsequently repopulated.


On line 41:

for i in range(1, 100):

This range is the number of total generations executed.


On line 75:

wb = load_workbook('futureStocks.xlsx')

Finally, this line directs the path to the excel sheet where it gets the stock data, and the futureStocks.xlsx is included in the repository as an example. 

==========================
Additional note:
==========================
To give a better insight into the rapid optimization occurring, this program plots the fitness of each generation and displays this data. Given that the aim is for the fitness to go down in this case, (confusing I know), here is an example of one such run:

![](./Graph.png?raw=true "Graph of average fitness accross generations")


This graph helps to provide insights into the evolution that we might not realize otherwise. For example, we can determine that the efficacy of the solution found bottoms out after fifty or so generations. We can use this information to scale back our number of generations and save on computation time.










