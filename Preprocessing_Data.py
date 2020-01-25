import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split,KFold



#load data
df_merge_s = pd.read_csv('train_merge.csv', index_col=0)
print('df_merge_s shape:', df_merge_s.shape)


#Find the columns with over 20% missing values
for cols in df_merge_s.columns[2:]:
    if df_merge_s[cols].value_counts(normalize = True, dropna = False).values[0]> 0.2:
        print(df_merge_s[cols].value_counts(normalize = True, dropna = False)*100)
        print('-'*90)
        print('-'*90)



cols_drop_merge_s = [cols for cols in df_merge_s.columns if df_merge_s[cols].isnull().sum()/ df_merge_s.shape[0] > 0.1]
print(cols_drop_merge_s)

##Drop the columns
drop_cols = cols_drop_merge_s
df_merge_s.drop(drop_cols, axis = 1, inplace = True)
df_merge = df_merge_s
df_merge = df_merge.drop(columns=['TransactionID'])
print('dfmerge_columns',df_merge.columns)
print("df_merge shape:", df_merge.shape)




#Encoding
cat_list = [cols for cols in df_merge.columns if df_merge[cols].dtype == 'O']
print(cat_list)
from sklearn import preprocessing
for cat in cat_list:
    if cat in df_merge.columns:
        le = preprocessing.LabelEncoder()
        le.fit(list(df_merge[cat].astype(str).values))
        df_merge[cat] = le.transform(list(df_merge[cat].astype(str).values))

#fillna
df_merge = df_merge.fillna(-999)


print(df_merge.columns.values)

#Standardardize
from sklearn.preprocessing import StandardScaler
data1 = df_merge
scaler = StandardScaler()
print(scaler.fit(data1))
StandardScaler(copy=True, with_mean=True, with_std=True)
print(scaler.mean_)
df_merge_s = scaler.transform(data1)
print(df_merge)

#pca for v feature

df = df_merge
def PCA_change(df, cols, n_components, prefix='PCA_', rand_seed=4):
    pca = PCA(n_components=n_components, random_state=rand_seed)

    principalComponents = pca.fit_transform(df[cols])

    principalDf = pd.DataFrame(principalComponents)

    df.drop(cols, axis=1, inplace=True)

    principalDf.rename(columns=lambda x: str(prefix) + str(x), inplace=True)

    df = pd.concat([df, principalDf], axis=1)

    return df



from sklearn.preprocessing import minmax_scale
from sklearn.decomposition import PCA




mas_v = df_merge.columns[24: ]
for col in mas_v:
    df[col] = df[col].fillna((df[col].min() - 2))
    df[col] = (minmax_scale(df[col], feature_range=(0, 1)))

df = PCA_change(df, mas_v, prefix='PCA_V_', n_components=30)

df.to_csv('df_pca.csv')


