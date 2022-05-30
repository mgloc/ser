#------------------------------------------------FONCTION MINIMALE--------------------------------------------------------------

# FONCTIONS SUBSIDIAIRES
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
def total_cost(Tflh, c_heat, beta, P_in, c_om, l, X, p_umd, D, c_fix, alpha, c_var, nb_vertices,v_0):
    Total_Heat_Genration_Cost = total_heat_generation_cost(Tflh, c_heat, beta, P_in, v_0, nb_vertices)
    Total_Investment_Cost = total_investment_cost(c_fix, l, alpha, X, c_var, P_in, nb_vertices)
    Total_Maintenance_Cost = total_maintenance_cost(c_om, l, X, nb_vertices)
    Unmet_Demand_Penalty = unmet_demand_penalty(p_umd, D, X, nb_vertices)
    return Total_Heat_Genration_Cost + Total_Investment_Cost + Total_Maintenance_Cost + Unmet_Demand_Penalty

# FONCTION FINALE
def total_expense(c_rev, D, lbd, X, Tflh, c_heat, beta, P_in, c_om, l, p_umd, c_fix, alpha, c_var, nb_vertices,v_0):
    Total_Cost = total_cost(Tflh, c_heat, beta, P_in, c_om, l, X, p_umd, D, c_fix, alpha, c_var, nb_vertices,v_0)
    Total_Revenue = total_revenue(c_rev, D, lbd, X, nb_vertices)
    return Total_Cost - Total_Revenue

#------------------------------------------------CONTRAINTES--------------------------------------------------------------

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