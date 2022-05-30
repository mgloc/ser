from msilib.schema import Binary
from pulp import *

#------------------------------IMPORT CONSTRAINTS------------------------------
from scripts.constraints import *

#------------------------------IMPORT PARAMETERS------------------------------
import scripts.get_parameters as gp

#------------------------------DEFINE VARIABLES------------------------------
# Utilisation du module get_parameters
inputData = r'xls_tests\InputDataExample.xlsx'
variables = gp.get_variables(inputData)

# Attribution des variables
nb_vertices = variables['nb_vertices']
v_0 = variables['v_0']

c_fix    = variables['c_fix']
c_var    = variables['c_var']
c_om     = variables['c_om']
c_heat   = variables['c_heat']
c_rev    = variables['c_rev']
p_umd    = variables['p_umd']
alpha    = variables['alpha']
teta_fix = variables['teta_fix']
teta_var = variables['teta_var']
Tflh     = variables['Tflhc_fix']
beta     = variables['beta']
lbd      = variables['lbd']
l        = variables['l']
d        = variables['d']
D        = variables['D']
C_max    = variables['C_max']
Q_max    = variables['Q_max']

L = [range(0,nb_vertices)]
X = LpVariable('X', [L, L], cat='Binary')
P_in = LpVariable('P_in', [L, L], lowbound = 0, cat='Continuous')
P_out = LpVariable('P_out', [L, L], lowbound = 0, cat='Continuous')

#------------------------------CONTRAINTES & PROBLEME------------------------------

Heating_Energy_Network_Optimization_Problem = LpProblem("Heating_Energy_Network_Optimization_Problem", LpMinimize)
Heating_Energy_Network_Optimization_Problem += total_expense(c_rev, D, lbd, X, Tflh, c_heat, beta, P_in, c_om, l, p_umd, c_fix, alpha, c_var, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_1(X, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_2(X, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_3(teta_var, teta_fix, l, lbd, beta, d, P_in, P_out, X, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_4(P_in, P_out, v_0, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_5(P_in, X, C_max, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_6(X, v_0, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_7(P_in, Q_max, v_0, nb_vertices)
Heating_Energy_Network_Optimization_Problem += contrainte_8(X, v_0, nb_vertices)
Heating_Energy_Network_Optimization_Problem.solve()


