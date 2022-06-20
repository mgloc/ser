from msilib.schema import Binary
from pulp import *

#------------------------------IMPORT PARAMETERS------------------------------
import scripts.get_parameters as gp

#------------------------------DEFINE VARIABLES------------------------------
# Utilisation du module get_parameters
inputData = r'content\InputDataEnergySmallInstance.xlsx'
variables = gp.get_variables(inputData)

# Attribution des variables
nb_vertices = variables['nb_vertices']
v_0 = variables['v_0']#TODO MAYBE ERROR HERE##################################################

c_fix    = variables['c_fix']
c_var    = variables['c_var']
c_om     = variables['c_om']
c_heat   = variables['c_heat']
c_rev    = variables['c_rev']
p_umd    = variables['p_umd']
alpha    = variables['alpha']
teta_fix = variables['teta_fix']
teta_var = variables['teta_var']
Tflh     = variables['Tflh']
beta     = variables['beta']
lbd      = variables['lbd']
l        = variables['l']
d        = variables['d']
D        = variables['D']
C_max    = variables['C_max']
Q_max    = variables['Q_max']

print("################# VARIABLES ###################")
for key,var in variables.items() :
    print("---")
    print(f"{key} : {var}")
print("################# VARIABLES END ###############")

L = [i for i in range(1,nb_vertices+1)]
print(L)
X = LpVariable.dicts('X', (L, L), cat='Binary')
P_in = LpVariable.dicts('P_in', (L, L), lowBound = 0)
P_out = LpVariable.dicts('P_out', (L, L), lowBound = 0)
print(X)

#------------------------------CONTRAINTES & PROBLEME------------------------------

Heating_Energy_Network_Optimization_Problem = LpProblem("Heating_Energy_Network_Optimization_Problem", LpMinimize)

Total_Fixed_Investment_Cost = lpSum(alpha*c_fix*l[(i,j)]*X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1) if (i!=j))

Total_Variable_Investment_Cost = lpSum((alpha*c_var[(i,j)]*l[(i,j)])*P_in[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1) if (i!=j))

Total_Investment_Cost = Total_Fixed_Investment_Cost + Total_Variable_Investment_Cost

Total_Heat_Genration_Cost = lpSum(((Tflh*c_heat[v_0])/beta)*P_in[v_0][j] for j  in range(1,nb_vertices+1) if (j != v_0))

Total_Maintenance_Cost = lpSum((c_om[(i,j)]*l[(i,j)])*X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1) if (i!=j))

Unmet_Demand_Penalty = lpSum(0.5*(p_umd[(i,j)]*D[(i,j)])*(1 - X[i][j] - X[j][i]) for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1) if (i != j))

Total_Cost = Total_Heat_Genration_Cost + Total_Investment_Cost + Total_Maintenance_Cost + Unmet_Demand_Penalty

Total_Revenue = lpSum(lbd*c_rev[(i,j)]*D[(i,j)]*X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1) if (i!=j))

Z = Total_Cost - Total_Revenue

Heating_Energy_Network_Optimization_Problem += Z

Heating_Energy_Network_Optimization_Problem += (lpSum(X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1)) == nb_vertices - 1)

for i in range(1,nb_vertices+1):
    for j in range(1,nb_vertices+1):
        if i != j:
            Heating_Energy_Network_Optimization_Problem += ((X[i][j] + X[j][i]) <= 1)

for i in range(1,nb_vertices+1):
    for j in range(1,nb_vertices+1):
        if i != j:
            delta = d[(i,j)]*beta*lbd + teta_fix[(i,j)]*l[(i,j)]
            eta = 1 - teta_var[(i,j)]*l[(i,j)]
            Heating_Energy_Network_Optimization_Problem += (eta*P_in[i][j] - P_out[i][j] == delta*X[i][j])

for j in range(1,nb_vertices+1):
    if j != v_0:
        Heating_Energy_Network_Optimization_Problem += lpSum(P_out[i][j] for i in range(1,nb_vertices+1) if (i!=j)) == lpSum(P_in[j][i] for i in range(1,nb_vertices+1) if (i!=j))

for i in range(1,nb_vertices+1):
    for j in range(1,nb_vertices+1):
        Heating_Energy_Network_Optimization_Problem += (P_in[i][j] <= X[i][j]*C_max[(i,j)])

Heating_Energy_Network_Optimization_Problem += (lpSum(X[i][v_0] for i in range(1,nb_vertices +1) if (i != v_0)) == 0)

Heating_Energy_Network_Optimization_Problem += (lpSum(P_in[v_0][j] for j in range(1,nb_vertices +1) if (j != v_0)) <= Q_max[v_0])

for i in range(1,nb_vertices+1):
    if i != v_0:
        Heating_Energy_Network_Optimization_Problem += (lpSum(X[j][i] for j in range(1,nb_vertices+1) if (j != i)) >= 1)

#------------------------------RESOLUTION-----------------------------------------

Heating_Energy_Network_Optimization_Problem.solve()

for v in Heating_Energy_Network_Optimization_Problem.variables() :
    print(v.name," = ",v.varValue)
