import mylab as ml
import pandas as pd
import numpy as np
df = pd.read_excel('e:\\sample1.xlsx',sheet_name='data')
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
Idmu = ml.find_IDMU(df)
print(" \n Ideal DMU is : \n {} ".format(Idmu)) 

# ------------- finding DMUI and DMUO  ----------------------------------------
#-----------------------DMUOI-------------------------------------------------
setdmui= ml.filter_dmuo_dmui_sets(df,I,O)[0];print("\nDMU I selection:\n",setdmui)
setdmuo= ml.filter_dmuo_dmui_sets(df,I,O)[1];print("\nDMU O selection:\n",setdmuo)

if len(setdmui.index)==1:
    dmu_i=setdmui
    print ("\n DMU_I is :\n {}".format(setdmui))
else: 
    dmu=ml.find_dominator_in_set(setdmui,I,O);
    testI=list();testI.clear()
    for x,y in dmu.items():
        if bool(y) == False:
            testI.append(x);
if len(testI)>1:
       dmu_i=ml.choice_dmui_or_dmuo_from_multiples(setdmui, I, O);
       print("\n DMU_I is chosien  :\n {}".format(dmu_i))
else :
        dmu_i=setdmui.filter(items=[testI[0]],axis=0)
        print("\n DMU_I is :\n {}".format(dmu_i))
#-----------------------DMUO---------------------------------------------------
if len(setdmuo.index)==1:
    dmu_o=setdmuo
    print ("\n DMU_O is :\n {}".format(setdmuo))
else:
    dmu=ml.find_dominator_in_set(setdmuo,I,O);
    testO=list();testO.clear()
    for x,y in dmu.items():
        if bool(y) == False:
            testO.append(x);
if len(testO)>1:
       dmu_o=ml.choice_dmui_or_dmuo_from_multiples(setdmuo, I, O)
       print("\n DMU_O is chosien  :\n {}".format(dmu_o))
else :
        dmu_o=setdmuo.filter(items=[testO[0]],axis=0)
        print("\n DMU_O is :\n {}".format(dmu_o))
#------------------------------------------------------------------------------
DominatedByDmuI= ml.find_dominated_by_dmu(df,dmu_i,I);
print("\n Dominated set of dmus by DMU_I is :\n ",DominatedByDmuI)
DominatedByDmuO= ml.find_dominated_by_dmu(df,dmu_o,I);
print("\n Dominated set of dmus by DMU_O is :\n ",DominatedByDmuO)
#------------------------------------------------------------------------------
DominatedByDmuO.extend(x for x in DominatedByDmuI if x not in DominatedByDmuO)
first_data_set=ml.removeDominatedDmus(df,DominatedByDmuO)
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
    mainvector=ml.return_vector_elements(Idmu,firstDmu,I,O)
    print("\n Main vector :\n{}\n\n\n".format(mainvector))
    angledict=dict();angledict.clear()
    for row in dataset.index:
       print("\n-----------------------------------------------------------\n")
       selected_dmu = dataset.filter(items=[row],axis=0)
       print(" {} selected as start point :\n {}".format(row,selected_dmu))     
       vectorshape=ml.return_vector_elements(selected_dmu,firstDmu,I,O)
       print("\n vector from {} to {} :{}".format(firstDmu.iloc[0,0],selected_dmu.iloc[0,0],vectorshape))
       vectorsize=ml.size_of_vector(vectorshape[2:len(vectorshape)],I,O)  
       print("\n the size of vector is :",vectorsize)
       degree=\
           ml.vector_angle(mainvector[2:len(mainvector)],vectorshape[2:len(vectorshape)],I,O)
       print("\n the angle between the vector and main vector is :{}".\
             format(degree))
       if (degree>=0 and degree<=180):
           angledict[selected_dmu.iloc[0,0]]=degree      
    anglecheck1=pd.DataFrame(angledict.items(),columns=['dmu','angle']);
    
    
    teta=anglecheck1.min(axis=0,numeric_only=True);
    small_teta=anglecheck1.loc[anglecheck1['angle']==teta[0]];print(small_teta)
    eff_dmus.append(small_teta.iloc[0,0]);print(eff_dmus)
    
    
    dataset.drop(dataset[dataset['DMUS']==firstDmu.iloc[0,0]].index,inplace=True);
    firstDmu=dataset[dataset['DMUS']==small_teta.iloc[0,0]] ;print(firstDmu) 
    DominatedBychosenfirstdmu=ml.find_dominated_by_dmu(dataset,firstDmu,I);
    print(DominatedBychosenfirstdmu)
    dataset=ml.removeDominatedDmus(dataset,DominatedBychosenfirstdmu);
    print(dataset)
    ii+=1
    print(angledict)
    print(eff_dmus)
    print('\n ------------------------------------------ :',ii)
    s=input('press a key!!!!!')
    if s=='y':   
       pass
#################################
    if degree==0 or dataset.empty:
       condition=False
       
for x in dataset.index:
    eff_dmus.append(dataset.iloc[0,0])
print("the efficent set of Dmus is :",eff_dmus)
#--------------------------------------------------------------------------------------

