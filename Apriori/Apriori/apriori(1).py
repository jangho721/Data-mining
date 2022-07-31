#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Receive program argument values
import sys

minimum_sup = int(sys.argv[1])
input_txt = sys.argv[2]
output_txt = sys.argv[3]


# In[ ]:


# Load file
# Preprocessing
f = open(input_txt, 'r')
line = f.readlines()

List = []
for i in range(len(line)):
    line[i] = line[i].replace('\n','')
    line[i]= line[i].split('\t')
    List.append(set(list(map(int, line[i]))))


# In[ ]:


# import the class and function
from AP_Algorithm import PAlgorithm

a = PAlgorithm(minimum_sup)
b = a.Partition_Database(List, 5)
c = a.Scan_one(b)
d = a.Consolidate(c)
e = a.Scan_two(d, List)
f = a.Association_rule(e)
g = a.Cal_sup_conf(f, List)
a.Make_output(g,output_txt)