#this program finds out words!
string = input ("Please Enter Your Text ( End by Dot) :")
space =0
text=''
mylist=[]
i=0
while i<=len(string):
    for l in string:
        if l==' ':
            space+=1
        else:
            text=text+l 
    i+=1 
    mylist.append(text)

print(space)
print(text)
print(mylist,':',mylist.count(text))
        
