from msilib.schema import Binary
from pulp import *

#------------------------------IMPORT CONSTRAINTS------------------------------
from scripts.constraints import *

#------------------------------IMPORT PARAMETERS------------------------------
import scripts.get_parameters as gp

#------------------------------DEFINE VARIABLES------------------------------
# Utilisation du module get_parameters
inputData = r'xls_file\InputDataEnergySmallInstance.xlsx'
variables = gp.get_variables(inputData)

# Attribution des variables
nb_vertices = variables['nb_vertices']
v_0 = variables['v_0'] #TODO MAYBE ERROR HERE##################################################

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

Total_Fixed_Investment_Cost = lpSum(alpha*c_fix*l[(i-1,j-1)]*X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1))

Total_Variable_Investment_Cost = lpSum((alpha*c_var[(i-1,j-1)]*l[(i-1,j-1)])*P_in[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1))

Total_Investment_Cost = Total_Fixed_Investment_Cost + Total_Variable_Investment_Cost

Total_Heat_Genration_Cost = lpSum(((Tflh*c_heat[v_0])/beta)*P_in[v_0][j] for j  in range(1,nb_vertices+1))

Total_Maintenance_Cost = lpSum((c_om[(i-1,j-1)]*l[(i-1,j-1)])*X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1))

Unmet_Demand_Penalty = lpSum((p_umd[(i-1,j-1)]*D[(i-1,j-1)])*(1 - X[i][j] - X[j][i]) for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1))

Total_Cost = Total_Heat_Genration_Cost + Total_Investment_Cost + Total_Maintenance_Cost + Unmet_Demand_Penalty

Total_Revenue = lpSum(lbd*c_rev[(i-1,j-1)]*D[(i-1,j-1)]*X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1))

Heating_Energy_Network_Optimization_Problem += Total_Cost - Total_Revenue

Heating_Energy_Network_Optimization_Problem += lpSum(X[i][j] for i in range(1,nb_vertices+1) for j  in range(1,nb_vertices+1)) <= nb_vertices - 1

for i in range(1,nb_vertices+1):
    for j in range(1,nb_vertices+1):
        if i != j:
            Heating_Energy_Network_Optimization_Problem += ((X[i][j]-X[j][i]) <= 1)

for i in range(1,nb_vertices+1):
    for j in range(1,nb_vertices+1):
        if i != j:
            delta = d[(i-1,j-1)]*beta*lbd + teta_fix[(i-1,j-1)]*l[(i-1,j-1)]
            eta = 1 - teta_var[(i-1,j-1)]*l[(i-1,j-1)]
            Heating_Energy_Network_Optimization_Problem += eta*P_in[i][j] - P_out[i][j] == delta*X[i][j]



for j in range(1,nb_vertices+1):
    if j != v_0:
        contrainte_4_P_out = []
        contrainte_4_P_in = []
        for i in range(1,nb_vertices+1):
            if i != j :
                contrainte_4_P_out.append(P_out[i][j])
                contrainte_4_P_in.append(P_in[j][i])
        Heating_Energy_Network_Optimization_Problem += lpSum(contrainte_4_P_out[i] for i in range(len(contrainte_4_P_out))) == lpSum(contrainte_4_P_in[i] for i in range(len(contrainte_4_P_out)))

for i in range(1,nb_vertices+1):
    for j in range(1,nb_vertices+1):
        Heating_Energy_Network_Optimization_Problem += (P_in[i][j] <= X[i][j]*C_max[(i-1,j-1)])

contrainte_6 = []

for i in range(1,nb_vertices+1):
    if i != v_0:
        contrainte_6.append(X[i][v_0])
Heating_Energy_Network_Optimization_Problem += (lpSum(contrainte_6[i] for i in range(len(contrainte_6))) == 0)

contrainte_7 = []

for j in range(1,nb_vertices+1):
    if j != v_0:
        contrainte_7.append(P_in[v_0][j])
Heating_Energy_Network_Optimization_Problem += (lpSum(contrainte_7[i] for i in range(len(contrainte_7))) <= Q_max[v_0])


for i in range(1,nb_vertices+1):
    if i != v_0:
        contrainte_8 = []
        for j in range(1,nb_vertices+1):
            if j != i:
                contrainte_8.append(X[j][i])
        Heating_Energy_Network_Optimization_Problem += (lpSum(contrainte_8[i] for i in range(len(contrainte_8))) >= 1)

#------------------------------RESOLUTION-----------------------------------------

Heating_Energy_Network_Optimization_Problem.solve()


