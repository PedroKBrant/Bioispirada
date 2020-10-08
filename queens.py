import numpy as np
import random
import copy as cp
import webbrowser
import statistics as st
import io

population_size = 100
crossover_rate = 0.9
mutation_rate = 0.4
num_queens = 8

def board_to_fen(board):
    # Use StringIO to build string more efficiently than concatenating
    with io.StringIO() as s:
        for row in board:
            empty = 0
            for cell in row:
                c = cell[0]
                if c in ('w', 'b'):
                    if empty > 0:
                        s.write(str(empty))
                        empty = 0
                    s.write(cell[1].upper() if c == 'w' else cell[1].lower())
                else:
                    empty += 1
            if empty > 0:
                s.write(str(empty))
            s.write('/')
        # Move one position back to overwrite last '/'
        s.seek(s.tell() - 1)
        # If you do not have the additional information choose what to put
        s.write(' w KQkq - 0 1')
        return s.getvalue()

def gen_board(positions):
    board =  [
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
    ['em', 'em', 'em', 'em', 'em', 'em', 'em', 'em'],
]
    for i in range(len(positions)):
        board[positions[i]][i] = 'bq'
    return board


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
def recombinacao(mae1, mae2, tipo = "geracional"):
    corte_idx = random.randint(1, (num_queens - 2))

    gen1 = np.append(mae1.genotipo[:corte_idx], mae2.genotipo[corte_idx:])
    gen2 = np.append(mae2.genotipo[:corte_idx], mae1.genotipo[corte_idx:])

    gen1 = list(dict.fromkeys(np.append(list(dict.fromkeys(gen1)), mae2.genotipo[:corte_idx])))
    gen2 = list(dict.fromkeys(np.append(list(dict.fromkeys(gen2)), mae1.genotipo[:corte_idx])))

    gen1 = gen1[:len(mae2.genotipo)]
    gen2 = gen2[:len(mae1.genotipo)]

    filho1 = individuo(gen1)
    filho2 = individuo(gen2)
    
    if tipo == "geracional":
        #maes_filhos = [filho1, filho2, mae1, mae2]
        selecao_geracional(filho1, filho2, mae1, mae2)
    else:
        selecao_sobreviventes(filho1)
        selecao_sobreviventes(filho2)



#survival selection replace worst
def selecao_sobreviventes(individuo):
    pior_indv = max(pop, key=lambda x: x.fit)

    if(individuo.fit < pior_indv.fit):
        pop.remove(pior_indv)
        pop.append(individuo)

#survival selection generation
def selecao_geracional(filho1, filho2, mae1, mae2):

    if mae1 in pop:
        pop.remove(mae1)
    if mae2 in pop:
        pop.remove(mae2)
 
    individuos= [filho1, filho2, mae1, mae2]
    melhores_indv = sorted(individuos, key=lambda x: x.fit, reverse=False)

    pop.append(melhores_indv[1])
    pop.append(melhores_indv[0])

#parent selection: tourney and
def selecao_pais(tipo = "torneio"):
    if (tipo == "torneio"):
        maes = np.random.choice(pop, 5, replace=False)
        maes = sorted(maes, key=lambda x: x.fit, reverse=False)
        return maes[0], maes[1]
    else:
        sumFitness = sum(ind.fit for ind in pop)
        p_list = [x.fit/sumFitness for x in pop]
        maes = np.random.choice(pop, 2, p = p_list, replace=False)
        return maes[0], maes[1]
    
def mutation(individuo):
    positions = individuo.genotipo
    ar = np.random.choice(np.arange(num_queens), 2, replace = False)
    positions[ar[1]], positions[ar[0]] = positions[ar[0]], positions[ar[1]]
    individuo.calculateFitness()

pop = []
pop = genPopulation(pop, population_size)


def main(tipo_selecao, tipo_sobrevivencia, so):
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
            recombinacao(mae1,mae2, tipo_sobrevivencia)
            fit_count+=2

        if chance <= mutation_rate:
            mutation(pop[random.randint(0,population_size-1)])
            fit_count+=1
            
    return gen, tipo_selecao, tipo_sobrevivencia

    print("gen: ", gen)
    print('len pop',len(pop))
    print(str(solution))
    print(board_to_fen(gen_board(solution.genotipo)))
    if so == "linux":
        path = '/usr/bin/google-chrome'
    else:
        path = "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
    url = 'https://lichess.org/editor/' + board_to_fen(gen_board(solution.genotipo))
    webbrowser.register('chrome',
    None,
    webbrowser.BackgroundBrowser(path))
    webbrowser.get('chrome').open(url)

# Para cada implementação devem ser feitas 30 execuções e analisar
#     • Em quantas execuções o algoritmo convergiu (no/30 execuções);
#     • Em que iteração o algoritmo convergiu (média e desvio padrão);
#     • Número de indivíduos que convergiram por execução;
#     • Fitness médio alcançado nas 30 execuções (média e desvio padrão);
#     • Análise adicional: Quantas iterações são necessárias para toda a população convergir?

vet_gens = []
vet_convergencias = []
vet_pop_fit = []
vet_pop_gen = []
total_convergiu = 0

def avaliacao(total_convergiu, gen, i):
    convergiu = 0
    vet_gens.append(gen)
    for ind in pop:
        vet_pop_fit.append(ind.fit)
        vet_pop_gen.append(ind.genotipo)
        if ind.fit == 0:
            convergiu+=1 
    vet_convergencias.append(convergiu)
    if convergiu != 0:
        total_convergiu+=1
    print(".\n")
    if i == 29:
        print("===================================================")
        print("\nTipo Selecao :",tipo_selecao)
        print("\nTipo Sobrevivencia :",tipo_sobrevivencia)
        print("\nPopulation Size : ",population_size)
        print("\nCrossover Rate : ",crossover_rate)
        print("\nMutation Size : ",mutation_rate)
        print("\n1 - Total de vezes que convergiu: ", total_convergiu)
        
        print ("\n2 - Média de Iterações: ",st.mean(vet_gens))
        print ("\nVariância de Iterações: ",st.variance(vet_gens))
        print("\n3 - Número de indivíduos que convergiram por execução: ")
        for iten in vet_convergencias:print(iten)
        print ("\n4 - Média do Fitness: ",st.mean(vet_pop_fit))
        print ("\nVariância do Fitness: ",st.variance(vet_pop_fit))
        print("===================================================")
    return total_convergiu 

for i in range(30):
    gen, tipo_selecao, tipo_sobrevivencia = main('torneio', 'geracional','linux')
    total_convergiu = avaliacao(total_convergiu, gen, i)
#a = individuo()

# print(str(a))