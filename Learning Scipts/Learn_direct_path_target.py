import pandas as pd
from helper import *
import os

sp_ratio=pd.read_csv('C:/Users/presi/Desktop/PhD/Memory guided attention in'\
                     ' cluttered scenes v.3/Eye Tracking Data/'\
                     '1. Associative Learning/direct_route.csv')

for i in range(len(sp_ratio)):
    row=sp_ratio.iloc[[i]].reset_index(drop=True)
    subject=row.iloc[0,0]
    image=row.iloc[0,1]
    file='Sub_'+str(subject)+'_Image_'+str(image)+'.csv'
    row.to_csv(os.path.join(DIR_ROUTE_PATH,file),index=False)
    print(subject,image)
