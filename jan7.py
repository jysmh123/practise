import pandas as pd
import numpy
fec = pd.read_csv('E:\\pythondata\\ch09\\P00000001-ALL.csv',low_memory=False)
unique_cands = fec.cand_nm.unique()
print(unique_cands[1])