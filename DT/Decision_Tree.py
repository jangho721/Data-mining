import pandas as pd
import numpy as np
import math

class Node:
    
    def __init__(self, data):
        self.att = None
        self.data = data
        self.childs = []
        self.col = None
        
class att_selection:
    
    def info(data):
        temp = 0
        Data_size = len(data)
        Class_counting = data[data.columns[-1]].value_counts()
        Prob = Class_counting/Data_size

        for i in Prob:
            temp += -i*math.log2(i)

        return temp

    def infoA(data, colA):
        temp = 0
        Data_size = len(data)

        for i in data[colA].unique():
            temp_1 = data[colA] == i
            temp += (len(data[temp_1])/Data_size) * att_selection.info(data[temp_1])

        return temp

    def Gain(data,colA):
        Gain = att_selection.info(data) - att_selection.infoA(data,colA)

        return Gain

    def splitInfoA(data, colA):
        temp = 0
        Data_size = len(data)

        for i in data[colA].unique():
                temp_1 = data[colA] == i
                Divide_D = len(data[temp_1])/Data_size
                temp += -(Divide_D) * math.log2(Divide_D)

        return temp

    def Gain_ratio(data, colA):
        Gain_ratio = att_selection.Gain(data, colA)/att_selection.splitInfoA(data, colA)

        return Gain_ratio

    def gini(data):
        temp = 0
        Data_size = len(data)
        Class_counting = data[data.columns[-1]].value_counts()
        Prob = Class_counting/Data_size

        for i in Prob:
            temp += i**2

        gini = 1 - temp

        return gini

    def make_subset(data, colA):
        a = []
        colA_element = list(data[colA].unique())
        x = len(colA_element)

        for i in range(1 << x):
            a.append(set([colA_element[j] for j in range(x) if (i & (1 << j))]))

        del a[len(a)-1]
        del a[0]

        return a

    def giniA(data, colA):
        dic = {}
        a = []
        Data_size = len(data)
        all_element = set(data[colA].unique())
        subset = att_selection.make_subset(data, colA)

        for i in subset:
            D_1 = data[data[colA].isin(i)]
            D_2 = data[data[colA].isin(all_element-i)]
            # data[(data['income'] == 'low') | (data['income'] == 'high')]
            giniA = (len(D_1)/Data_size)*att_selection.gini(D_1) + (len(D_2)/Data_size)*att_selection.gini(D_2)
            a.append(giniA)

        ele = subset[a.index(min(a))]
        dic[min(a)] = ele

        return dic

    def gini_delta(data, colA):
        gini_delta = att_selection.gini(data) - list(att_selection.giniA(data, colA).keys())[0]

        return gini_delta

    def AttributeSelection_gini(data, col):
        gain_arr = {}
        for i in col:
            gain_arr[i] = att_selection.gini_delta(data,i)

        return gain_arr
    
    def AttributeSelection_Gain(data, col):
        gain_arr = {}
        for i in col:
            gain_arr[i] = att_selection.Gain(data,i)

        return gain_arr

class Gini_dt:
    
    def DT_train(data):
        col = data.columns[0:len(data.columns)-1]

        if len(data[data.columns[len(data.columns)-1]].unique()) == 1:
            root = None
            pass
        else:
            root = Node(data)
            att_value = att_selection.AttributeSelection_gini(data, col)
            root.att = max(att_value, key= lambda x : att_value[x])

            all_temp = set(data[root.att].unique())
            temp = list(att_selection.giniA(data, root.att).values())[0]
            other_temp = all_temp - temp
            L = [temp, other_temp]


            temp_2 = col[:]
            temp_2 = list(temp_2)
            temp_2.remove(root.att)

            for i in L:
                temp_1 = data[root.att].isin(i)
                child = Node(data[temp_1])
                root.childs.append(child)
                child.col = temp_2

            for i in range(len(root.childs)):
                Gini_dt.Decision_Tree(root.childs, root.childs[i], data)

            return root

    def Decision_Tree(childs ,child, data):
        if len(child.data[child.data.columns[len(child.data.columns)-1]].unique()) == 1 or len(childs) == 0 or len(child.col) == 0:
            root = None
            pass
        else:
            root = child
            att_value = att_selection.AttributeSelection_gini(root.data, root.col)
            root.att = max(att_value, key = lambda x : att_value[x])

            all_temp = set(data[root.att].unique())
            temp = list(att_selection.giniA(data, root.att).values())[0]
            other_temp = all_temp - temp
            L = [temp, other_temp]

            temp_2 = root.col[:]
            temp_2.remove(root.att)

            for i in L:
                temp_1 = root.data[root.att].isin(i)
                c = Node(root.data[temp_1])
                root.childs.append(c)
                c.col = temp_2

            for i in range(len(root.childs)):
                Gini_dt.Decision_Tree(root.childs, root.childs[i], data)

