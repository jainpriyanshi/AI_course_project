from preprocessing import TextPreprocessor 
import pandas as pd
postfiles = ['AI','AImeta','ComputerGraphic','ComputerGraphicmeta','CS','CSmeta','DataScience','DataSciencemeta']

for files in postfiles:
    print(files)
    data = pd.read_csv('csv/'+ files +'.csv')
    data_agg = TextPreprocessor(n_jobs=-1).transform(data,'Text')
    print(data.isna().sum())
    data_agg.to_csv('csv/' + files+ '.csv',encoding='utf-8',index=False)
