import numpy as np
import random
import copy as cp



population_size = 400
crossover_rate = 0.9
mutation_rate = 0.4
num_queens = 8
bin_size =  int(np.log2(num_queens))

def binToNumber(bin):
    return int(bin.dot(1 << np.arange(bin.size)[::-1]))

def binToArray(bin):
    count = 0
    array = np.zeros(num_queens, np.int32)
    for i in range(num_queens):
        array[i] = binToNumber(bin[count : count+bin_size])
        count+=bin_size
    return array

# def numberToBin(number):
#     bin = np.frombuffer(np.binary_repr(number).encode(), 'u1') - ord('0')
#     result = np.zeros(arraySize, dtype = np.uint8)
#     result[arraySize - bin.shape[0]:] = bin
#     return result

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
            self.genotipo = np.random.randint(2, size = bin_size * num_queens)
        self.fit = self.calculateFitness()

    def __str__(self):
        bin_genotipo = ''
        array_repr = binToArray(self.genotipo)
        for gene in array_repr:
            bin_genotipo = bin_genotipo + str(format(gene, f'0{bin_size}b'))+' '
        return 'Genótipo: %s\nFitness:  %s\n\n' % (bin_genotipo, self.fit)

    def calculateFitness(self):
        conflict = 0
        array_repr = binToArray(self.genotipo)
        for i in range(num_queens):
            conflict+= checkLeft(array_repr, i)
            conflict+= checkRight(array_repr, i)
        conflict = conflict/2
        unique = np.unique(array_repr).size
        conflict += num_queens-unique
        return conflict

def genPopulation(pop, pop_size):
    for i in range(pop_size):
        pop.append(individuo())
    return pop

#cut-and-crossfill crossover
def recombinacao(mae1, mae2):
    corte_idx = random.randint(1, (num_queens*bin_size) - 2)

    gen1 = np.append(mae1.genotipo[:corte_idx], mae2.genotipo[corte_idx:])
    gen2 = np.append(mae2.genotipo[:corte_idx], mae1.genotipo[corte_idx:])

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
    genes = individuo.genotipo
    troca = random.randint(0, (num_queens*bin_size)-1)
    genes[troca] = (genes[troca]+1)%2
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
