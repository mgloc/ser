from msilib.schema import Binary
import numpy as np
from pulp import *
import pandas as pd
from itertools import combinations
import math as mt

# fonction prédéfinies

def total_fixed_investment_cost(c_fix, l, alpha, X, nb_vertices):
    S = 0
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            S += (alpha*c_fix[(i,j)]*l[(i,j)])*X[(i,j)]
    return S

def total_variable_investment_cost(c_var, l, alpha, P_in, nb_vertices):
    S = 0
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            S += (alpha*c_var[(i,j)]*l[(i,j)])*P_in[(i,j)]
    return S

def total_heat_generation_cost( Tflh, c_heat, beta, P_in, v_0, nb_vertices):
    S = 0
    for j in range(nb_vertices):
        S += ((Tflh*c_heat[v_0])/beta)*P_in[(v_0,j)]
    return S

def total_maintenance_cost(c_om, l, X, nb_vertices):
    S(i,j)
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            S += (c_om[(i,j)]*l[(i,j)])*X[(i,j)]
    return S

def unmet_demand_penalty(p_umd, D, X, nb_vertices):
    S = 0
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            S += (p_umd[(i,j)]*D[(i,j)])*(1 - X[(i,j)] - X[(j,i)])
    return S/2

def total_revenue(c_rev, D, lbd, X, nb_vertices):
    S = 0
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            S += lbd*c_rev[(i,j)]*D[(i,j)]*X[(i,j)]
    return S

def total_investment_cost(c_fix, l, alpha, X, c_var, P_in, nb_vertices):
    Total_Fixed_Investment_Cost = total_fixed_investment_cost(c_fix, l, alpha, X, nb_vertices)
    Total_Variable_Investment_Cost = total_variable_investment_cost(c_var, l, alpha, P_in, nb_vertices)
    return Total_Fixed_Investment_Cost + Total_Variable_Investment_Cost

def total_cost(Tflh, c_heat, beta, P_in, c_om, l, X, p_umd, D, c_fix, alpha, c_var, nb_vertices):
    Total_Heat_Genration_Cost = total_heat_generation_cost(Tflh, c_heat, beta, P_in, v_0, nb_vertices)
    Total_Investment_Cost = total_investment_cost(c_fix, l, alpha, X, c_var, P_in, nb_vertices)
    Total_Maintenance_Cost = total_maintenance_cost(c_om, l, X, nb_vertices)
    Unmet_Demand_Penalty = unmet_demand_penalty(p_umd, D, X, nb_vertices)
    return Total_Heat_Genration_Cost + Total_Investment_Cost + Total_Maintenance_Cost + Unmet_Demand_Penalty

def total_expense(c_rev, D, lbd, X, Tflh, c_heat, beta, P_in, c_om, l, p_umd, c_fix, alpha, c_var, nb_vertices):
    Total_Cost = total_cost(Tflh, c_heat, beta, P_in, c_om, l, X, p_umd, D, c_fix, alpha, c_var, nb_vertices)
    Total_Revenue = total_revenue(c_rev, D, lbd, X, nb_vertices)
    return Total_Cost - Total_Revenue

def contrainte_1(X, nb_vertices):
    S = 0
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            S += X[(i,j)]
    return S == nb_vertices - 1

def contrainte_2(X, nb_vertices):
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            if i != j and X[(i,j)] + X[(j,i)] > 1:
                return False      
    return True

def contrainte_3(teta_var, teta_fix, l, lbd, beta, d, P_in, P_out, X, nb_vertices):
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            delta = d[(i,j)]*beta*lbd + teta_fix[(i,j)]*l[(i,j)]
            eta = 1 - teta_var[(i,j)]*l[(i,j)]
            if i != j and eta*P_in[(i,j)] - P_out[(i,j)] != delta*X[(i,j)]:
                return False       
    return True

def contrainte_4(P_in, P_out, v_0, nb_vertices):
    for j in range(nb_vertices):
        if j != v_0:
            S_out = 0
            S_in = 0
            for i in range(nb_vertices):
                if i != j :
                    S_out += P_out[(i,j)]
                    S_in += P_in[(j,i)]
            if S_out != S_in:
                return False
    return True

def contrainte_5(P_in, X, C_max, nb_vertices):
    for i in range(nb_vertices):
        for j in range(nb_vertices):
            if P_in[(i,j)] > X[(i,j)]*C_max[(i,j)]:
                return False
    return True

def contrainte_6(X, v_0, nb_vertices):
    S = 0
    for i in range(nb_vertices):
        if i != v_0:
            S += X[(i,v_0)]
    return S == 0

def contrainte_7(P_in, Q_max, v_0, nb_vertices):
    S = 0
    for j in range(nb_vertices):
        if j != v_0:
            S += P_in[(v_0, j)]
    return S <= Q_max[v_0]

def contrainte_8(X, v_0, nb_vertices):
    for i in range(nb_vertices):
        if i != v_0:
            S = 0
            for j in range(nb_vertices):
                if j != i:
                    S += X[(j,i)]
            if S < 1:
                return False
    return True

#import des paramètres

if __name__ == "__main__":

    inputData = r'xls_tests\InputDataExample.xlsx'

    # Input Data Preparation #
    def read_excel_data(filename, sheet_name):
        data = pd.read_excel(filename, sheet_name=sheet_name, header=None, engine='openpyxl')
        values = data.values
        if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
            if values.shape[0] == 1:
                values = values.tolist()
            else:
                values = values.transpose()
                values = values.tolist()
            return values[0]
        else:
            data_dict = {}
            if min(values.shape) == 2:  # For single-dimension parameters in Excel
                if values.shape[0] == 2:
                    for i in range(values.shape[1]):
                        data_dict[i+1] = values[1][i]
                else:
                    for i in range(values.shape[0]):
                        data_dict[i+1] = values[i][1]

            else:  # For two-dimension (matrix) parameters in Excel
                for i in range(values.shape[0]):
                    for j in range(values.shape[1]):
                        data_dict[(i+1, j+1)] = values[i][j]
            return data_dict

    # This section reads the data from Excel #

    # Read a set (set is the name of the worksheet)
    # The set has eight elements
    set_I = read_excel_data(inputData, "set")
    print("set: ", set_I)

    # Read an array 1x1 (array1 is the name of the worksheet)
    array1 = read_excel_data(inputData, "array1")
    array1 = array1[0]
    print("array1: ", array1)

    # Read an array 4x4 (array2 is the name of the worksheet)
    array2 = read_excel_data(inputData, "array2")
    print("array2: ", array2)

#Paramètres

v_0 =
nb_vertices =
c_fix =
c_var =
c_om =
c_heat =
c_rev =
p_umd =
alpha =
teta_fix =
teta_var =
Tflh =
beta =
lbd =
l =
d = 
D =
C_max = 
Q_max =

#Variables

L = [range(0,nb_vertices)]
X = LpVariable('X', [L, L], cat='Binary')
P_in = LpVariable('P_in', [L, L], lowbound = 0, cat='Continuous')
P_out = LpVariable('P_out', [L, L], lowbound = 0, cat='Continuous')
            
#Problème et contraintes

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


