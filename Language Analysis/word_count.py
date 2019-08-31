space = 0
letters=0
string=input("متن مورد نظر را وارد کنيد :")
temp1=[]
temp2=[]
# Salting text to list
y=string.split(" " or "\n")

# Counting the freguency of words in list
#-----------------------------------------------------------------

for i,j in enumerate(y):
   if y.count(j)==1:
      print (j + " = " ,y.count(j))
   else:
      if temp1.count(j) == 0:
          temp1.append(j)
          temp2.append(y.count(j))
for r,q in enumerate (temp1):
            print( temp1[r] + " = " ,str(temp2[r]))

#-----------------------------------------------------------------
   
# Counting the number of characters and spaces
for k in string :
    if k==' ':
       space+=1
    else :
       letters+=1
       
#----------------------------------------------------------------
       
print("--------------------------------------")       
print("تعداد فاصله ها برابر است با :",space)
print("--------------------------------------") 
print("تعداد حروف برابر است با :",letters)
print("--------------------------------------") 
print("تعداد کلمات برابر است با :",i+1)
print("--------------------------------------") 
