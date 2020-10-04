import numpy as np
import random
import copy as cp

population_size = 400
crossover_rate = 0.9
mutation_rate = 0.4
num_queens = 64

def checkLeft (positions, init):
    conflict = 0
    i = init-1
    if i < 0:
        return 0
    cresc, decr = positions[init]+1, positions[init]-1
    while i >=0:
        if(positions[i] == cresc):
            conflict+=1
        if(positions[i] == decr):
            conflict+=1
        i -= 1
        decr -= 1
        cresc += 1
    return conflict

def checkRight (positions, init):
    conflict = 0
    i = init+1
    if i >= num_queens:
        return 0
    cresc, decr = positions[init]+1, positions[init]-1
    while i < num_queens:
        if(positions[i] == cresc):
            conflict+=1
        if(positions[i] == decr):
            conflict+=1
        i += 1
        decr -= 1
        cresc += 1
    return conflict

class individuo:
    def __init__(self, gen = None):
        if gen is not None:
            self.genotipo = gen
        else:
            self.genotipo = np.random.permutation(num_queens)
        self.fit = self.calculateFitness()

    def __str__(self):
        bin_genotipo = ''
        for gene in self.genotipo:
            bin_genotipo = bin_genotipo + str(format(gene, '03b'))+' '
        return 'Genótipo: %s\nFitness:  %s\n\n' % (bin_genotipo, self.fit)  

    def calculateFitness(self):
        conflict = 0
        for i in range(num_queens):
            conflict+= checkLeft(self.genotipo, i)
            conflict+= checkRight(self.genotipo, i)
        return int(conflict/2)

def genPopulation(pop, pop_size):
    for i in range(pop_size):
        pop.append(individuo())
    return pop

#cut-and-crossfill crossover
def recombinacao(mae1, mae2):
    corte_idx = random.randint(1, (num_queens - 2))

    gen1 = np.append(mae1.genotipo[:corte_idx], mae2.genotipo[corte_idx:])
    gen2 = np.append(mae2.genotipo[:corte_idx], mae1.genotipo[corte_idx:])

    gen1 = list(dict.fromkeys(np.append(list(dict.fromkeys(gen1)), mae2.genotipo[:corte_idx])))
    gen2 = list(dict.fromkeys(np.append(list(dict.fromkeys(gen2)), mae1.genotipo[:corte_idx])))

    gen1 = gen1[:len(mae2.genotipo)]
    gen2 = gen2[:len(mae1.genotipo)]

    filho1 = individuo(gen1)
    filho2 = individuo(gen2)
    
    selecao_sobreviventes(filho1)
    selecao_sobreviventes(filho2)

#survival selection replace worst
def selecao_sobreviventes(individuo):
    pior_indv = max(pop, key=lambda x: x.fit)

    if(individuo.fit < pior_indv.fit):
        pop.remove(pior_indv)
        pop.append(individuo)

#parent selection: tourney and
def selecao_pais(tipo = "torneio"):
    if (tipo == "torneio"):
        maes = np.random.choice(pop, 5)
        maes = sorted(maes, key=lambda x: x.fit, reverse=False)
        return maes[0], maes[1]
    else:
        new_pop = pop.copy()
        for i in range(len(pop)):
            new_pop += (len(pop)-i-1) * [pop[i]]
        maes = np.random.choice(new_pop, 2)
        del new_pop
        return maes[0], maes[1]
    
def mutation(individuo):
    positions = individuo.genotipo
    ar = np.random.choice(np.arange(num_queens), 2, replace = False)
    positions[ar[1]], positions[ar[0]] = positions[ar[0]], positions[ar[1]]
    individuo.calculateFitness()

pop = []
pop = genPopulation(pop, population_size)


def main(tipo_selecao):
    fit_count = population_size
    gen = 0
    solution = pop[0]# ind qualquer
    while (solution.fit > 0 and fit_count <10000):# cada geracao
        solution = min(pop, key=lambda x: x.fit)
        gen+=1
        print("\ngen: ", gen)
        print("\nSolution: ",solution.fit, "\nfit_count: ",fit_count)
        chance = random.random()

        if chance <= crossover_rate:
            mae1,mae2 = selecao_pais(tipo_selecao)
            recombinacao(mae1,mae2)
            fit_count+=2

        if chance <= mutation_rate:
            mutation(pop[random.randint(0,population_size-1)])
            fit_count+=1
            

    print("gen: ", gen)
    print(str(solution))

main('torneio')
#a = individuo()

# print(str(a))