class result_gini:
    
    def Predict(tree, data_test):
        arr = []
        reset = tree.att
        reset_tree = tree
        col = tree.att
        for i in range(len(data_test)):

            while True:
                att_val = data_test.iloc[i][col]
                for j in range(len(tree.childs)):
                    if att_val in tree.childs[j].data[col].unique():
                        tree = tree.childs[j]
                        break

                if len(tree.childs) > 0:
                    col = tree.att
                else:
                    Class = tree.data[tree.data.columns[-1]].value_counts()
                    C = Class.index[list(Class.values).index(max(list(Class.values)))]
                    arr.append(C)
                    col = reset
                    tree = reset_tree
                    break
        return arr
    
    def save(tree ,data, data_test):
        sol = result_gini.Predict(tree, data_test)
        data_test[data.columns[-1]] = sol
        data_test.to_csv('dt_result1.txt',index=False, sep='\t')

class Gain_dt:
    
    def DT_train(data):
        col = data.columns[0:len(data.columns)-1]

        if len(data[data.columns[len(data.columns)-1]].unique()) == 1:
            root = None
            pass
        else:
            root = Node(data)
            att_value = att_selection.AttributeSelection_Gain(data, col)
            root.att = max(att_value, key= lambda x : att_value[x])
    #         Att_idx = Att_value.index(max(Att_value))

    #         print(id(col))
    #         print(id(temp))
    #         print(col)
    #         print(temp)
    #         print(col is temp) # 객체는 동일한가?
            temp = col[:]
            temp = list(temp)
            temp.remove(root.att)

            for i in data[root.att].unique():
                temp_1 = i == data[root.att]
                child = Node(data[temp_1])
                root.childs.append(child)
                child.col = temp

            for i in range(len(root.childs)):
                Gain_dt.Decision_Tree(root.childs, root.childs[i])

        return root

    def Decision_Tree(childs ,child):
        if len(child.data[child.data.columns[len(child.data.columns)-1]].unique()) == 1 or len(childs) == 0 or len(child.col) == 0:
            pass
        else:
            root = child
            att_value = att_selection.AttributeSelection_Gain(root.data, root.col)
            root.att = max(att_value, key= lambda x : att_value[x])

            temp = root.col[:]
            temp.remove(root.att)

            for j in root.data[root.att].unique():
                temp_1 = j == root.data[root.att]
                c = Node(root.data[temp_1])
                root.childs.append(c)
                c.col = temp

            for i in range(len(root.childs)):
                Gain_dt.Decision_Tree(root.childs, root.childs[i])

class result_gain:
    
    def Predict(tree, data_test):
        arr = []
        reset = tree.att
        reset_tree = tree
        col = tree.att
        for i in range(len(data_test)):
            while True:
                att_val = data_test.iloc[i][col]
                for j in range(len(tree.childs)):
                    if tree.childs[j].data[col].unique() == att_val:
                        tree = tree.childs[j]
                        break
                if len(tree.childs) > 0:
                    col = tree.att
                else:
                    Class = tree.data[tree.data.columns[-1]].value_counts()
                    # print(type(Class))
                    list(Class.values).index(max(list(Class.values)))
                    C = Class.index[list(Class.values).index(max(list(Class.values)))]
                    arr.append(C)
                    col = reset
                    tree = reset_tree
                    break

        return arr
    
    def save(tree, data , data_test):
        sol_2 = result_gain.Predict(tree, data_test)
        data_test[data.columns[-1]] = sol_2
        data_test.to_csv('dt_result.txt',index=False, sep='\t')