'''LEARNING DATA COLLATION (VARIABLES OF INTEREST FOR EACH PARTICIPANT/TRIAL)'''

import os
import itertools
import pandas as pd
import numpy as np
from helper import *

collation=pd.DataFrame()

##TO DO: check why it omits subject 1, image 1.

for i,k in itertools.product(sub_id, img_id):
    for j in range (0,4):
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv'
        events=pd.read_csv(os.path.join(EVENTS_PATH,file))
        dir_route=pd.read_csv(os.path.join(DIR_ROUTE_PATH,file))
        collation['Subject_ID']=str(i)
        collation['Image_ID']=str(k)
        collation['Block']=str(j)
        collation['Clutter']=events['Clutter'].iloc[0]
        collation['Total_num_fixations']=events['Event_ID'].count()
        collation['Mean_fixation_dur']=events['FPOG_DUR'].mean()
        collation['First_saccade_latency']=events['SAC_LATENCY'].iloc[0]
        collation['Mean_saccade_length']=events['SAC_AMPLITUDE'].mean()
        collation['Scanpath_length']=events['SAC_AMPLITUDE'].sum()
        ratio=collation['Scanpath_length']/dir_route['Direct_path_in_pixels']
        collation['Scanpath_ratio']=ratio
        file_to_write='Learn_collate.csv'
        output_path=os.path.join(COLLATION_PATH,file_to_write)
        head=not os.path.exists(output_path)
        collation.to_csv(output_path, index=False,mode='a',header=head)

