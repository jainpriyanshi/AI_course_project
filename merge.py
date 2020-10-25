import os
import glob
import pandas as pd
os.chdir("./csv")
extension = 'csv'

all_filenames = ['AI.csv','ComputerGraphic.csv','CS.csv','DataScience.csv']
combined_csv = pd.concat([pd.read_csv(f).head(1500) for f in all_filenames ])
print(combined_csv.shape[0])
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')