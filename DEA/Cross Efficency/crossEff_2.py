from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import pandas as pd
import time
import os
import re
import win32com.client  # For Windows-specific Excel cleanup

# Input and output paths
input_path = 'd:\\11.xlsx'
output_path = 'd:\\cross_efficiency_2_output.xlsx'

def sanitize_column_name(name):
    """Sanitize column names to remove any invalid characters for Excel."""
    # Remove any characters that are not letters, numbers, or underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_\-\.]', '', name)
    return sanitized

def cleanup_excel():
    """Ensure all Excel processes are closed."""
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        if excel:
            excel.Quit()
    except Exception as e:
        print(f"Error closing Excel: {str(e)}")

def main():
    try:
        # Read data
        df = pd.read_excel(input_path, sheet_name='data')
        K = df['DMU'].tolist()
        I = [col for col in df.columns if col.startswith('I')]
        J = [col for col in df.columns if col.startswith('O')]
        n = len(K)
        m = len(I)
        s = len(J)

        # Prepare input and output parameters
        X = {i: {k: df.loc[df['DMU'] == k, i].values[0] for k in K} for i in I}
        Y = {j: {k: df.loc[df['DMU'] == k, j].values[0] for k in K} for j in J}

        # Prepare to store cross-efficiency results
        cross_efficiency_matrix = [[0.0 for _ in range(n)] for _ in range(n)]

        # Calculate DEA efficiency and weights for each DMU
        dea_results = []
        lambda_weights = {}

        for dmu_eval in K:
            print(f"Calculating DEA for {dmu_eval}")
            model = LpProblem(f"DEA_Model_{dmu_eval}", LpMinimize)
            
            theta = LpVariable(f"theta_{dmu_eval}")
            lambda_k = LpVariable.dicts("lambda", K, lowBound=0)
            slack_i = LpVariable.dicts("slack_i", I, lowBound=0)
            slack_j = LpVariable.dicts("slack_j", J, lowBound=0)
            
            model += theta + 0.000001 * (lpSum(slack_i.values()) + lpSum(slack_j.values()))
            
            for i in I:
                model += lpSum([lambda_k[k] * X[i][k] for k in K]) + slack_i[i] == theta * X[i][dmu_eval]
            
            for j in J:
                model += lpSum([lambda_k[k] * Y[j][k] for k in K]) - slack_j[j] == Y[j][dmu_eval]
            
            model += lpSum([lambda_k[k] for k in K]) == 1
            
            start_time = time.time()
            model.solve()
            elapsed_time = time.time() - start_time
            
            efficiency = value(theta)
            dea_results.append({
                'DMU': dmu_eval,
                'Efficiency': round(efficiency, 3),
                'Time (s)': round(elapsed_time, 3)
            })
            
            lambda_weights[dmu_eval] = {k: value(lambda_k[k]) for k in K}
            print(f"DEA completed for {dmu_eval}.")

        # Calculate cross-efficiency scores
        for eval_dmu in K:
            for base_dmu in K:
                if eval_dmu == base_dmu:
                    cross_efficiency_matrix[K.index(eval_dmu)][K.index(base_dmu)] = dea_results[K.index(eval_dmu)]['Efficiency']
                    continue
                
                lambda_weights_base = lambda_weights[base_dmu]
                total_output = sum(Y[j][eval_dmu] * lambda_weights_base[k] for k in K for j in J)
                total_input = sum(X[i][eval_dmu] * lambda_weights_base[k] for k in K for i in I)
                
                if total_input > 0:
                    efficiency = total_output / total_input
                    cross_efficiency_matrix[K.index(eval_dmu)][K.index(base_dmu)] = round(efficiency, 3)
                else:
                    cross_efficiency_matrix[K.index(eval_dmu)][K.index(base_dmu)] = 0

        # Create DataFrame with sanitized column names
        sanitized_columns = [sanitize_column_name(col) for col in K]
        matrix_df = pd.DataFrame(
            cross_efficiency_matrix,
            index=K,
            columns=sanitized_columns
        )

        # Ensure headers are properly set
        matrix_df.columns = [f"DMU_{col}" for col in matrix_df.columns]

        # Export cross-efficiency matrix to Excel
        try:
            # Ensure the output directory exists
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Use pandas' ExcelWriter for robust writing
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                matrix_df.to_excel(
                    writer,
                    sheet_name='Cross_Efficiency_Matrix',
                    index=True,
                    header=True
                )
            
            print(f"Cross-efficiency matrix saved successfully to: {output_path}")
            
        except PermissionError:
            print("Permission denied. Please close Excel and try again.")
            # Implement retry logic if needed
            retries = 0
            max_retries = 3
            success = False
            
            while retries < max_retries and not success:
                try:
                    cleanup_excel()
                    # Replace with your retry logic
                    time.sleep(1)
                    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                        matrix_df.to_excel(
                            writer,
                            sheet_name='Cross_Efficiency_Matrix',
                            index=True,
                            header=True
                        )
                    success = True
                except Exception as e:
                    print(f"Attempt {retries + 1} failed: {str(e)}")
                    retries += 1
            
            if not success:
                print(f"Failed after {max_retries} attempts. Please try again.")
        
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            # Ensure Excel processes are closed
            cleanup_excel()

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        cleanup_excel()
        raise

if __name__ == "__main__":
    main()