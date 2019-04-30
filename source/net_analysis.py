from local import local
import numpy as np
import networkx as net
import matplotlib.pyplot as plt
import math
import random
net_file=open("/Users/albert/Desktop/cs485/project/data/data.csv")
G=net.Graph()
G_un=net.Graph()
code=set()
net_file.readline();
for line in net_file.readlines():

    flight=line.split(",")
    if float(flight[0])>400:
        G.add_edge(flight[1],flight[2],weight=float(flight[0])/365)
        G_un.add_edge(flight[1],flight[2])
        if flight[1] not in code:
            code.add(flight[1])
        if flight[2] not in code:
            code.add(flight[2])




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

for air in reversed(sorted_weight):

