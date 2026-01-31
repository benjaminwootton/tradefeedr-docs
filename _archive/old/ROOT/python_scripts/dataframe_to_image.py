import dataframe_image as dfi
import pandas as pd
import os
import glob

path = "C:/Users/DilanPatel/OneDrive - Tradefeedr/Documents/Tradefeedr/doc_site/examples/api_rfq/outrights/participation_report/"
extension = 'csv'
os.chdir(path)
files = glob.glob(path+'*.{}'.format(extension))

def df_image(files):
    
    for file in files:
        df =pd.read_csv(file,index_col=0)
        if df.shape[1] >9:
            df= df.iloc[:,:9]
        df = df.head()
        name = file[:-3]+"png"

        dfi.export(df, name)
        
df_image(files)        