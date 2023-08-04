from pulp import *
from pandas import *
location = ['lashgarak','darband','karimi','saadat_abad','ofateh','Vanak']
D = dict(zip(location,[dict(zip(location, [0, 5.22418658123375, 2.67715850699252, 7.43026341185822, 6.01603928562997,4.53306697821871])),
dict(zip(location, [5.22418658123375, 0, 3.08724302354918, 3.11136568655155, 4.04371978181138,1.71611925969366])),
dict(zip(location, [2.67715850699252, 3.08724302354918, 0, 4.7815542075369, 3.48806789681937, 1.92480524745842])),
dict(zip(location, [7.43026341185822, 3.11136568655155, 4.7815542075369, 0, 2.8314476880489, 2.9023518748279])),
dict(zip(location, [6.01603928562997, 4.04371978181138, 3.48806789681937,2.8314476880489, 0, 2.54533229309125])),
dict(zip(location, [4.53306697821871, 1.71611925969366, 1.92480524745842, 2.9023518748279, 2.54533229309125, 0]))]))
p = 2
X = LpVariable.dicts('X_%s_%s', (location,location),cat = 'Binary',lowBound = 0,upBound = 1)

prob = LpProblem('P Median', LpMinimize)
prob += sum(sum(D[i][j]*X[i][j] for j in location) for i in location)
prob += sum(X[i][i] for i in location) == p
#prob += sum(X[i][j] for j in location) == 1 for i in location
#prob += X[i][j] <= X[j][j] for i in location for j in location
for i in location:
    prob += sum(X[i][j] for j in location) == 1

for i in location:
    for j in location:
        prob += X[i][j] <= X[j][j]
prob.writeLP("p-median.lp")
print(prob)
prob.solve()
print("Status:",LpStatus[prob.status])
print("Objective:" ,value(prob.objective))
for v in prob.variables():
    print (v.name , "=", v.varValue)
#------------------------------------------------------------------------------------------
print(dataframe(D))
