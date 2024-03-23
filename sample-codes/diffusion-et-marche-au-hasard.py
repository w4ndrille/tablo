
"""
Source : Dunod Tout-en-un Physique PC, Sanz et al., page 102
"""

import numpy as np 
import matplotlib. pyplot as plt
## Fonction
def marche (n,N) :
    x = np. zeros ((n,N), dtype = int)
    for i in range (n-1):
        x[i+1] = x[i] + np. random. choice ([- 1,1],N)
    return x

##Paramètres
N = 10000 #nombre de particules
n = 1001 #nombre de pas de temps

##Simulation de la marche
x = marche (n, N)

##Histogrammes à différents instants de la marche 
# liste des instants à représenter
t = [110,50,100,500, 10001]
p = len (t)

fig, ax = plt.subplots(1,p, sharey = 'row', figsize =(13,3)) #p graphes sur 1 ligne

for i in range (p):
    ax[i].hist(x[t[i]], (max(x[t[i]]) - min(x[t[i]]))//2,
     density = True, label = r'$t=${:)'.format(t[i]), color = 'k')
    ax[i].set_label('$x$')
    ax[i].grid(ls = '--')
    ax[i].legend()


ax[0].set_ylabel('densité')
plt.tight_layout()
plt.show()
plt.savefig('Histo eps', format=' eps', dpi=1200)
##Position moyenne et variance en fonction du temps

ò