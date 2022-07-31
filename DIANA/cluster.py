#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# coordinate = [list(map(float,line[i].replace('\t'," ").split()[1:])) for i in range(len(line))]


# In[ ]:


import time


# In[ ]:


# 시각화
# import matplotlib.pyplot as plt

# scatter = np.array(coordinate)
# x = scatter[:,0]
# y = scatter[:,1]

# plt.figure(figsize=(15, 10))
# plt.scatter(x,y,s = 7)
# plt.show


# In[ ]:


def distance(i,j):
    dist = (((i - j)**2).sum(axis = 1))**(1/2)

    return dist


# In[ ]:


def dist_matrix(coordinate):
    L = []
    size = len(coordinate)

    for i in range(size):
        L.append(distance(coordinate[:,[1,2]],coordinate[i,[1,2]]))
        
    matrix = np.array(L)

    return matrix


# In[ ]:


# mat = dist_matrix(coordinate_np)


# In[ ]:


def avg(mat):
    temp = mat.sum(axis = 0)/(len(mat)-1)
    
    return temp


# In[ ]:


# ave = avg(mat)
# init_obj_idx = np.argmax(ave)
# init_point = coordinate_np[init_obj_idx, :]


# In[ ]:


def dist_ij(i, j_group, coordinate):
    j_group = coordinate[:,[1,2]][j_group,:]
#     j_group = np.delete(coordinate[:,[1,2]], j_group_other, axis=0) # axis = 0 행 / axis = 1 열
    temp = distance(j_group, coordinate[i,[1,2]])
    avg_dij = temp.sum()/len(j_group)
    
    return avg_dij


# In[ ]:


def dist_is(i, s_group, coordinate):
    splinter_group = coordinate[:,[1,2]][s_group,:]
#     splinter_group = np.delete(coordinate[:,[1,2]], j_idx, axis=0)
    temp = distance(splinter_group, coordinate[i,[1,2]])
    avg_dis = temp.sum()/len(splinter_group)
    
    return avg_dis


# In[ ]:


def splinter_group(coordinate, idx_arr, init):
#     idx_arr = idx_arr.astype(np.int64)
    arr = np.array(range(len(idx_arr)))
    splinter_g = [init]
    append = splinter_g.append
    
    while True:
        dic = {}
        for i in range(len(arr)):
            if i in splinter_g:
                pass
            else:
                j_idx = np.delete(arr, splinter_g + [i])

                avg_ij = dist_ij(int(i), j_idx, coordinate)
                avg_is = dist_is(int(i), splinter_g, coordinate)

                dic[avg_ij - avg_is] = i
        
        D_h = max(dic.keys())
        if D_h > 0:
            append(dic[D_h])
        else:
            break
    
    return splinter_g


# In[ ]:


# one = splinter_group(coordinate_np, coordinate_np[:,0], init_obj_idx)


# In[ ]:


# one_idx = coordinate_np[one, 0].astype(np.int64)


# In[ ]:


# whole_idx = np.array(range(len(coordinate_np)))
# remain = list(set(whole_idx) - set(one))


# In[ ]:


# remain_idx = coordinate_np[remain, 0].astype(np.int64)


# In[ ]:


def idx_to_coord(idx, coordinate):
    idx = list(idx)
    coord = coordinate[:,:][idx,:]
    
    return coord


# In[ ]:


def diameter(cluster, coordinate_np):
    clu = idx_to_coord(cluster, coordinate_np)
    
    L = []
    size = len(clu)
    
    for i in range(size):
        L.append(distance(clu[:,[1,2]], clu[i,[1,2]]))
        
    matrix = np.array(L)
    
    diameter = matrix.sum()/(size*(size-1))
    
    return diameter


# In[ ]:


# dia_one = diameter(one, coordinate_np)


# In[ ]:


# dia_remain = diameter(remain, coordinate_np)


# In[ ]:


def save(dic, num):
    for i in range(len(dic)):
        (list(dic.values())[i]).sort()
        with open('input'+str(num)+'_cluster_'+str(i)+'.txt', 'w') as f:
            for line in list(dic.values())[i]:
                f.write(str(line)+"\n")
            f.close()


# In[ ]:


# Receive program argument values
import sys
import numpy as np

input_txt = sys.argv[1]
cluster_num = int(sys.argv[2])

num = int(''.join(ele for ele in input_txt if ele.isdigit()))

data = open(input_txt, 'r')
line = data.readlines()

coord = [list(map(float,line[i].replace('\t'," ").split())) for i in range(len(line))]
coordinate_np = np.array(coord)

dic = {}
n = cluster_num
co = coordinate_np

start = time.time()
while True:
    mat = dist_matrix(co)
    ave = avg(mat)
    init_obj_idx = np.argmax(ave)
    one = splinter_group(co, co[:,0], init_obj_idx)
    whole_idx = np.array(range(len(co)))
    remain = list(set(whole_idx) - set(one))
    one_idx = co[one, 0].astype(np.int64)
    remain_idx = co[remain, 0].astype(np.int64)
    dia_one = diameter(one, co)
    dia_remain = diameter(remain, co)
    dic[dia_one] = list(set(one_idx))
    dic[dia_remain] = list(set(remain_idx))
    
    if len(dic) == n:
        break
    divide = dic[max(dic.keys())]
    co = coordinate_np[divide,:]
    del dic[max(dic.keys())]
#     print('iteration')

save(dic, num)
print(time.time()-start)


# In[ ]:


# temp = 0
# for i in range(len(dic)):
#     temp += len(list(dic.values())[i])
# print(temp)


# In[ ]:


# plt.figure(figsize=(15, 10))
# plt.scatter(coordinate_np[list(dic.values())[0],1],coordinate_np[list(dic.values())[0],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[1],1],coordinate_np[list(dic.values())[1],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[2],1],coordinate_np[list(dic.values())[2],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[3],1],coordinate_np[list(dic.values())[3],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[4],1],coordinate_np[list(dic.values())[4],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[5],1],coordinate_np[list(dic.values())[5],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[6],1],coordinate_np[list(dic.values())[6],2],s = 7)
# plt.scatter(coordinate_np[list(dic.values())[7],1],coordinate_np[list(dic.values())[7],2],s = 7)
# plt.show


# In[ ]:


# from tqdm import tqdm_notebook, tnrange, tqdm

