import pandas as pd

df = pd.DataFrame(columns=['A','B','C','D'])

df = df.loc[:, 'B':]

print(df)
