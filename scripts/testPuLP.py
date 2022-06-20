import pulp as plp

###Exemple 1 (fonctionnel)
def exemple1():
    #Create decisions variables
    x1 = plp.LpVariable('x1',lowBound=0,cat='Continuous')
    x2 = plp.LpVariable('x2',lowBound=0,cat='Continuous')
    
    #Create the problem
    exemple1 = plp.LpProblem('exemple1',plp.LpMaximize)

    #Objectif function to minimize (to add first)
    exemple1 += 3*x1 + 5*x2

    #Constraints
    exemple1 += x1 <= 4
    exemple1 += x2 <= 6
    exemple1 += 3*x1 + 2*x2 <= 18

    #Solve
    exemple1.solve()

    #Status
    print("Status :", plp.LpStatus[exemple1.status])

    #Optimal value
    for v in exemple1.variables() :
        print(v.name," = ",v.varValue)


###Exercice 1 (problématique)
def exercice1():
    set_I = list(range(1,9))
    set_J = list(range(1,11))
    param_f = 90
    fixedcost_i = [
        684,
        977,
        563,
        612,
        950,
        928,
        750,
        766
    ]
    capacity_i = [
        200,
        300,
        150,
        180,
        280,
        270,
        200,
        220
    ]
    demand_j = [
        80,
        50,
        82,
        43,
        96,
        107,
        88,
        42,
        65,
        38]
    param_d = [
        [18,14,12,16,19,17,14,18,11,13],
        [12,15,17,19,13,10,15,14,16,14],
        [11,12,12,20,19,20,12,15,13,16],
        [11,18,10,10,11,15,13,15,10,15],
        [10,14,20,10,10,16,18,16,15,15],
        [12,14,20,14,15,10,12,15,17,13],
        [13,17,19,15,12,12,12,14,20,14],
        [11,10,12,18,18,17,19,20,15,10]
    ]

    param_c = []
    for i in set_I :
        param_c.append([param_d[i-1][j-1]*param_f for j in set_J])

    x_var = plp.LpVariable.dicts('x', (set_I, set_J), 0)
    y_var = plp.LpVariable.dicts('y', set_I, cat=plp.LpBinary)

    #Déclaration qu'on a un problème sheesh
    problem = plp.LpProblem("exercice1", plp.LpMinimize)

    #Contrainte a minimiser
    problem += plp.lpSum(param_c[i-1][j-1] * x_var[i][j] for j in set_J for i in set_I) + plp.lpSum(y_var[i+1]*fixedcost_i[i] for i in range(8))

    #Autres contraintes
    for i in set_I:
        problem += plp.lpSum(x_var[i][j] for j in set_J) <= capacity_i[i-1]*y_var[i]

    for j in set_J:
        problem += plp.lpSum(x_var[i][j] for i in set_I) >= demand_j[j-1]

    for i in set_I:
        problem += plp.lpSum(y_var[i]) == 3


    #Status
    print("Status :", plp.LpStatus[problem.status])

    problem.solve()

    
    for v in problem.variables() :
        print(v.name," = ",v.varValue)

