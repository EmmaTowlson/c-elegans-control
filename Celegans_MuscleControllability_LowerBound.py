
###################################################################################
###
### Obtain the Lower Bound of the number of controllable muscles when no ablations
###
###################################################################################


import networkx as nx
import random
import time
import re
from random import shuffle
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow import preflow_push
from networkx.algorithms.flow import edmonds_karp


###################################
## the first subgraph

G = nx.DiGraph()

depth = 50
# the value of depth should be large enough

fp = open('network_adult_NoMuscles.dat','r')
for line in fp:
        a = line.split('\t')[0]
        b = line.split('\t')[1]
        b = b.split('\n')[0]
        c = a + 'a1'
        d = b + 'a1'
        if G.has_node(c) == False:
                for i in range(1,depth+1):
                        G.add_edge(a+'a'+str(i),a+'b'+str(i),capacity=1)
        if G.has_node(d) == False:
                for i in range(1,depth+1):
                        G.add_edge(b+'a'+str(i),b+'b'+str(i),capacity=1)
        if G.has_edge(a+'b'+str(2),b+'a'+str(1)) == False:
                for i in range(2,depth+1):
                        G.add_edge(a+'b'+str(i),b+'a'+str(i-1),capacity=1)

fp.close()

# anterior gentle touch
sensor = ['ALML','ALMR','AVM']
#posterior gentle touch
#sensor = ['PLML','PLMR']   
for k in range(0,len(sensor)):
        for i in range(1,depth+1):
                G.add_edge('SOURCE',sensor[k]+'a'+str(i),capacity=100)
                
enn = []
fp = open('neurons_connected_to_muscles_adult.txt','r')
for line in fp:
        s = line.split('\n')[0]
        enn.append(s)
        G.add_edge(s+'b1','SINK',capacity=100)
fp.close()             

flow_value, flow_dict = nx.maximum_flow(G,'SOURCE','SINK')

if flow_value == len(enn):
        print('OK!')
del G



#############################
## the second subgraph

G = nx.DiGraph()

depth = 5
# the value of depth should be large enough, but for the case here 5 is enough

fp = open('neuron_muscle_connections.txt','r')
for line in fp:
        a = line.split('\t')[0]
        b = line.split('\t')[1]
        b = b.split('\n')[0]
        c = a + 'a1'
        d = b + 'a1'
        if G.has_node(c) == False:
                for i in range(1,depth+1):
                        G.add_edge(a+'a'+str(i),a+'b'+str(i),capacity=1)
        if G.has_node(d) == False:
                for i in range(1,depth+1):
                        G.add_edge(b+'a'+str(i),b+'b'+str(i),capacity=1)
        if G.has_edge(a+'b'+str(2),b+'a'+str(1)) == False:
                for i in range(2,depth+1):
                        G.add_edge(a+'b'+str(i),b+'a'+str(i-1),capacity=1)

fp.close()

for k in range(0,len(enn)):
        for i in range(1,depth+1):
                G.add_edge('SOURCE',enn[k]+'a'+str(i),capacity=100)
                
fp = open('muscles_adult.txt','r')
for line in fp:
        s = line.split('\n')[0]
        G.add_edge(s+'b1','SINK',capacity=100)
fp.close()

flow_value, flow_dict = nx.maximum_flow(G,'SOURCE','SINK')

print('Lower Bound is' + '\t' + str(flow_value))

del G
