
"""
Source : Dunod Tout-en-un Physique PC, Sanz et al., page 828
"""

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRES DE LA RESOLUTION

x0 = -20    # bornes de l'intervalle
x1 = 320    # d'étude (en m)
X = 10000   # nombre de points de discrétisation
N = 1000    # nombre de composantes de Fourier utilisées dans le calcul

# PARAMETRES DU SYSTEME

omega_0 = 1.5     # pulsation moyenne du paquet d'onde
sigma = 0.15      # ecart type du paquet d'onde gaussien
k0 = (omega_0**2 - 1) **0.5   # pulsation moyenne du paquet d'onde


# RELATIONS DE DISPERSION

def kl(omega) :    # DL1 du module d'onde
    return (k0 + omega_0 / (omega_0 **2-1)**0.5 * (omega - omega_0))

def k(omega) :      # module d'onde sans DL
    return ((omega**2 - 1) **0.5)

def ks(omega) :    # module d'onde sans dispersion
    return (omega)

# CONSTRUCTION DU PAQUET D'ONDE

def amp(omega) :       # amplitude de l'harmonique de pulsation omega
    return (0.01*np.exp(-((omega-omega_0) / sigma) **2) )

x = np.linspace(x0 , x1, X)
def paquetOnde(t):     # construction du paquet d'onde à l'instant t (s)
    PO = np.zeros (X)
    for omega in np.linspace(omega_0-3*sigma, omega_0+3*sigma, N) :
        PO = PO + amp(omega) * np.cos(omega * t - k(omega) * x)
    return (PO)

# REPRESENTATION GRAPHIQUE
t = np.array([0,150,300])

fig, ax = plt.subplots(3, 1, sharex='col')

ax[0].plot(x, paquetOnde(t[0]), '0.2') 
ax[0].axis([x0, x1, -0.7,0.7])
ax[0].legend([r' $t$ = {}'. format (t[0])])

ax[1].plot(x, paquetOnde(t[1]), '0.4') 
ax[1].axis([x0, x1 , -0.7,0.7])
ax[1].legend([r' $t$ = {}'.format(t[1])])

ax[2].plot(x, paquetOnde (t[2]), '0.6') 
ax[2].axis([x0, x1 , -0.7,0.7])
ax[2].legend([r' $t$ = {}'. format (t[2])])

ax[2].set_xlabel(r'$x$') #nom de l'axe x, taille de la police
plt.tight_layout ()
plt.show ()