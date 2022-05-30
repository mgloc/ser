import pandas as pd
import numpy as np

#Paramètres
variables = {
    'v_0':None,
    'nb_vertices':None,
    'c_fix' :None,
    'c_var' :None,
    'c_om' :None,
    'c_heat' :None,
    'c_rev' :None,
    'p_umd' :None,
    'alpha' :None,
    'teta_fix' :None,
    'teta_var' :None,
    'Tflh':None,
    'beta' :None,
    'lbd' :None,
    'l' :None,
    'd':None, 
    'D' :None,
    'C_max' :None, 
    'Q_max' :None
    }

def read_excel_data(filename:str, sheet_name:str):
    """Function use to read excel data"""
    data = pd.read_excel(filename, sheet_name=sheet_name, header=None)
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
        """if min(values.shape) == 2:  # For single-dimension parameters in Excel
            if values.shape[0] == 2:
                for i in range(values.shape[1]):
                    data_dict[i+1] = values[1][i]
            else:
                for i in range(values.shape[0]):
                    data_dict[i+1] = values[i][1]

        else:  # For two-dimension (matrix) parameters in Excel"""
        for i in range(values.shape[0]):
            for j in range(values.shape[1]):
                data_dict[(i, j)] = values[i][j]
        return data_dict

def get_variables(inputData:str)->dict :
    """Function use to get variables for the Heating Problem from excel"""

    variables['v_0'] = read_excel_data(inputData, "SourceNum")[0]

    variables['nb_vertices'] = read_excel_data(inputData, "Nodes")[0]

    #Définition variable "l"
    node_coord = read_excel_data(inputData,"NodesCord")
    l = {}
    for i in range(variables['nb_vertices']):
        for j in range(variables['nb_vertices']):
            l[(i,j)] = np.sqrt((node_coord[(i,0)]-node_coord[(j,0)])**2 + (node_coord[(i,1)]-node_coord[(j,1)])**2)
    variables['l'] = l

    variables['teta_fix'] = read_excel_data(inputData, "vfix(thetaijfix)")

    variables['teta_var'] = read_excel_data(inputData, "vvar(thetaijvar)")

    variables['c_fix'] = read_excel_data(inputData, "FixedUnitCost")[0]

    variables['c_var'] = read_excel_data(inputData, "cvar(cijvar)")

    variables['c_heat'] = read_excel_data(inputData, "cheat(ciheat)")

    variables['c_om'] = read_excel_data(inputData, "com(cijom)")

    variables['c_rev'] = read_excel_data(inputData, "crev(cijrev)")

    variables['Tflh'] = read_excel_data(inputData, "Tflh(Tiflh)")[0]

    variables['beta'] = read_excel_data(inputData, "Betta")[0]

    variables['lbd'] = read_excel_data(inputData, "Lambda")[0]

    variables['alpha'] = read_excel_data(inputData, "Alpha")[0]

    variables['d'] = read_excel_data(inputData, "EdgesDemandPeak(dij)")

    variables['D'] = read_excel_data(inputData, "EdgesDemandAnnual(Dij)")

    variables['C_max'] = read_excel_data(inputData, "Cmax(cijmax)")

    variables['Q_max'] = read_excel_data(inputData, "SourceMaxCap(Qimax)")

    variables['p_umd'] = read_excel_data(inputData, "pumd(pijumd)")

    return variables







            

    

