import time
import mylabnew as mll
import pandas as pd
start_time = time.time()
df = pd.read_excel('d:\\non_dominated_rows.xlsx',sheet_name='data')
# ------------  finding the number of inputs and outputs --------------------
t=0
for i in df.columns:
    t+=1
    if i =="O1":
        I=t-2
        O=len(df.columns)-I-1
# ------------- getting the Dimentions of dataFrame --------------------------
print("\n your matrix id : {} * {} \n".format( len(df.index),len(df.columns)));
print("\n Your dataset is : \n", df)
# ------------- finding the Iedal DMU ----------------------------------------
Idmu = mll.find_IDMU(df)
print(" \n Ideal DMU is : \n {} ".format(Idmu)) 

# ------------- finding DMUI and DMUO  ----------------------------------------
#-----------------------DMUOI-------------------------------------------------
setdmui= mll.filter_dmuo_dmui_sets(df,I,O)[0];print("\nDMU I selection:\n",setdmui)
setdmuo= mll.filter_dmuo_dmui_sets(df,I,O)[1];print("\nDMU O selection:\n",setdmuo)

if len(setdmui.index)==1:
    dmu_i=setdmui
    print ("\n DMU_I is :\n {}".format(setdmui))
else: 
    dmu=mll.find_dominator_in_set(setdmui,I,O);
    testI=list();testI.clear()
    for x,y in dmu.items():
        if bool(y) == False:
            testI.append(x);
if len(testI)>1:
       dmu_i= mll.choice_dmui_or_dmuo_from_multiples(setdmui, I, O);
       print("\n DMU_I is chosien  :\n {}".format(dmu_i))
else :
        dmu_i=setdmui.filter(items=[testI[0]],axis=0)
        print("\n DMU_I is :\n {}".format(dmu_i))
#-----------------------DMUO---------------------------------------------------
if len(setdmuo.index)==1:
    dmu_o=setdmuo
    print ("\n DMU_O is :\n {}".format(setdmuo))
else:
    dmu=mll.find_dominator_in_set(setdmuo,I,O);
    testO=list();testO.clear()
    for x,y in dmu.items():
        if bool(y) == False:
            testO.append(x);
if len(testO)>1:
       dmu_o=mll.choice_dmui_or_dmuo_from_multiples(setdmuo, I, O)
       print("\n DMU_O is chosien  :\n {}".format(dmu_o))
else :
        dmu_o=setdmuo.filter(items=[testO[0]],axis=0)
        print("\n DMU_O is :\n {}".format(dmu_o))
