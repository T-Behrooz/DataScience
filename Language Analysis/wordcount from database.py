import pyodbc
def count_words(y) :
    space = 0
    letters = 0
    temp1 = []
    temp2 = []

    for i, j in enumerate(y):
        if y.count(j) == 1:
            print(j + " = ", y.count(j))
        else:
            if temp1.count(j) == 0:
                temp1.append(j)
                temp2.append(y.count(j))
    for r, q in enumerate(temp1):
        print(temp1[r] + " = ", str(temp2[r]))

    # -----------------------------------------------------------------

    # Counting the number of characters and spaces
    # for k in string:
    #     if k == ' ':
    #         space += 1
    #     else:
    #         letters += 1

    # ----------------------------------------------------------------
    print("--------------------------------------")
    print("تعداد فاصله ها برابر است با :", space)
    print("--------------------------------------")
    print("تعداد حروف برابر است با :", letters)
    print("--------------------------------------")
    print("تعداد کلمات برابر است با :", i + 1)
    # print("--------------------------------------")
con=pyodbc.connect("DRIVER={SQL Server};SERVER=localhost;DATABASE=sanj;UID=sa;PWD=123")
do = con.cursor()
space = 0
letters = 0
temp1 = []
temp2 = []
text = []
# row = do.execute("select trade_name from contracts")
row0 = do.execute("select trade_name from contracts").fetchall()
print(type(row0))
for _ in range(len(row0)):
    text.append(row0[_][0])
text1 = " ".join(str(x) for x in text)
text = text1.split(" "or "\n")
count_words(text)

