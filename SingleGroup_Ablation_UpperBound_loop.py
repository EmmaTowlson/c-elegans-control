######################################################################
###  Code for the paper Nature 550, 519-523 (2017).                ###
###                                                                ###
###  Obtain the upper bound of muscle controllability after        ###
###  ablating each neuron group, by calculating the max flow in    ###                                ###
###  the linking graph.                                            ###
###                                                                ###
###  Python 2.7.12                                                 ###
###                                                                ###
###  last update Sept. 7, 2017                                     ###
######################################################################


import networkx as nx
import random
import time
import re
from random import shuffle


# read the connectome data of adult worm
G = nx.DiGraph()
fo = open('network_adult.txt','r')
for line in fo:
    s = line.split('\n')[0]
    ss = s.split('\t')
    a = ss[0]
    b = ss[1]
    G.add_edge(a,b)
fo.close()

sensor = ['AVM','ALML','ALMR']
#the sensory neuron set can be changed to: sensor = ['PLML','PLMR']

# test reachability of the nodes
reachable = []
for na in sensor:
    a = nx.descendants(G,na)
    for b in a:
        if b not in reachable:
            reachable.append(b)
print('\n')
print('Unreachable nodes:')
for a in G.nodes():
    if a not in reachable:
        print(a)

# build the linking graph of the connectome
H = nx.DiGraph()
depth = 120
## note that the depth should be larger than the number of target nodes
## i.e. here the number of muscles. After simple tests, we find that
## depth = 120 is far enough for assessing muscle controllability.

for ee in G.edges():
    a = ee[0]
    b = ee[1]
    c = a + 'a1'
    d = b + 'a1'
    if H.has_node(c) is False:
            for i in range(1,depth+1):
                    H.add_edge(a+'a'+str(i),a+'b'+str(i),capacity=1)
    if H.has_node(d) is False:
            for i in range(1,depth+1):
                    H.add_edge(b+'a'+str(i),b+'b'+str(i),capacity=1)
    if H.has_edge(a+'b'+str(2),b+'a'+str(1)) is False:
        for i in range(2,depth+1):
                H.add_edge(a+'b'+str(i),b+'a'+str(i-1),capacity=1)

## add 'Source' nodes into the linking graph
for k in range(0,len(sensor)):
    for i in range(1,depth+1):
        H.add_edge('SOURCE',sensor[k]+'a'+str(i),capacity=100)

## add the 'Sink' node
output = []
fp = open('muscles_adult.txt','r')
for line in fp:
    nn = line.split('\n')[0]
    H.add_edge(nn+'b1','SINK',capacity=100)
    output.append(nn+'b1')
fp.close()


# The upper bound of muscle controllability for the healthy worm
time1 = time.clock()
flow_value, flow_dict = nx.maximum_flow(H, 'SOURCE', 'SINK')
time2 = time.clock()
print('If no ablation:')
print('time == ' + str(time2-time1))
print(flow_value)
print('\n')


# The upper bound of muscle controllability when ablating each neuron group
fp = open('neuron_group_adult.txt','r')
fo = open('result_anterior_SingleGroup_Ablation_adult_UpperBound_loop.txt','w')
tmp = 1;
for line in fp:
    s = line.split(' ')
    print('If ablating neuron group ' + s[len(s)-2] + ' :')
    ## To print the result, here we use the single neuron s[0] to denote the
    ## neuron group s, for ease.    

    R = H.copy()
    for i in range(1,depth+1):
        for j in range(0,len(s)-1):
            a = s[j] + 'a' + str(i)
            b = s[j] + 'b' + str(i)
            if a in R.nodes():
                R.remove_node(a)
                #print(s[j] + 'a' + str(i))
                R.remove_node(b)
                #print(s[j] + 'b' + str(i))
    time1 = time.clock()
    flow_value, flow_dict = nx.maximum_flow(R, 'SOURCE', 'SINK')
    time2 = time.clock()
    #print(tmp)
    print('time == ' + str(time2-time1))
    print(s)
    print(flow_value)
    print('\n')
    ss = s[0]+'\t'+str(flow_value) + '\n'
    fo.write(ss)
    ## To write the result, here we use the single neuron s[0] to denote the
    ## neuron group s, for ease.
    tmp = tmp + 1
    del(R)
    
fp.close()
fo.close()

    
