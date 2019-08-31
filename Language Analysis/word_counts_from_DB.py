import pyodbc
import xlsxwriter
def words_count(string):
    row = 0
    col = 0
    space = 0
    letters = 0
    temp1 = []
    temp2 = []
    path = input("Enter Destination Path : ")
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'لغت')
    worksheet.write(0, 1, 'تعداد')
    y = string.split(" " or "\n")
    # Counting the Frequency of words in list
    # -----------------------------------------------------------------
    for i , j in enumerate(y):
        if y.count(j) == 1:
            print(j + " = ", y.count(j))
        else:
            if temp1.count(j) == 0:
                temp1.append(j)
                temp2.append(y.count(j))
    for r, q in enumerate(temp1):
        print(temp1[r] + " = ", str(temp2[r]))
        worksheet.write(row+1, col, temp1[r])
        worksheet.write(row+1, col + 1,temp2[r])
        row += 1
    workbook.close()
    # -----------------------------------------------------------------
    # Counting the number of characters and spaces
    for k in string:
        if k == ' ':
            space += 1
        else:
            letters += 1
    # ----------------------------------------------------------------
    print("--------------------------------------")
    print("تعداد فاصله ها برابر است با :", space)
    print("--------------------------------------")
    print("تعداد حروف برابر است با :", letters)
    print("--------------------------------------")
    print("تعداد کلمات برابر است با :", i + 1)
    print("--------------------------------------")


con = pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=sanj;UID=sa;PWD=123")
do = con.cursor()
row = do.execute("select trade_name from contracts where year1 =1397 ")
word_list = []
for i in row :
    word_list.append(i[0])
string = " ".join(str(x) for x in word_list)
words_count(string)
con.close()