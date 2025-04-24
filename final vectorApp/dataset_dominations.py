import time
import mylabnew as mll
import pandas as pd
import openpyxl
start_time = time.time()
path1='d:\\vectorDataset1.xlsx'
path2='d:\\Dtest.xlsx'
path3="d:\\.xlsx"
df = pd.read_excel(path1,sheet_name='data')
# ------------  finding the number of inputs and outputs --------------------
t=0
for i in df.columns:
    t+=1
    if i =="O1":
        I=t-2
        O=len(df.columns)-I-1
# ------------- getting the Dimentions of dataFrame --------------------------
print("\n your matrix id : {} * {} \n".format( len(df.index),len(df.columns)));
print("\n Your dataset is : \n", df)


def find_non_dominated_rows(df, num_inputs, num_outputs):  
    """  
    Finds the non-dominated rows in the given DataFrame.  
    
    Args:  
        df (pandas.DataFrame): The DataFrame containing the DMUs.  
        num_inputs (int): The number of input columns.  
        num_outputs (int): The number of output columns.  
    
    Returns:  
        pandas.DataFrame: The DataFrame containing the non-dominated rows.  
    """  
    non_dominated_rows = []  
    
    for i, row_i in df.iterrows():  
        is_dominated = False  
        
        for j, row_j in df.iterrows():  
            if i != j:  
                # Check if row_i is dominated by row_j  
                if all(row_j[1:1+num_inputs] <= row_i[1:1+num_inputs]) and all(row_j[1+num_inputs:1+num_inputs+num_outputs] >= row_i[1+num_inputs:1+num_inputs+num_outputs]):  
                    is_dominated = True  
                    break  
        
        if not is_dominated:  
            non_dominated_rows.append(row_i)  
    
    return pd.DataFrame(non_dominated_rows, columns=df.columns) 
non_dominated_df = find_non_dominated_rows(df,I,O) 
 
print("\n Non-dominated rows:\n", non_dominated_df)

# Save the non-dominated rows to an Excel file  
output_path = 'd:\\non_dominated_rows.xlsx'  
non_dominated_df.to_excel(output_path, index=False)  
print(f"\nNon-dominated rows saved to: {output_path}")
    