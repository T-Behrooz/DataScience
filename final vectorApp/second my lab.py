import numpy as np  
import pandas as pd  
import math as m  

#------------------------------------------------------------------------------   
def domination(df, I, O):  
    mat = df.values[:, 1:]  
    rows = mat.shape[0]  

    def cal():  
        results = []  
        for i in range(rows):  
            temp_results = []  
            for j in range(rows):  
                if i == j:  
                    continue  
                state_input = np.all(-mat[j, :I] >= -mat[i, :I])  
                state_output = np.all(mat[j, I:] >= mat[i, I:])  
                temp_results.append(state_input and state_output)  
            results.append(temp_results)  
        return results  

    res = cal()  
    unique_indices = {i for i, row_results in enumerate(res) if any(row_results)}  

    if not unique_indices:  
        return "There is no solution"  

    solutions = [mat[i] for i in unique_indices]  

    def remove_duplicates(x):  
        return list(dict.fromkeys(x))  

    Index = remove_duplicates([df.values[i, 0] for i in unique_indices])  
    return solutions, Index  

#------------------------------------------------------------------------------  
def find_dominator_in_set(df, I, O):    
    res = {}  
    for row1 in df.index:  
        dominated = []  
        dmuo = df.loc[row1]  
        for row2 in df.index:  
            if row1 != row2:  
                temp1 = np.all(-df.loc[row2, 1:I + 1] >= -dmuo[1:I + 1])  
                temp2 = np.all(df.loc[row2, I + 1:O + I] >= dmuo[I + 1:O + I])  
                if temp1 and temp2:  
                    dominated.append(row2)  
        res[row1] = dominated  
    return res  

#-------------------------------------------------------------------------------  
def find_dominated_by_dmu(df, dmu, I):       
    dominated = []  
    row1 = dmu.index[0]  
    for row2 in df.index:  
        if row1 != row2:  
            temp1 = np.all(-df.loc[row2, 1:I + 1] <= -dmu[1:I + 1])  
            temp2 = np.all(df.loc[row2, I + 1:] <= dmu[I + 1:])  
            if temp1 and temp2:  
                dominated.append(row2)  
    return dominated  

#----------------------- calculating vector size -----------------------------------  
def size_of_vector(dmu):  
    return np.linalg.norm(dmu)  

#-------------------------- finding the ideal DMU -------------------------------------     
def find_IDMU(df):  
    I = df.columns.get_loc('O1') - 1  
    ideal_dmu = {'dmus': 'IDMU'}  
    
    for i, col in enumerate(df.columns):  
        if 1 <= i <= I:  
            ideal_dmu[col] = df[col].min()  
        elif i > I:  
            ideal_dmu[col] = df[col].max()  
            
    return pd.DataFrame([ideal_dmu])  

#-------------------------- finding DMUI and DMUO sets-------------------------------------            
def filter_dmuo_dmui_sets(df, I, O):  
    dfI = df.iloc[:, 1:I + 1]  
    dfO = df.iloc[:, I + 1:]  

    input_filter = pd.concat([df[df[i] == dfI[i].min()] for i in dfI.columns], ignore_index=True).drop_duplicates()  
    output_filter = pd.concat([df[df[i] == dfO[i].max()] for i in dfO.columns], ignore_index=True).drop_duplicates()  

    return input_filter, output_filter  

#--------------------------- Remove Dominated DMUs from main DataFrame ----------------  
def removeDominatedDmus(maindf, dmu_set):  
    return maindf.drop(index=dmu_set)  

#------------------------ returns vector elements ------------------------------------------  
def return_vector_elements(dmu1, dmu2):  
    return [dmu1.iloc[0, 0], dmu2.iloc[0, 0]] + (dmu1.iloc[0, 1:].values - dmu2.iloc[0, 1:]).tolist()  

#------------------------ returns angles of vectors with main vector ----------------------  
def vector_angle(dmu1, dmu2):  
    bottom = size_of_vector(dmu1) * size_of_vector(dmu2)  
    top = np.dot(dmu1, dmu2)  

    if bottom != 0:  
        angle = m.degrees(m.acos(top / bottom))  
    else:  
        angle = 360  # Default angle if vectors are zero-length  
    return angle  

#------------------------------------------------------------------------------  
def choice_dmui_or_dmuo_from_multiples(newdataset, I, O):  
    eff = {}  
    for i in newdataset.index:  
        inputs = newdataset.loc[i, 1:I + 1].values  
        bottom = inputs.sum()  
        outputs = newdataset.loc[i, I + 1:].values  
        top = outputs.sum()  
        eff[newdataset.loc[i, 0]] = top / bottom if bottom != 0 else 0  # Handle division by zero  

    max_eff = max(eff.values())  
    optimal_dmu = [k for k, v in eff.items() if v == max_eff][0]  
    return newdataset.loc[newdataset['DMUS'] == optimal_dmu]  

#-------------------------- Example usage -------------------------   
# Assuming that you have a DataFrame called `df` with relevant DMU data.  
# Replace the following line with your actual DataFrame initialization.  
# df = pd.DataFrame()  

# I = number of inputs, O = number of outputs  
# I = num_inputs   
# O = num_outputs  

# You can now call the functions defined above as needed.