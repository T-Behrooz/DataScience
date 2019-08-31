import pyodbc
import matplotlib.pyplot as plt

con = pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=sanj;UID=sa;PWD=123")
do = con.cursor()
row = do.execute("select sum(income),duration from contracts where year1 =1397 and trade_name =N'توزيع مرسولات خدمات خودرويي 2' group by duration order by duration asc ")
x_list = []
y_list = []
for i in row :
    # word_list.append(i[0])
    # print(i[1])
    x_list.append(i[1])
    y_list.append(i[0])
print (x_list)
print(y_list)
plt.plot(x_list,y_list)
plt.show()