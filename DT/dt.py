# Receive program argument values
import sys

dt_train_txt = sys.argv[1]
dt_test_txt = sys.argv[2]
dt_result_txt = sys.argv[3]

import pandas as pd
data = pd.read_csv(dt_train_txt, sep = "\t", engine='python', encoding = "cp949")
data_test = pd.read_csv(dt_test_txt, sep = "\t", engine='python', encoding = "cp949")

from Decision_Tree import Gain_dt
from Decision_Tree import result_gain
from Decision_Tree import Gini_dt
from Decision_Tree import result_gini

if dt_train_txt == 'dt_train.txt':
    temp = Gain_dt
    tree = temp.DT_train(data)
    result_gain.save(tree, data, data_test)
else:
    temp = Gini_dt
    tree = temp.DT_train(data)
    result_gini.save(tree, data, data_test)