from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value  
import pandas as pd  
import time  


path= 'd:\\bank.xlsx'

# Set building  
df = pd.read_excel(path, sheet_name='data')  
K = df['DMU'].tolist()  
I = [col for col in df.columns if col.startswith('I')]  
J = [col for col in df.columns if col.startswith('O')]  
eps = 0.000001  

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

# ε-constrained DEA Model  
results = []  
for dmu in K:  
    # Start timer  
    start_time = time.time()  

    # Model Building  
    model = LpProblem('ε-constrained_model', LpMinimize)  

    # Decision variables Building  
    theta_r = LpVariable(f'theta_r')  
    lambda_k = {k: LpVariable(f'lambda_{k}', lowBound=0) for k in K}  
    s_i = {i: LpVariable(f's_i_{i}', lowBound=0) for i in I}  
    s_j = {j: LpVariable(f's_j_{j}', lowBound=0) for j in J}  

    # Objective Function setting  
    model += theta_r + eps * (lpSum(s_i.values()) + lpSum(s_j.values()))  

    # Constraints setting  
    for i in I:  
        model += lpSum([  
            lambda_k[k] * X[i][k]  
        ] for k in K) + s_i[i] == theta_r * X[i][dmu]  
    for j in J:  
        model += lpSum([  
            lambda_k[k] * Y[j][k]  
        ] for k in K) - s_j[j] >= Y[j][dmu]  
    model += lpSum([lambda_k[k] for k in K]) == 1  # Added convexity constraint  

    # model solving  
    model.solve()  

    # Collect results  
    efficiency = value(model.objective) - eps * (value(lpSum(s_i.values())) + value(lpSum(s_j.values())))  
    result = {  
        'DMU': dmu,  
        'Efficiency': round(efficiency, 3),  
        'Time (s)': round(time.time() - start_time, 3)  
    }  
    for k in K:  
        result[f'lambda_{k}'] = round(value(lambda_k[k]), 3)  
    for i in I:  
        result[f'slack_i_{i}'] = round(value(s_i[i]), 3)  
    for j in J:  
        result[f'slack_j_{j}'] = round(value(s_j[j]), 3)  
    result['epsilon'] = round(eps * (value(lpSum(s_i.values())) + value(lpSum(s_j.values()))), 9)  
    results.append(result)  

df_results = pd.DataFrame(results)  

filename = path  
sheet_name = 'result-ε-constrained_model'  

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