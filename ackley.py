import numpy as np
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
import random
import copy as cp
import webbrowser
import statistics as st
import io

population_size = 40
pressao = 4
crossover_rate = 0.9
mutation_rate = 0.4
gen_size = 30
C = 0.9

class individuo:

    def __init__(self, gen = None):
        self.sigma = random.uniform(0, 1)
        if gen is not None:
            self.genotipo = gen
        else:
            self.genotipo = np.array([(random.uniform(-15, 15))
                      for _ in range(gen_size)])
        self.fit = self.calculateFitness()

    def __str__(self):
        return 'Genótipo: %s\nSigma: %s\nFitness:  %s\n\n' % (self.genotipo, self.sigma, self.fit)

    def ackley(self, x, a=20, b=0.2, c=2 * pi):
        x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
        n = len(x)
        s1 = sum(x**2)
        s2 = sum(cos(c * x))
        return -a * exp(-b * sqrt(s1 / n)) - exp(s2 / n) + a + exp(1)

    def calculateFitness(self):
        return self.ackley(self.genotipo)

def generatePopulation(pop, pop_size):
    for _ in range(pop_size):
        pop.append(individuo())
    return pop

def mutation(individuo):
    aux_genotipo = np.copy(individuo.genotipo)
    fit = individuo.fit
    success = 0
    for i in range(gen_size):
        aux_gen = individuo.genotipo[i]
        individuo.genotipo[i] += random.normalvariate(0, individuo.sigma)
        if (individuo.genotipo[i] > 15): individuo.genotipo[i] = 15
        elif (individuo.genotipo[i] < -15): individuo.genotipo[i] = -15
        new_fit = individuo.calculateFitness()
        if new_fit < fit:
            aux_genotipo[i]=individuo.genotipo[i]
            success+=1
        individuo.genotipo[i] = aux_gen
    individuo.genotipo = aux_genotipo
    individuo.fit = individuo.calculateFitness()
    Ps = 0.2 * gen_size
    if success > Ps:
        individuo.sigma = individuo.sigma/C
    elif success < Ps:
        individuo.sigma = individuo.sigma*C
    return

def recombinacao(population):
    pais = np.random.choice(population, 10, replace=False)
    pais = sorted(pais, key=lambda x: x.fit, reverse=False)[0:2]
    aux_gen = np.copy(pais[1].genotipo)
    for i in range(gen_size):
        aux_gen[i] = (pais[0].genotipo[i] + pais[1].genotipo[i])/2
        # if bool(random.getrandbits(1)):
        #     aux_gen[i] = pais[0].genotipo[i]
        # else:
        #     aux_gen[i] = pais[1].genotipo[i]
    child = individuo(aux_gen)
    child.sigma = (pais[0].sigma+pais[1].sigma)/2
    return child

def selecao_sobreviventes(children, pop):
    sort = sorted(children + pop, key=lambda x: x.fit, reverse=False)
    return sort[0:population_size]









# def mutation(individuo):
#     # SWAP two random gens
#     positions = individuo.genotipo
#     ar = np.random.choice(np.arange(gen_size), 2, replace = False)
#     positions[ar[1]], positions[ar[0]] = positions[ar[0]], positions[ar[1]]
#     individuo.calculateFitness()

# #cut-and-crossfill crossover
# def recombinacao(mae1, mae2, tipo = "geracional"):
#     corte_idx = random.randint(1, (gen_size - 2))

#     gen1 = np.append(mae1.genotipo[:corte_idx], mae2.genotipo[corte_idx:])
#     gen2 = np.append(mae2.genotipo[:corte_idx], mae1.genotipo[corte_idx:])

#     gen1 = list(dict.fromkeys(np.append(list(dict.fromkeys(gen1)), mae2.genotipo[:corte_idx])))
#     gen2 = list(dict.fromkeys(np.append(list(dict.fromkeys(gen2)), mae1.genotipo[:corte_idx])))

#     gen1 = gen1[:len(mae2.genotipo)]
#     gen2 = gen2[:len(mae1.genotipo)]

#     filho1 = individuo(gen1)
#     filho2 = individuo(gen2)

#     if tipo == "geracional":
#         #maes_filhos = [filho1, filho2, mae1, mae2]
#         selecao_geracional(filho1, filho2, mae1, mae2)
#     else:
#         selecao_sobreviventes(filho1)
#         selecao_sobreviventes(filho2)


# #survival selection replace worst
# def selecao_sobreviventes(individuo):
#     pior_indv = max(pop, key=lambda x: x.fit)

#     if(individuo.fit < pior_indv.fit):
#         pop.remove(pior_indv)
#         pop.append(individuo)

# #survival selection generation
# def selecao_geracional(filho1, filho2, mae1, mae2):

#     if mae1 in pop:
#         pop.remove(mae1)
#     if mae2 in pop:
#         pop.remove(mae2)

#     individuos= [filho1, filho2, mae1, mae2]
#     melhores_indv = sorted(individuos, key=lambda x: x.fit, reverse=False)

#     pop.append(melhores_indv[1])
#     pop.append(melhores_indv[0])

# #parent selection: tourney and
# def selecao_pais(tipo = "torneio"):
#     if (tipo == "torneio"):
#         maes = np.random.choice(pop, 5, replace=False)
#         maes = sorted(maes, key=lambda x: x.fit, reverse=False)
#         return maes[0], maes[1]
#     else:
#         sumFitness = sum(ind.fit for ind in pop)
#         p_list = [x.fit/sumFitness for x in pop]
#         maes = np.random.choice(pop, 2, p = p_list, replace=False)
#         return maes[0], maes[1]

pop = []
pop = generatePopulation(pop, population_size)


def main(pop):
    gen = 0
    solution = pop[0]# ind qualquer
    while (solution.fit > 0 and gen <10000):# cada geracao
        new_pop = []
        for _ in range(population_size*pressao):
            new_child = recombinacao(pop)
            mutation(new_child)
            new_pop.append(new_child)
        pop = selecao_sobreviventes(new_pop, [])
        solution = min(pop, key=lambda x: x.fit)
        gen+=1
        print("\ngen: ", gen)
        print("\nSolution: ", solution.fit)
    return solution, gen, pop

solution, gen, pop = main(pop)


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
# mutation(a)
# print(str(a))