#------------------------------------------------------------------------------
DominatedByDmuI= mll.find_dominated_by_dmu(df,dmu_i,I);
print("\n Dominated set of dmus by DMU_I is :\n ",DominatedByDmuI)
DominatedByDmuO= mll.find_dominated_by_dmu(df,dmu_o,I);
print("\n Dominated set of dmus by DMU_O is :\n ",DominatedByDmuO)
#------------------------------------------------------------------------------
DominatedByDmuO.extend(x for x in DominatedByDmuI if x not in DominatedByDmuO)
first_data_set=mll.removeDominatedDmus(df,DominatedByDmuI)
first_data_set=mll.removeDominatedDmus(df,DominatedByDmuO)
print("\n ####################################################################")
print("\n starting data set evaluation ... \n",first_data_set)
#------------------------------------------------------------------------------
eff_dmus=list();eff_dmus.clear()
eff_dmus.append(dmu_o.iloc[0,0]);
eff_dmus.append(dmu_i.iloc[0,0]);print(eff_dmus)
firstDmu=dmu_o;
Idmu=Idmu;
dataset=first_data_set;print(dataset)
condition=True
ii=0
while condition:
#################################
    mainvector=mll.return_vector_elements(Idmu,firstDmu,I,O)
    print("\n Main vector :\n{}\n\n\n".format(mainvector))
    angledict=dict();angledict.clear()
    for row in dataset.index:
       print("\n-----------------------------------------------------------\n")
       selected_dmu = dataset.filter(items=[row],axis=0)
       print(" {} selected as start point :\n {}".format(row,selected_dmu))     
       vectorshape=mll.return_vector_elements(selected_dmu,firstDmu,I,O)
       print("\n vector from {} to {} :{}".format(firstDmu.iloc[0,0],selected_dmu.iloc[0,0],vectorshape))
       vectorsize=mll.size_of_vector(vectorshape[2:len(vectorshape)],I,O)  
       print("\n the size of vector is :",vectorsize)
       degree=\
           mll.vector_angle(mainvector[2:len(mainvector)],vectorshape[2:len(vectorshape)],I,O)
       print("\n the angle between the vector and main vector is :{}".\
             format(degree))
       if (degree>=0 and degree<=180):
           angledict[selected_dmu.iloc[0,0]]=degree      
    anglecheck1=pd.DataFrame(angledict.items(),columns=['dmu','angle']);
    
    teta=anglecheck1.min(axis=0,numeric_only=True);
    small_teta=anglecheck1.loc[anglecheck1['angle']==teta[0]];print(small_teta)
    eff_dmus.append(small_teta.iloc[0,0]);print(eff_dmus)
    
    dataset.drop(dataset[dataset['DMUS']==firstDmu.iloc[0,0]].index,inplace=True);
    SecondDmu=dataset[dataset['DMUS']==small_teta.iloc[0,0]] ;print(SecondDmu) 
    DominatedBychosenSecondDmu=mll.find_dominated_by_dmu(dataset,SecondDmu,I);
    print(DominatedBychosenSecondDmu)
    dataset=mll.removeDominatedDmus(dataset,DominatedBychosenSecondDmu);
    #------------------------------------------------------------------
    between=mll.find_between_dmus(SecondDmu,firstDmu,dataset,I);
    print("Between Dmus are :\n",between)
    dataset=mll.removeDominatedDmus(dataset,between);
    #------------------------------------------------------------------
    firstDmu=SecondDmu
    print("\n Datasets :\n",dataset)
    ii+=1
    print(angledict)
    print(eff_dmus)
    print('\n ------------------------------------------ :',ii)
    # s=input('press a key!!!!!')
    # if s=='y':   
    #    pass
#################################
    if degree==0 or dataset.empty:
       condition=False
       
for x in dataset.index:
    eff_dmus.append(dataset.iloc[0,0])
print("the efficent set of Dmus is :",eff_dmus)

end_time = time.time()
# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(" \n Elapsed time: ", elapsed_time, "in seconds")
print("\n Elapsed time: ", elapsed_time/60, "in Mintues")
print("\n Elapsed time: ", elapsed_time/3600, "in Hours")
# Assuming 'eff_dmus' contains the column data you want to export

# Create a DataFrame from the 'eff_dmus' list
eff_dmus_df = pd.DataFrame({'eff_dmus_column': eff_dmus})

# Specify the file path for the Excel file
excel_file_path = 'd:\\efficent_set_of_Raw 1400 Dmus DataSet ( no Zero ).xlsx'

# Export the DataFrame to Excel
eff_dmus_df.to_excel(excel_file_path, index=False)

# =============================================================================
# print(ml.find_between_dmus(dmu_i,dmu_o,df,I))
# dmu1=dmu_i
# dmu2=dmu_o
# removeable=[];removeable.clear()
# n1=dmu1.index[0];print("n1=",n1)
# n2=dmu2.index[0];print("n2=",n2)
# for row in df.index:
#     print(row)
#     if (row!=n1)and(row!=n2):
#             temp1=[];temp2=[];temp1.clear();temp2.clear();
#             temp=[];temp.clear()
#             print(dmu_i)
#             test=df.filter(items=[row],axis=0);print(test.to_string(header=False))
#             print(dmu_o.to_string(header=False))
#             for i in range(1,I+1):
#                 if ((dmu1.iloc[0,i]<=test.iloc[0,i]) and (test.iloc[0,i]<=dmu2.iloc[0,i])):
#                     print(dmu1.iloc[0,i],",",test.iloc[0,i],",",dmu2.iloc[0,i])
#                     temp1.append(True);
#                 else:
#                     temp1.append(False);
#             for j in range(I+1,len(df.columns)):
#                 if ((dmu2.iloc[0,j]<=test.iloc[0,j]) and (test.iloc[0,j]<=dmu2.iloc[0,j])):
#                     temp2.append(True);
#                 else:
#                     temp2.append(False)
#             temp=temp1+temp2;print(temp)
#             if (all(temp)==True):
#                 removeable.append(row);
# print(removeable)
# =============================================================================
