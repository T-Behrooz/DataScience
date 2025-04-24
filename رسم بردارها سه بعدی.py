import matplotlib.pyplot as plt  
from mpl_toolkits.mplot3d import Axes3D  

# داده‌ها  
data = [  
    [2, 85109595, 0, 4940390053, 8444610529, 18545675, 6514099, 0],  
    [2, 160826219, 0, 9541242615, 14497510825, 246560473, 5967964, 5163900],  
    [2, 165882927, 0, 4949921039, 15855342693, 59911522, 18110319, 16904000],  
]  

# تبدیل داده‌ها به آرایه‌های جداگانه  
labels = [d[0] for d in data]  
values = [d[1:] for d in data]  

# ایجاد نمودار سه بعدی  
fig = plt.figure(figsize=(10, 6))  
ax = fig.add_subplot(111, projection='3d')  

# ترسیم داده‌ها و نامگذاری نقاط  
for i, value in enumerate(values):  
    x = range(len(value))  
    
    # رسم خط  
    ax.plot(x, value, zs=i, zdir='y', marker='o', label=f'Line {labels[i]}')  

    # نامگذاری نقاط  
    for j in x:  
        ax.text(j, i, value[j], f'{value[j]:,.0f}', fontsize=10, ha='right', color='black')  

# تنظیمات نمودار  
ax.set_title('رسم داده‌ها به صورت سه بعدی با نامگذاری نقاط')  
ax.set_xlabel('اندیس')  
ax.set_ylabel('برچسب خط')  
ax.set_zlabel('مقدار')  
ax.set_yticks(range(len(values)))  # برچسب‌گذاری محور y  
ax.set_yticklabels([f'خط {labels[i]}' for i in range(len(labels))])  # برچسب دهی  

# نمایش راهنما  
ax.legend()  
ax.grid()  

# نمایش نمودار  
plt.show()