import pandas as pd

cols = ['postcode','town','eastings','northings','latitude','longitude','region']


df = pd.read_csv('data_files/cleaned/postcodes_ldn_with_hd.csv', index_col=0)
print(df)

new_row = pd.DataFrame([['E20','Olympic Park District',538208,185027,51.54722,-0.00819,'Greater London']],columns=df.columns)
print(new_row)

new_df = pd.concat([df, new_row]).sort_values('postcode').reset_index(drop=True)

print(new_df.loc[new_df['postcode'].str.startswith('E20',na=False)])

new_df.to_csv('data_files/cleaned/postcodes_ldn_with_hd.csv', index=False)