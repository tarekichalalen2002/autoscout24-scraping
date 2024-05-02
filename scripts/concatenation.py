import os
import pandas as pd
file_names = os.listdir('../separated-results')
df = pd.concat([pd.read_csv(f'../separated-results/{file_name}') for file_name in file_names])
df.to_csv('../final-result/autoscout-brut-data.csv', index=False)