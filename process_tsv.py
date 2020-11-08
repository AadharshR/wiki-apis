import pandas as pd 
tsv_file='name.tsv'
data=pd.read_table(tsv_file,sep='\t')
df = data['name'].unique().tolist()
s = pd.Series(df)
s.to_csv('processed_output.csv',index=False)