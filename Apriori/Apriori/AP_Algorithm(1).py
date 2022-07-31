#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class PAlgorithm:
    
    def __init__(self, m):
        self.Min_sup = m * 0.01
        self.dblen = 0
        self.k = 0

    # Divide a database into k pieces (local databases called partition)
    def Partition_Database(self, db, k):
        self.dblen = len(db)
        self.k = k
        count= int(len(db)/k)
        
        new_db = [db[i:i + count]
                  for i in range(0, len(db), count)]
        
        return new_db

    # Find a set of frequent items in partition (Scan 1)
    def Scan_one(self, new_db):
        freq_pattern = []
        total = self.dblen
        
        for Partition in new_db:
            local_Min_sup = self.Min_sup / self.k
            # It is possible to replace self.k with len(Partition)/total
            
            Local_freq = self.Apriori(Partition, local_Min_sup)
            freq_pattern.append(Local_freq)
            
        return freq_pattern
    
    # As a representative form of association rule
    # an algorithm to reveal the association between each data based on the frequency of occurrence of the data.
    def Apriori(self, db, Min_sup):
        # Finding L1 
        # L1 : Frequent itemset of size 1
        L_1 = []
        db_length = len(db)
        freq_dict = {}
        
        # Finding C1
        # C1 : Candidate itemset of size 1
        # Counting the frequency of candidates
        for itemset in db:
            for item in itemset:
                if item not in freq_dict.keys():
                    freq_dict[item] = 0
                freq_dict[item] += 1
        
        # Find patterns larger than Min_sup
        # sup = count
        for item, sup in freq_dict.items():
            if sup/db_length >= Min_sup:
                L_1.append([item])
          
        U = []
        U.append(L_1)
        
        # Finding L2, L3, ... , Lk
        i = 0
        while True:
            step_one = self.Self_joining(U[i], i) # step 1
            step_two = self.Pruning(step_one, U[i]) # step 2
            C_k = self.Scan(step_two, db)
            L_k = self.Freq_itemset(C_k, step_two, Min_sup, db_length)
            
            if len(L_k) == 0:
                break
            else:
                U.append(L_k)
            i = i+1
        
        return U
    
    # generate candidates (step 1)
    def Self_joining(self, L, length):
        Candidate = []
        
        # Lk * Lk
        for Lk_1 in L:
            for Lk_2 in L:
                if Lk_1 != Lk_2:
                    unit_1 = set(Lk_1)
                    unit_2 = set(Lk_2)
                    join = unit_1.union(unit_2)
                    if len(join) == length + 2:
                        C = join
                        if C not in Candidate:
                            Candidate.append(C)
        
        return Candidate
    
    # generate candidates (step 2)
    def Pruning(self, Candidate_k, L):
        
        for itemset in Candidate_k:
            for item in itemset:
                temp = itemset.remove(item)
                if temp not in L:
                    Candidate_k.remove(itemset)
                    break
        
        return Candidate_k
    
    # Counting the frequency of candidates
    def Scan(self, Candidate_k, Partition):
        dic = {}
        
        for itemset in Candidate_k:
            temp = 0
            for i in range(len(Partition)):
                if itemset.issubset(Partition[i]) == True:
                    temp = temp + 1
            idx = Candidate_k.index(itemset)
            dic[idx] = temp
        
        return dic
    
    # Finding Lk
    def Freq_itemset(self, Freq_dic, Candidate_k, Min_sup, P_len):
        temp = []
        
        for idx, sup in Freq_dic.items():
            if sup/P_len >= Min_sup:
                temp.append(list(Candidate_k[idx]))
                
        return temp
    
    # Merge local frequent patterns
    def Consolidate(self, Freq_pattern):
        C = []
        
        for local_freq in Freq_pattern:
            for itemset in local_freq:
                for i in itemset:
                    temp = set(i)
                    if temp not in C:
                        C.append(temp)
                        
        return C
    
    # FInd global frequent patterns using local frequent patterns candidate (scan 2)
    def Scan_two(self, Candidates, transection_db):
        dic = {}
        L = []
        
         # Counting the frequency of candidates in the total transaction database (not partition)
        for item_c in Candidates:
            temp = 0
            for item_t in transection_db:
                if item_c.issubset(item_t) == True:
                    temp = temp + 1
            idx = Candidates.index(item_c)
            dic[idx] = temp
            
        total = self.dblen
        
        # Compare Min_sup and support
        for idx, sup in dic.items():
            if sup/total >= self.Min_sup:
                L.append(Candidates[idx])
        
        return L
    
    # Finding a relationship in the form of "x is y" from frequent transaction database
    def Association_rule(self, Freq_db):
        L = []
        
        for i in range(len(Freq_db)):
            if len(Freq_db[i]) != 1:
            # One item cannot create an association
                powerset = self.Make_powerset(Freq_db[i])
                for subset in powerset:
                    partner = Freq_db[i] - subset
                    pair = [subset, partner]
                    L.append(pair)
        
        return L
    
    # Powerset
    # Recursive or (from itertools import combinations)
    def Make_powerset(self, itemset):
        temp = list(itemset)
        n = len(temp)
        L = []
        
        # Using bit operator
        for i in range(1 << n): # << : shift
            s = set([])
            for j in range(n):
                value = i & (1 << j) # & : and
                if value != 0:
                    s.add(int(temp[j]))
            L.append(s)
        
        L.pop()
        L.pop(0)
    
        return L

    # Calculate support and confidence
    def Cal_sup_conf(self, association_rule, db):
        db_len = len(db)
        dic = {}
        
        for i in association_rule:
            count = 0
            count_2 = 0
            # [itemset] U [associative itemset]
            temp = i[0].union(i[1])
            for j in range(db_len):
                # Counting [itemset] U [associative itemset] (support)
                if temp.issubset(db[j]) == True:
                    count = count +1
                # Counting [itemset] (confidence)
                if i[0].issubset(db[j]) == True:
                    count_2 = count_2 +1
            
            idx = association_rule.index(i)
            dic[idx] = [count, count_2]

        for idx, value in dic.items():
            # rounded to two decimal places
            sup = '%.2f'%round(100*value[0]/db_len,2)
            conf = '%.2f'%round(100*value[0]/value[1],2)
            
            if len(association_rule[idx]) >= 4:
                pass
            else:
                association_rule[idx].append(sup)
                association_rule[idx].append(conf)
        
        return association_rule
    
    # Print the result to a text file
    def Make_output(self, final_L, output):
        f = open(output, 'w')
        
        # itemset -> associative itemset
        for i in final_L:
            for j in i[0:2]:
                count = 1
                # Use braces to represent item sets
                f.write("{")
                for item in j:
                    t = (str(item))
                    f.write(t)
                    if count == len(j):
                        f.write("}\t")
                    else:
                        f.write(",")
                        count += 1
            
            # support(%) and confidence(%)
            for value in i[2:]:
                string_val = str(value)
                f.write(string_val)
                f.write("\t")
            f.write("\n")
        f.close()