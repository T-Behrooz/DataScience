import matplotlib.pyplot as plt  

# داده‌ها  
data = [  
    [2, 85109595, 0, 4940390053, 8444610529, 18545675, 6514099, 0],  
    [2, 160826219, 0, 9541242615, 14497510825, 246560473, 5967964, 5163900],  
    [2, 165882927, 0, 4949921039, 15855342693, 59911522, 18110319, 16904000],  
]  

# تبدیل داده‌ها به آرایه‌های جداگانه  
labels = [d[0] for d in data]  
values = [d[1:] for d in data]  

# رسم داده‌ها  
plt.figure(figsize=(10, 6))  

for i, value in enumerate(values):  
    plt.plot(range(len(value)), value, marker='o', label=f'Line {labels[i]}')  

# تنظیمات نمودار  
plt.title('رسم داده‌ها')  
plt.xlabel('اندیس')  
plt.ylabel('مقدار')  
plt.xticks(range(len(values[0])))  # برچسب گذاری محور x  
plt.legend()  
plt.grid()  

# نمایش نمودار  
plt.show()