import matplotlib.pyplot as plt  
import numpy as np  
from scipy.spatial import ConvexHull  

# داده‌ها  
data = [  
    ['dmu9', 3, 1005113914, 0, 3584419088, 50202986408, 5370125, 9269576, 390000],  
    ['dmu831', 3, 268900331, 0, 40957313986, 22303615732, 239092135, 31793067, 44000000],  
    ['dmu383', 3, 238745538, 0, 24841123887, 18561868500, 69147926, 11021450, 71324500],  
    ['dmu515', 3, 491111077, 0, 29265219481, 37766245801, 0, 28044196, 0],  
    ['dmu57', 3, 154763052, 0, 9276125118, 18386800568, 117438020, 741398, 0],  
    ['dmu43', 3, 131689000, 0, 8083598806, 10494704407, 149610232, 7807255, 0],  
    ['dmu276', 3, 131315447, 0, 20249357786, 9042946726, 68212247, 16084775, 42800000],  
    ['dmu641', 3, 317550897, 0, 34093695518, 23698398262, 183063583, 28888851, 27800000],  
    ['dmu206', 3, 219470054, 0, 17459023215, 15963539095, 11891709, 3346775, 0],  
]  

# تبدیل داده‌ها به آرایه‌های جداگانه  
input_indices = [d[2:3] + d[6:9] for d in data]  # سه ورودی اول (داده‌های ورودی)  
output_indices = [d[3:6] for d in data]  # پنج ورودی آخر (داده‌های خروجی)  

input_values = np.array(input_indices)  
output_values = np.array(output_indices)  

# رسم نقاط ورودی و خروجی  
fig = plt.figure(figsize=(12, 8))  

# رسم ورودی‌ها  
ax1 = fig.add_subplot(121, projection='3d')  
ax1.scatter(input_values[:, 0], input_values[:, 1], input_values[:, 2], color='blue', label='Inputs')  
ax1.set_title('داده‌های ورودی')  
ax1.set_xlabel('ورودی 1')  
ax1.set_ylabel('ورودی 2')  
ax1.set_zlabel('ورودی 3')  
ax1.legend()  

# رسم خروجی‌ها  
ax2 = fig.add_subplot(122, projection='3d')  
ax2.scatter(output_values[:, 0], output_values[:, 1], output_values[:, 2], color='red', label='Outputs')  
ax2.set_title('داده‌های خروجی')  
ax2.set_xlabel('خروجی 1')  
ax2.set_ylabel('خروجی 2')  
ax2.set_zlabel('خروجی 3')  
ax2.legend()  

plt.tight_layout()  
plt.show()  

# رسم پوسته محدب برای داده‌های خروجی  
hull = ConvexHull(output_values)  

fig_hull = plt.figure(figsize=(8, 8))  
ax_hull = fig_hull.add_subplot(111, projection='3d')  

# رسم نقاط  
ax_hull.scatter(output_values[:, 0], output_values[:, 1], output_values[:, 2], color='red')  

# رسم پوسته محدب  
for simplex in hull.simplices:  
    ax_hull.plot(output_values[simplex, 0], output_values[simplex, 1], output_values[simplex, 2], color='blue')  

ax_hull.set_title('پوسته محدب داده‌های خروجی')  
ax_hull.set_xlabel('خروجی 1')  
ax_hull.set_ylabel('خروجی 2')  
ax_hull.set_zlabel('خروجی 3')  
plt.show()