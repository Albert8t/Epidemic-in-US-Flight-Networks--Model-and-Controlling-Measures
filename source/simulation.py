from local import local
import numpy as np
import networkx as net
import matplotlib.pyplot as plt
import math
import random

#hyper parameters
beta=0.9   #0.9 0.2
gamma=0.18   #0.18  0.12
sigma1=0.005
sigma2=0.01
sigsig=0.3
nu=0.01
infect_decrease=1
mode='nature'   # nature,vaccine,cancel,shutdown, traveler check
vaccine=True
# end of parameters
def origin_point(sims):
    sims['IWD'].E=2
    return sims
def oneFlight(s, e, f):
    up = bool(random.getrandbits(1))
    if up:
        toRatio = f / s.population()
        toS = math.ceil(toRatio * s.S)
        toE = math.ceil(toRatio * s.E)
        toI1 = math.ceil(toRatio * s.I1 * infect_decrease)
        toI2 = math.ceil(toRatio * s.I2)
        toR = math.ceil(toRatio * s.R)
        delS = s.beta * toS * (toI1 + toI2) / f
    else:
        toRatio = f / s.population()
        toS = math.floor(toRatio * s.S)
        toE = math.floor(toRatio * s.E)
        toI1 = math.floor(toRatio * s.I1 * infect_decrease)
        toI2 = math.floor(toRatio * s.I2)
        toR = math.floor(toRatio * s.R)
        delS = s.beta * toS * (toI1 + toI2) / f

    s.depart(toS, toE, toI1, toI2, toR)
    e.arrive(toS-delS, toE+delS, toI1, toI2, toR)

    realFlow=toS+toE+toI1+toI2+R
    return s,e,realFlow

def fly(st, end, f):
    s1,e1,f1=oneFlight(st,end,f)
    s,e,f2=oneFlight(e1,s1,f)





    return s,e,f1+f2



net_file=open("/Users/albert/Desktop/cs485/project/data/data.csv")
G=net.Graph()
G_un=net.Graph()
code=set()
net_file.readline();
for line in net_file.readlines():

    flight=line.split(",")
    name1 = flight[1].split("\"")
    name2 = flight[2].split("\"")
    if float(flight[0])>400:
        G.add_edge(name1[1],name2[1],weight=float(flight[0])/365)
        G_un.add_edge(name1[1],name2[1])
        if name1[1] not in code:
            code.add(name1[1])
        if name2[1] not in code:
            code.add(name2[1])

between=net.edge_betweenness(G_un)
be=net.edge_betweenness(G)
jaccard=net.jaccard_coefficient(G)
locals=dict()
weight=dict()
for city in code:
    weight[city]=0
for s,e in G.edges():
    weight[e]+=G.get_edge_data(s,e)['weight']
    weight[s]+=G.get_edge_data(s,e)['weight']


jacc=dict()
for u,v,j in jaccard:
    jacc[(u,v)]=j
print(G.degree())
degree_diff=dict()
degree_prod=dict()
for a,b in G.edges():
    degree_diff[(a,b)]=abs(G.degree[a]-G.degree[b])
    degree_prod[(a,b)]=G.degree[a]*G.degree[b]



sorted_weight = sorted(weight, key=weight.__getitem__)



sorted_bt=sorted(between, key=between.__getitem__)
sorted_jd = sorted(jacc, key=jacc.__getitem__)
sorted_diff = sorted(degree_diff, key=degree_diff.__getitem__)
sorted_prod=sorted(degree_prod,key=degree_prod.__getitem__)
# the sorted removal stegtagy
print(len(sorted_bt),len(sorted_jd),len(sorted_diff),len(sorted_prod))
def remove_link(G, dicts):
    num=len(dicts)*0.9
    for i,(u,v) in enumerate(dicts):

        if i>num:
            G.remove_edge(u, v)
    return G
def remove_hub(G, dicts):
    target=len(G.edges())
    for city in reversed(sorted_weight):
        G.remove_node(city)
        if len(G.edges())<=target:
            break
    return G
print(len(G.edges))
#G=remove_link(G,sorted_prod)
G=remove_hub(G,sorted_weight)

print(len(G.edges))





locals=dict()
for city in code:
    locals[city]=local(city,beta,gamma,sigma1,sigma2,sigsig,nu,False)
#print(locals.keys())


pass_flow=list()
slist=list()
elist=list()
i1list=list()
i2list=list()
ilist=list()
rlist=list()

locals=origin_point(locals)

max=0;
maxday=0
for day in range(365):
    alert_city=0
    actual=0
    plan=0
    S=0
    E=0
    I1=0
    I2=0
    R=0
    for sim in locals:  #used to keep record of population
        local = locals[sim]
        S+=local.S
        E+=local.E
        I1+=local.I1
        I2+=local.I2
        R+=local.R
    #print(S,E,I1,I2,R,day)
    if I1+I2>max:
        max=I1+I2
        maxday=day

    for sim in locals:
        local=locals[sim]
        if local.Alert():
            #print(code_dict[sim],"alert dected")
            alert_city+=1
            if vaccine:
                local.vaccine_propogate()
            else:
                local.nature_propogate()
            #print("sick",sim,local.I1)
        else:
            local.nature_propogate()

    slist.append(S)
    elist.append(E)
    i1list.append(I1)
    i2list.append(I2)
    ilist.append(I1+I2)
    rlist.append(R)

    for flight in G.edges():
        origin=flight[0]
        oriSim=locals[origin]
        destini=flight[1]
        desSim=locals[destini]
        halfFlow=G.get_edge_data(origin,destini)['weight']/2
        plan+=2*halfFlow
        if mode == 'nature':
            newOri, newDest,flow = fly(oriSim, desSim, halfFlow)
            locals[origin]=newOri
            locals[destini]=newDest
            actual += flow
        elif mode == 'cancel':
            print("to be filled")
    pass_flow.append(actual/plan)



with open('7.txt', 'w+') as f:
    for item in ilist:
        f.write("%s\n" % item)

#plt.plot(slist)
plt.subplot(211)
plt.title("Experiment 8 Infected population over 4 year")
plt.plot(i1list,label='infected with symptom')
plt.plot(i2list,label='infected without symptom')
plt.plot(ilist,label='total infected')
plt.legend()
#plt.plot(rlist)
plt.subplot(212)
plt.title("Exposed population over 4 year")
plt.plot(elist,label='exposed')
plt.show()
print(len(code))
print("peak infected population is at %s at day %s"%(max,maxday))



