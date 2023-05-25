#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import necessary library
import pandas as pd
import numpy as np
import glob
import os
import warnings
warnings.simplefilter('ignore')

#read the files depend on your local directory
files = glob.glob('c:/Users/akhda/Documents/python_porto/cleaning_case/product_analytics/*.xlsx')

#concatenate multiple files diminished by assigning new column with the filename
df = pd.concat([pd.read_excel(f).assign(Files=os.path.basename(f).split('.')[0]) for f in files])

#make function for the code
def all_loc_product_analytics(df):
    
    #reset index
    df.reset_index(inplace=True)
    df.drop(columns='index',inplace=True)
    
    #rename columns
    rename_cols = {}
    for col in df.columns:
        rename_cols[col] = col.rstrip("\xa0")
    df = df.rename(columns=rename_cols)
    
    #separate ID and shop name to new columns and merge
    id_rows = df['Product Info'].str.contains('ID:')
    id_split = df[id_rows]['Product Info'].str.split('ID:', expand=True).rename(columns={1:"Product ID"}).drop(columns=0)
    shop_rows = df['Product Info'].str.contains('Shop name: ')
    shop_split = df[shop_rows]['Product Info'].str.split('Shop name: ',expand= True).rename(columns={1:"Shop name"}).drop(columns=0)
    df = pd.concat([id_split, shop_split, df], axis=1)
    
    #shifting cells and rename column product info
    df['Product ID'] = df['Product ID'].shift(periods=-2)
    df['Shop name'] = df['Shop name'].shift(periods=-1)
    df = df.rename(columns={"Product Info": "Product Name"})
    df = df.dropna()
    
    #remove 'RP', '.', and change to float dtype
    cols = []
    for c in df.columns:
        if c != 'Product Name':
            cols.append(c)
    df[cols] = df[cols].replace({'^Rp':"", '\.': ""}, regex=True)
    
    num = {}
    for c in df.columns:
        if c == 'Revenue' or c == 'Revenue (LIVE)' or c == 'Revenue (Video)' or c == 'Revenue (Showcase)' or c == 'Refunds':
            num[c] = float
    df = df.astype(num)
    
    #math operation and change to integer dtypes
    for cols in df.columns:
        if cols == 'Revenue' or cols == 'Revenue (LIVE)' or cols == 'Refunds' or cols == 'Revenue (Showcase)' or cols == 'Revenue (Video)':
            df[cols] = df[cols].apply(lambda x: x*1000 if x <= 1000000 else x)
            
    num2 = {}
    for c in df.columns:
        if c != 'Product ID' and c != 'Shop name' and c != 'Product Name' and c != 'CTR' and c != 'C_O' and c!= 'Action' and c!= 'Files' and c!= 'Return rate' and c!= 'Negative review rate' and c!= 'Complaint rate':
            num2[c] = np.int64
    df = df.astype(num2)
    
    #set Product ID as index, drop unwanted columns, split 'Files' column
    df = df.set_index('Product ID')
    df = df.drop(columns= ['Action', 'Complaint rate'])
    split_files = df['Files'].str.split(' ', expand=True).drop(columns=1).rename(columns={0:'location', 2:'period'})
    df = pd.concat([split_files, df], axis=1).drop(columns='Files')
    
    #lowercase columns and change the format
    newcols = df.columns.str.lower().str.replace(" ","_").str.replace("(","").str.replace(")","")
    df.columns = newcols
    
    #export to excel
    return df.to_excel('c:/Users/akhda/Documents/python_porto/cleaning_case/product_analytics/Clean - Prod Analytics Apr.xlsx')

all_loc_product_analytics(df)

