import numpy as np


Probs = np.array([[0,1/3,1/3,1/3],
                 [1/4,0,1/4,1/4,1/4],
                 [1/2,1/2,0,0,0],
                 [1/2,1/2,0,0,0],
                 [0,1,0,0,0]])
nomes_cidades = ['a', 'b', 'c','d', 'e']

cidade = 0
cidades_visitadas = [0,0,0,0,0]
count = 5000

for i in range(count):

    cidades_visitadas[cidade] +=1
    cidade = np.random.choice([0,1,2,3,4,5], 1)