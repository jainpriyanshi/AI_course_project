import pandas as pd
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))
df = pd.read_csv('./csv/combined_csv.csv')
df.groupby('Topic').Text.count().plot.bar(ylim=0)
plt.show()