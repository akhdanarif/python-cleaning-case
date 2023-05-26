#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing necessary library
import pandas as pd
import numpy as np
import glob
import os
import warnings
warnings.simplefilter('ignore')

#read the files depend on your local directory
files = glob.glob('c:/Users/akhda/Documents/python_porto/cleaning_case/livestream_analytics/*.xlsx')

#concatenate multiple files diminished by assigning new column with the 'account'
df = pd.concat([pd.read_excel(f, header=None).assign(Account=os.path.basename(f).split('.')[0]) for f in files])

#shifting Account column place
df['Account'].iloc[2] = 'Account'

#combining all the code into one function
def cleaning_LS(df):
    
    #promoted column & drop the nulls
    df = df.dropna()
    newcolumns = df.iloc[0]
    df.columns = newcolumns
    
    #filtering the Gross revenue column
    df_filter = df[df['Gross revenue'] =='Gross revenue'].index
    df.drop(df_filter, inplace=True)

    #move account column to first column
    first_column = df.pop('Account')
    df.insert(0, 'Account', first_column)
    
    #remove Rp & change dot to comma
    cols = []
    for c in df.columns:
        if c != 'Account' and c!= 'Livestream' and c!= 'Engagement rate' and c!='CTR' and c!='C_O':
            cols.append(c)
    df[cols] = df[cols].replace({'^Rp':"", '\.': ""}, regex=True)
    
    #create dict for numeric & float
    df_num = {}
    for c in df.columns:
        if c != 'Account' and c != 'Livestream' and c != 'Start time' and c != 'Engagement rate' and c != 'CTR' and c != 'C_O':
            df_num[c] = np.int64
    df_float = {'Engagement rate': float, 'CTR': float, 'C_O': float}
    
    #change data types & reindex
    df = df.astype(df_num)
    df = df.astype(df_float)
    df['Start time'] = pd.to_datetime(df['Start time'])
    df = df.set_index('Account')
    
    #date, time, and hours reconfig
    df[['Date']] = df['Start time'].dt.date
    date_column = df.pop('Date')
    df.insert(3, 'Date', date_column)

    df[['Time']] = df['Start time'].dt.strftime('%H:%M')
    time_column = df.pop('Time')
    df.insert(4, 'Time', time_column)

    df['Hours'] = df['Duration']/3600
    df['Hours'] = df['Hours'].round(decimals=1)
    duration_column = df.pop('Hours')
    df.insert(5, 'Hours', duration_column)
    
    return df.to_excel('c:/Users/akhda/Documents/python_porto/cleaning_case/livestream_analytics/Clean LS.xlsx')

cleaning_LS(df)

