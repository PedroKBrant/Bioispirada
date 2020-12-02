import numpy
import pickle
import matplotlib.pyplot as plt
import statistics as st

# for i in range(10):
#     f = open("ackley_" + str(i), "rb")
#     g = open("ackley_ag_" + str(i), "rb")
#
#     best_fit1, fit_med1, time_array1, gen1, solution1 = pickle.Unpickler(f).load()
#     best_fit2, fit_med2, time_array2, gen2, solution2 = pickle.Unpickler(g).load()
#     # line 1 points
#     # plotting the line 1 points
#     plt.plot(time_array1, best_fit1, label = "Estratégia Evolutiva")
#     plt.plot(time_array2, best_fit2, label = "Algoritmo Genético")
#     # line 2 points
#     # plotting the line 2 points
#     plt.yscale('log')
#     plt.xlabel('Time (s)')
#     # Set the y axis label of the current axis.
#     plt.ylabel('f(X)')
#     # Set a title of the current axes.
#     plt.title('Ackley - Melhor solução - Execução ' + str(i))
#     # show a legend on the plot
#     plt.legend()
#     # Display a figure.
#     plt.show()
#
#     f.close()
#     g.close()


solutions_ag = []
solutions_ee = []
med_ag = []
med_ee = []
for i in range(10):
    f = open("ackley_" + str(i), "rb")
    g = open("ackley_ag_" + str(i), "rb")

    best_fit1, fit_med1, time_array1, gen1, solution1 = pickle.Unpickler(f).load()
    best_fit2, fit_med2, time_array2, gen2, solution2 = pickle.Unpickler(g).load()
    solutions_ee.append(solution1)
    solutions_ag.append(solution2)
    med_ee.append(fit_med1[-1])
    med_ag.append(fit_med2[-1])
    f.close()
    g.close()

ee_best_avg = sum(solutions_ee)/10
ee_best_var = st.stdev(solutions_ee)

ag_best_avg = sum(solutions_ag)/10
ag_best_var = st.stdev(solutions_ag)

ee_medio_avg = sum(med_ee)/10
ee_medio_var = st.stdev(med_ee)

ag_medio_avg = sum(med_ag)/10
ag_medio_var =st.stdev(med_ag)

print('EE 10 execuções: ')
print(f'Fitness médio: {ee_medio_avg} (+/- {ee_medio_var})')
print(f'Melhor fitness: {ee_best_avg} (+/- {ee_best_var})')
print('\n\n')
print('AG 10 execuções: ')
print("%s: %f (+/- %f)" % ("Fitness médio", ag_medio_avg, ag_medio_var))
print("%s: %f (+/- %f)" % ("Melhor fitness", ag_best_avg, ag_best_var))
