from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value  
import pandas as pd  
import time  
import os  
import shutil

#زمان و تاریخ 
from datetime import datetime
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# مسیر فایل ورودی
drive = "d:\\"
file_name = 'Raw 1400 Dmus DataSet ( no Zero ).xlsx'  
input_path = os.path.join(drive, file_name)  
output_file = os.path.join(drive, "BCC_ε_of_" + current_datetime +"_"+ file_name)  

# خواندن داده‌ها
df = pd.read_excel(input_path, sheet_name='data')  
K = df['DMU'].tolist()  
I = [col for col in df.columns if col.startswith('I')]  
J = [col for col in df.columns if col.startswith('O')]  
eps = 0.000001  

# ساخت پارامترها
X = {i: {k: df.loc[df['DMU'] == k, i].values[0] for k in K} for i in I}  
Y = {j: {k: df.loc[df['DMU'] == k, j].values[0] for k in K} for j in J}  

# اجرای مدل DEA برای هر DMU
results = []  
for dmu in K:  
    start_time = time.time()  
    model = LpProblem('ε-constrained_model', LpMinimize)  
    
    # تعریف متغیرهای تصمیم
    theta_r = LpVariable(f'theta_r', lowBound=0)
    lambda_k = {k: LpVariable(f'lambda_{k}', lowBound=0) for k in K}  
    s_i = {i: LpVariable(f's_i_{i}', lowBound=0) for i in I}  
    s_j = {j: LpVariable(f's_j_{j}', lowBound=0) for j in J}  
    
    # تابع هدف
    model += theta_r + eps * (lpSum(s_i.values()) + lpSum(s_j.values()))  
    
    # محدودیت‌ها
    for i in I:  
        model += lpSum(lambda_k[k] * X[i][k] for k in K) + s_i[i] == theta_r * X[i][dmu]  
    for j in J:  
        model += lpSum(lambda_k[k] * Y[j][k] for k in K) - s_j[j] == Y[j][dmu]
    model += lpSum([lambda_k[k] for k in K]) == 1  # Added convexity constraint
    # حل مدل
    model.solve()  
    
    # جمع‌آوری نتایج
    efficiency = value(theta_r)
    result = {'DMU': dmu, 'Efficiency': round(efficiency, 3), 'Time (s)': round(time.time() - start_time, 3)}  
    result.update({f'l_{k}': round(value(lambda_k[k]), 3) for k in K})  
    result.update({f'si_{i}': round(value(s_i[i]), 3) for i in I})  
    result.update({f'so_{j}': round(value(s_j[j]), 3) for j in J})  
    result['epsilon'] = round(eps * (value(lpSum(s_i.values())) + value(lpSum(s_j.values()))), 9)  
    results.append(result)  

# تبدیل نتایج به DataFrame
df_results = pd.DataFrame(results)  

# راه‌حل جایگزین: استفاده از pandas برای ذخیره‌سازی در اکسل
def save_with_pandas(df_results, df, output_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            # ایجاد یک ExcelWriter جدید
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df_results.to_excel(writer, sheet_name='نتایج', index=False)
                df.to_excel(writer, sheet_name='داده‌ها', index=False)
            
            print(f"فایل با موفقیت ذخیره شد: {output_path}")
            return True
            
        except PermissionError:
            print(f"خطای دسترسی در تلاش {attempt + 1}. منتظر بمانید...")
            time.sleep(2)
        except Exception as e:
            print(f"خطا در ذخیره فایل: {e}")
            
            # تلاش با موتور xlsxwriter
            try:
                with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                    df_results.to_excel(writer, sheet_name='نتایج', index=False)
                    df.to_excel(writer, sheet_name='داده‌ها', index=False)
                print(f"فایل با موتور xlsxwriter ذخیره شد: {output_path}")
                return True
            except Exception as e2:
                print(f"خطا در ذخیره با xlsxwriter: {e2}")
                
                # ذخیره به صورت CSV
                try:
                    csv_path = output_path.replace('.xlsx', '.csv')
                    df_results.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    print(f"نتایج به صورت CSV ذخیره شد: {csv_path}")
                    return True
                except Exception as e3:
                    print(f"خطا در ذخیره CSV: {e3}")
                    return False
    
    return False

# راه‌حل نهایی: اگر همه روش‌ها شکست خوردند، از کتابخانه‌ی دیگری استفاده کنیم
def final_save_solution(df_results, df, output_path):
    try:
        # استفاده از کتابخانه xlwt برای ذخیره‌سازی در قالب xls (قدیمی اما پایدار)
        try:
            # ذخیره در قالب xls با xlwt
            xls_path = output_path.replace('.xlsx', '.xls')
            with pd.ExcelWriter(xls_path, engine='xlwt') as writer:
                df_results.to_excel(writer, sheet_name='نتایج', index=False)
                df.to_excel(writer, sheet_name='داده‌ها', index=False)
            print(f"نتایج در قالب XLS ذخیره شد: {xls_path}")
            return True
        except:
            pass
        
        # ذخیره به صورت چندین فایل CSV
        try:
            base_name = output_path.replace('.xlsx', '')
            df_results.to_csv(f"{base_name}_results.csv", index=False, encoding='utf-8-sig')
            df.to_csv(f"{base_name}_data.csv", index=False, encoding='utf-8-sig')
            print(f"نتایج در فایل‌های CSV ذخیره شدند: {base_name}_results.csv و {base_name}_data.csv")
            return True
        except Exception as e:
            print(f"خطا در ذخیره CSV: {e}")
            return False
            
    except Exception as e:
        print(f"خطای نهایی در ذخیره‌سازی: {e}")
        return False

# اجرای ذخیره‌سازی
print("در حال ذخیره نتایج...")

# ابتدا با pandas امتحان می‌کنیم
success = save_with_pandas(df_results, df, output_file)

# اگر موفق نبود، از راه‌حل نهایی استفاده می‌کنیم
if not success:
    print("استفاده از راه‌حل نهایی...")
    success = final_save_solution(df_results, df, output_file)

if success:
    print("پردازش و ذخیره‌سازی کامل شد.")
else:
    print("ذخیره‌سازی ناموفق بود. لطفاً مطمئن شوید فایل‌های اکسل باز نیستند و مجدداً اجرا کنید.")
    # نمایش نتایج در خروجی به عنوان آخرین راه‌حل
    print("\nنتایج محاسبات:")
    print(df_results.to_string())