# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:46:52 2022

@author: Gary

This code is used to download a set of csv tables that are then  merged
to create a dataframe of the Open-FF data.
"""

zip_url = 'https://storage.googleapis.com/gwa-test/sm_dataframe.zip'

import pandas as pd
import zipfile
import requests
from io import BytesIO

def get_dataset(url = zip_url,verbose=True): 

    # get zipped file with CSV table from given address
    c = requests.get(url).content
    
    filebytes = BytesIO(c)
    zfile = zipfile.ZipFile(filebytes)
    if verbose:
        print(f' Files in downloaded zip archive: {zfile.namelist()}')
    
    # now unzip and create the associated dataframes
    with zfile.open('repo_info.txt','r') as f:
        txt = f.read()
    if verbose:
        print(f' reading data from repository: {txt}')
    
    with zfile.open('disclosures.csv') as f:
        if verbose: print(' -- processing disclosures')
        ddf = pd.read_csv(f,quotechar='$',encoding='utf-8',low_memory=False,
                         dtype={'APINumber':'str'})
        ddf.date = pd.to_datetime(ddf.date)
    with zfile.open('chemrecs.csv') as f:
        if verbose: print(' -- processing chemical records')
        cdf = pd.read_csv(f,quotechar='$',
                          encoding='utf-8',low_memory=False)
    mg = pd.merge(cdf,ddf, on='UploadKey', how='left')
    with zfile.open('bgCAS.csv') as f:
        if verbose: print(' -- processing chemical metadata')
        casdf = pd.read_csv(f,quotechar='$',
                          encoding='utf-8',low_memory=False)
    mg = pd.merge(mg,casdf, on='bgCAS', how='left')
    if verbose: print(f'Dataframe size: {mg.shape}')
    return mg