import pandas as pd

#Paramètres
variables = {
    'v_0':0,
    'nb_vertices':0,
    'c_fix' :0,
    'c_var' :0,
    'c_om' :0,
    'c_heat' :0,
    'c_rev' :0,
    'p_umd' :0,
    'alpha' :0,
    'teta_fix' :0,
    'teta_var' :0,
    'Tflh':0,
    'beta' :0,
    'lbd' :0,
    'l' :0,
    'd':0, 
    'D' :0,
    'C_max' :0, 
    'Q_max' :0
    }

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

def testRead(inputData) :
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

    v_0 = read_excel_data(inputData, "SourceNum")
    variables['v_0'] = v_0[0]

    nb_vertices = read_excel_data(inputData, "Nodes")
    nb_vertices = nb_vertices[0]

    node_coord = read_excel_data(inputData,"NodesCord")

