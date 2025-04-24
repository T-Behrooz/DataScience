import numpy as np
import pandas as pd
import math as m


#------------------------------------------------------------------------------
def domination(df,I,O):
    
    mat = df.values[:,1:]
    mat = mat.tolist()
    rows = len(mat) # Height.
    columns = len(mat[0])
    def permute(Mat):
        s = []
        for i in range(rows):
            for j in range(rows):
                if i == j:
                    continue
                s.append([Mat[i],Mat[j]])
        s = np.reshape(s,(rows, rows-1,2,columns))
        return s
    def cal(Res):
        TrueOrFalse = np.empty((len(Res),len(Res[0])))
        for i in range(len(Res)):
            for j in range(len(Res[0])):
                state_input , state_output= True, True
                for k1 in range(I):
                    state_input = state_input and (-Res[i][j][0][k1] >= -Res[i][j][1][k1])
                for k2 in range(I,I+O):
                    state_output = state_output and (Res[i][j][0][k2] >= Res[i][j][1][k2])
                state = state_input and state_output
                if state:
                    TrueOrFalse[i][j] = True
                else:
                    TrueOrFalse[i][j] = False
        return TrueOrFalse

    res = cal(permute(mat))
    temp = np.ones((len(res),1),dtype=bool)
    Result = False
    for i in range(len(res)):
        for j in range(len(res[0])): 
            temp[i] = temp[i] and res[i][j]
            solution = [mat[i] for i in range(len(temp)) if temp[i] == 1]
            Result = Result or temp[i]
    Index =list()
    for i in range(len(solution)):
        for j in range(rows):
            if solution[i]==mat[j]:
                Index.append(df.values[j,0])

    def RemoveDuplicate(x):
      return list(dict.fromkeys(x))
    Index = RemoveDuplicate(Index)
    if Result == False:
        return "There is no solution"
    else: 
         return solution,Index 
#------------------------------------------------------------------------------
def find_dominator_in_set(df,I,O):    
    res=dict();res.clear()    
    for row1 in df.index:
        dominated=[];dominated.clear()
        dmuo=df.filter(items=[row1],axis=0)
        res[row1]=''
        for row2 in df.index:
            if (row1!=row2):
                temp1=[];temp2=[];temp1.clear();temp2.clear();
                temp=[];temp.clear()
                for i in range(1,I+1):
                    test=df.filter(items=[row2],axis=0)
                    if -test.iloc[0,i]>=-dmuo.iloc[0,i]:
                        temp1.append(True)
                    else:
                        temp1.append(False)
                for j in range(I+1,O+I):
                    if test.iloc[0,j]>=dmuo.iloc[0,j]:
                        temp2.append(True)
                    else:
                        temp2.append(False)
                temp=temp1+temp2
                if (all(temp)==True):
                    dominated.append(row2);
        res[row1]=dominated
    return res
#-------------------------------------------------------------------------------------
def find_dominated_by_dmu(df,dmu,I):       
    dominated=[];dominated.clear()
    row1=dmu.index;
    for row2 in df.index:
            if (row1!=row2):
                temp1=[];temp2=[];temp1.clear();temp2.clear();
                temp=[];temp.clear()
                for i in range(1,I+1):
                    test=df.filter(items=[row2],axis=0)
                    if -test.iloc[0,i]<=-dmu.iloc[0,i]:
                        temp1.append(True)
                    else:
                        temp1.append(False)
                for j in range(I+1,len(df.columns)):
                    if test.iloc[0,j]<=dmu.iloc[0,j]:
                        temp2.append(True)
                    else:
                        temp2.append(False)
                temp=temp1+temp2
                if (all(temp)==True):
                    dominated.append(row2);
    return dominated
#----------------------- math calculation of vector size -----------------------------------
def math_size_of_vector(dmu,I,O):
    var=list();var.clear()
    for e in range(0,O+I):
        var.append(dmu[e]*dmu[e])
    v_size=m.sqrt(sum(var))
    return v_size
#----------------------- numpy calculation of vector size -----------------------------------
def size_of_vector(dmu, I, O):
    var = np.square(dmu)
    v_size = np.sqrt(np.sum(var))
    return v_size
#--------------------------finding the ideal DMU -------------------------------------     
def find_IDMU(df):
    t=0
    for i in df.columns:
        t+=1
        if i =="O1":
            I=t-2
    IDMU=dict()
    IDMU.clear()
    IDMU['dmus']='IDMU'
    for i, col in enumerate(df):
        if(i)>0 and i<=I :
           IDMU.update({col:df[col].min()})
        elif i>I and i<len(df.columns):
           IDMU.update({col:df[col].max()})
    IDMU1=pd.DataFrame([IDMU],columns=IDMU.keys());
    return IDMU1        
#--------------------------finding DMUI and DMUO sets-------------------------------------            
def filter_dmuo_dmui_sets(df,I,O):
    dfI=df.iloc[:,range(1,I+1)]
    dfO=df.iloc[:,range(I+1,len(df.columns))] 
    # finding the all values of  min in columns
    inputFilter=pd.DataFrame()
    for i,j in dfI.min().items():
       inputFilter=inputFilter.append(df.loc[df[i] == j],ignore_index = False)\
           .drop_duplicates() 
           
    #  finding the all values of  max in columns
    outputFilter=pd.DataFrame()
    for i,j in dfO.max().items():
        outputFilter=outputFilter.append(df.loc[df[i] == j],ignore_index = False)\
            .drop_duplicates() 

    return inputFilter,outputFilter
#---------------------------Remove Dominated dmu  sets from main dataFrame ----------------
def removeDominatedDmus(maindf,dmuSet):
    remove_df=pd.DataFrame(maindf)
    for i in range(len(dmuSet)):
        remove_df.drop(dmuSet[i],axis=0,inplace=True)  
    return remove_df
#------------------------returns vector elements ------------------------------------------
def return_vector_elements(dmu1,dmu2,I,O):
    var=list();var.clear()
    var.append(dmu1.iloc[0,0])
    var.append(dmu2.iloc[0,0])
    for e in range(1,O+I+1):
        var.append(dmu1.iloc[0,e]-dmu2.iloc[0,e])
    return var
#------------------------returns angles of vectors with main vector ----------------------
def vector_angle(dmu1,dmu2,I,O):
    pi=22/7
    if len(dmu1)==len(dmu2):
      bottom =ml.size_of_vector(dmu1,I,O)*ml.size_of_vector(dmu2,I,O)
    var=list();var.clear()
    for e in range(0,O+I):
        var.append(dmu1[e]*dmu2[e])
    top =(sum(var))
    if bottom!=0:
        angle = ((m.acos(top/bottom))*(180/pi))
    else:
        angle=360
    return angle
#------------------------------------------------------------------------------
def choice_dmui_or_dmuo_from_multiples(newdataset,I,O):
    eff=dict();eff.clear()
    for i in newdataset.index:
        inputs=list();inputs.clear()
        outputs=list();outputs.clear()
        newtest=newdataset.filter(items=[i],axis=0)
        for j in range(1,I+1):
            inputs.append(newtest.iloc[0,j])
            bottom=sum(inputs)
        for r in range(I,len(newtest.columns)):
            outputs.append(newtest.iloc[0,r])
            top=sum(outputs)
        eff[newtest.iloc[0,0]]=top/bottom
    eff=pd.DataFrame(eff.items())
    maximun=eff[1].max()
    result1=(eff[eff[1]==maximun])
    result=newdataset.loc[newdataset['DMUS'] == result1.iloc[0,0]]
    return result