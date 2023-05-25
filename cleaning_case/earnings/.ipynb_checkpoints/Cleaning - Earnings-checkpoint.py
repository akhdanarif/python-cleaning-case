#!/usr/bin/env python
# coding: utf-8

# In[7]:


#importing necessary library
import pandas as pd
import numpy as np
import glob
import os
import warnings
warnings.simplefilter('ignore')

#read the files depend on your local directory
files = glob.glob('c:/Users/akhda/Documents/python_porto/cleaning_case/earnings/*.xlsx')

#concatenate multiple files diminished by assigning new column with the filename
df = pd.concat([pd.read_excel(f).assign(Files=os.path.basename(f).split('.')[0]) for f in files])

#make function for the code
def clean_earnings(df):
    
    #change dtype dict
    dtype_dict = {'Order ID': str,
            'Product ID': str,
            'Plan ID': str,
            'Payment ID': str,
            'Commission rate': np.int64}
    
    #change dtype
    df = df.astype(dtype_dict)
    df['Time order created'] = pd.to_datetime(df['Time order created'], dayfirst=True)
    df['Time order delivered'] = pd.to_datetime(df['Time order delivered'], dayfirst=True)
    df['Time Commission Paid'] = pd.to_datetime(df['Time Commission Paid'], dayfirst=True)
    
    #move column account to the first column
    first_column = df.pop('Files')
    df.insert(1, 'Files', first_column)
    
    #lowercase column, replace space with underscore and renaming columns
    newcols = df.columns.str.lower().str.replace(" ","_")
    df.columns = newcols
    df = df.reset_index().drop(columns='index')
    
    #split files column
    split_files = df['files'].str.split(' ', expand=True).drop(columns=0).rename(columns={1:'location', 2:'paid_pending', 3:'period'}).reset_index().drop(columns='index')
    df = pd.concat([split_files, df], axis=1).drop(columns='files').set_index('order_id')

    #change format of content_id
    df['content_id'] = df['content_id'].fillna(0).astype(np.int64).astype(str).str[:-3]
    
    #drop column sub_order_id & content_id
    df = df.drop('sub_orderid', axis=1)
    
    #export to excel
    return df.to_excel('c:/Users/akhda/Documents/python_porto/cleaning_case/earnings/Clean-earnings.xlsx')

clean_earnings(df)

