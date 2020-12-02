import numpy as np
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
import random
import copy as cp
import webbrowser
import statistics as st
import io
import time
import pickle

population_size = 100
crossover_rate = 0.9
mutation_rate = 0.6
gen_size = 30
global fit_count
fit_count = 0

class individuo:

    def __init__(self, gen = None):
        if gen is not None:
            self.genotipo = gen
        else:
            self.genotipo = np.array([(random.uniform(-15, 15))
                      for _ in range(gen_size)])
        self.fit = self.calculateFitness()

    def __str__(self):
        return 'Genótipo: %s\nFitness:  %s\n\n' % (self.genotipo, self.fit)

    def __repr__(self):
        return 'Genótipo: %s\nFitness:  %s\n\n' % (self.genotipo, self.fit)

    def ackley(self, x, a=20, b=0.2, c=2 * pi):
        x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
        n = len(x)
        s1 = sum(x**2)
        s2 = sum(cos(c * x))
        return -a * exp(-b * sqrt(s1 / n)) - exp(s2 / n) + a + exp(1)

    def calculateFitness(self):
        self.fit = self.ackley(self.genotipo)
        global fit_count
        fit_count+=1
        return self.fit

def generatePopulation(pop_size):
    global pop
    for _ in range(pop_size):
        pop.append(individuo())
    return pop

def mutation(individuo):
    #modify a random gen to a random value
    individuo.genotipo[random.randint(0,gen_size-1)] = random.uniform(-15, 15)
    individuo.calculateFitness()


# def mutation_2(individuo):
#     ar = np.random.choice(np.arange(gen_size), 1, replace = False)

# #cut-and-crossfill crossover
def recombinacao(mae1, mae2, tipo = "geracional"):
    corte_idx = random.randint(1, (gen_size - 2))

    gen1 = np.append(mae1.genotipo[:corte_idx], mae2.genotipo[corte_idx:])
    gen2 = np.append(mae2.genotipo[:corte_idx], mae1.genotipo[corte_idx:])

    filho1 = individuo(gen1)
    filho2 = individuo(gen2)

    if tipo == "geracional":
        #maes_filhos = [filho1, filho2, mae1, mae2]
        selecao_geracional(filho1, filho2, mae1, mae2)
    else:
        selecao_sobreviventes(filho1)
        selecao_sobreviventes(filho2)


# #survival selection replace worst
def selecao_sobreviventes(individuo):
    pior_indv = max(pop, key=lambda x: x.fit)

    if(individuo.fit < pior_indv.fit):
        pop.remove(pior_indv)
        pop.append(individuo)

# #survival selection generation
def selecao_geracional(filho1, filho2, mae1, mae2):
    global pop
    if mae1 in pop:
        pop.remove(mae1)
    if mae2 in pop:
        pop.remove(mae2)

    individuos= [filho1, filho2, mae1, mae2]
    melhores_indv = sorted(individuos, key=lambda x: x.fit, reverse=False)

    pop.append(melhores_indv[1])
    pop.append(melhores_indv[0])

# #parent selection: tourney and
def selecao_pais(tipo = "torneio"):
    global pop
    if (tipo == "torneio"):
        maes = np.random.choice(pop, 5, replace=False)
        maes = sorted(maes, key=lambda x: x.fit, reverse=False)
        return maes[0], maes[1]
    else:
        sumFitness = sum(ind.fit for ind in pop)
        p_list = [x.fit/sumFitness for x in pop]
        maes = np.random.choice(pop, 2, p = p_list, replace=False)
        return maes[0], maes[1]

def main(tipo_selecao, tipo_sobrevivencia):
    global pop
    time_array = []
    fit_med = []
    best_fit = []
    gen = 0
    solution = pop[0]# ind qualquer
    time_0 = time.time()
    time_1 = time_0
    while (time_1-time_0 < 60):# cada geracao
        chance = random.random()

        if chance <= crossover_rate:
            mae1,mae2 = selecao_pais(tipo_selecao)
            recombinacao(mae1,mae2, tipo_sobrevivencia)

        if chance <= mutation_rate:
            mutation(pop[random.randint(0,population_size-1)])
        time_current = time.time()

        solutions = [x.fit for x in pop]
        med = sum(solutions)/population_size
        solution = min(solutions)
        gen+=1
        print("\ngen: ", gen)
        print("\nSolution: ",solution, "\nfit_count: ",fit_count)

        if gen==1 or time_current-time_1 >= 0.1:
            time_1 = time.time()
            time_array.append(time_1-time_0)
            fit_med.append(med)
            best_fit.append(solution)


    return best_fit, fit_med, time_array, gen, solution

global pop
pop = []
for i in range(10):
    pop = []
    pop = generatePopulation(population_size)
    ret = main('torneio', 'aa')
    with open("ackley_ag_" + str(i), "wb") as f:
        pickle.Pickler(f).dump(ret)
#     print("gen: ", gen)
#     print('len pop',len(pop))
#     print(str(solution))

# # Para cada implementação devem ser feitas 30 execuções e analisar
# #     • Em quantas execuções o algoritmo convergiu (no/30 execuções);
# #     • Em que iteração o algoritmo convergiu (média e desvio padrão);
# #     • Número de indivíduos que convergiram por execução;
# #     • Fitness médio alcançado nas 30 execuções (média e desvio padrão);
# #     • Análise adicional: Quantas iterações são necessárias para toda a população convergir?

# vet_gens = []
# vet_convergencias = []
# vet_pop_fit = []
# vet_pop_gen = []
# total_convergiu = 0

# def avaliacao(total_convergiu, gen, i):
#     convergiu = 0
#     vet_gens.append(gen)
#     for ind in pop:
#         vet_pop_fit.append(ind.fit)
#         vet_pop_gen.append(ind.genotipo)
#         if ind.fit == 0:
#             convergiu+=1
#     vet_convergencias.append(convergiu)
#     if convergiu != 0:
#         total_convergiu+=1
#     print(".\n")
#     if i == 29:
#         print("===================================================")
#         print("\nTipo Selecao :",tipo_selecao)
#         print("\nTipo Sobrevivencia :",tipo_sobrevivencia)
#         print("\nPopulation Size : ",population_size)
#         print("\nCrossover Rate : ",crossover_rate)
#         print("\nMutation Size : ",mutation_rate)
#         print("\n1 - Total de vezes que convergiu: ", total_convergiu)

#         print ("\n2 - Média de Iterações: ",st.mean(vet_gens))
#         print ("\nVariância de Iterações: ",st.variance(vet_gens))
#         print("\n3 - Número de indivíduos que convergiram por execução: ")
#         for iten in vet_convergencias:print(iten)
#         print ("\n4 - Média do Fitness: ",st.mean(vet_pop_fit))
#         print ("\nVariância do Fitness: ",st.variance(vet_pop_fit))
#         print("===================================================")
#     return total_convergiu

# for i in range(30):
#     gen, tipo_selecao, tipo_sobrevivencia = main('torneio', 'geracional')
#     total_convergiu = avaliacao(total_convergiu, gen, i)

# a = individuo()
# print(str(a))
# mutation_1(a)
# print(str(a))
