from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value  
import pandas as pd  


path= 'd:\\r.xlsx'
# Set building  
df = pd.read_excel(path, sheet_name='data')  
K = df['DMU'].tolist()  
I = [col for col in df.columns if col.startswith('I')]  
J = [col for col in df.columns if col.startswith('O')]  

# Parameters building  
X = {  
    i: {  
        k: 0 for k in K  
    } for i in I  
}  
Y = {  
    j: {  
        k: 0 for k in K  
    } for j in J  
}  

# Populate input and output parameters  
for i in I:  
    for k in K:  
        X[i][k] = df.loc[df['DMU'] == k, i].values[0]  
for j in J:  
    for k in K:  
        Y[j][k] = df.loc[df['DMU'] == k, j].values[0]  

# BCC_DEA_Model  
results = []  
for dmu in K:  
    # Model Building  
    model = LpProblem('BCC_model', LpMinimize)  

    # Decision variables Building  
    theta_r = LpVariable(f'theta_r')  
    lambda_k = {k: LpVariable(f'lambda_{k}', lowBound=0) for k in K}  

    # Objective Function setting  
    model += theta_r  

    # Constraints setting  
    for i in I:  
        model += lpSum([  
            lambda_k[k] * X[i][k]  
            for k in K]) <= theta_r * float(X[i][dmu])  
    for j in J:  
        model += lpSum([  
            lambda_k[k] * Y[j][k]  
            for k in K]) >= float(Y[j][dmu])  
    model += lpSum([lambda_k[k] for k in K]) == 1  # Added convexity constraint  

    # model solving  
    model.solve()  

    # Collect results  
    result = {'DMU': dmu, 'Efficiency': round(value(model.objective), 3)}  
    for k in K:  
        result[f'lambda_{k}'] = round(value(lambda_k[k]), 3)  
    results.append(result)  

df_results = pd.DataFrame(results)  

filename = path 
sheet_name = 'BCC-Results'  

try:  
    with pd.ExcelWriter(filename, mode='a', engine='openpyxl') as writer:  
        if sheet_name in writer.sheets:  
            # Append to the existing sheet  
            df_results.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=writer.sheets[sheet_name].max_row)  
        else:  
            # Create a new sheet and write the header  
            df_results.to_excel(writer, sheet_name=sheet_name, index=False, header=True)  
except:  
    # Create a new Excel file and write the header  
    df_results.to_excel(filename, sheet_name=sheet_name, index=False, header=True)