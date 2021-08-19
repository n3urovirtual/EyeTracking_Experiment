''' EVENT DETECTION (FIXATIONS & SACCADES)'''

import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from helper import *


# Categorize fixations and saccades based on their order:
for i,k in itertools.product(sub_id, img_id):
    file='Sub_'+str(i)+'_Image_'+str(k)+'.csv'
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    category = dataset['Fix_or_Sac']
    watch_next = category != category.shift()
    rank_order = watch_next.cumsum().groupby(category).rank(method='dense')
    dataset['Group'] =  category +"_"+ rank_order.astype(int).astype(str)
    dataset.to_csv(os.path.join(TRIALS_PATH,file), index=False)


#Create separate files for each participant's fixations:
for i,k in itertools.product(sub_id, img_id):
    file='Sub_'+str(i)+'_Image_'+str(k)+'.csv'
    trials=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    events=pd.DataFrame()
    events['Fixation_Start']=trials.groupby('Group')['TIME'].min()
    events['Event_ID']= trials.groupby('Group')['Group'].first()
    only_fixations=trials.query("Group.str.startswith('F').values")
    time_fix_max=only_fixations.groupby('Group')['TIME'].max()
    time_fix_min=only_fixations.groupby('Group')['TIME'].min()
    events['FPOG_DUR']=time_fix_max-time_fix_min
    events['FPOG_X']=only_fixations.groupby('Group')['BPOGX'].mean()
    events['FPOG_Y']=only_fixations.groupby('Group')['BPOGY'].mean()
    #events['event'] = events['Event_ID'].str.rsplit("_").str[0]
    events['Idx'] = events['Event_ID'].str.rsplit("_").str[-1].astype(int)
    events.sort_values('Idx',inplace=True)
    events.drop('Idx', axis = 1,inplace=True)
    #final=events[(events['FPOG_DUR']> 0.050) | (events['SAC_DUR'] > 0.010)]
    to_write=events[events['FPOG_DUR']> 0.050]
    to_write.loc[to_write.index[0], 'Trial_Start'] = trials['TIME'].iloc[0]
    to_write.loc[to_write.index[0], 'Clutter'] = trials['CLUTTER'].iloc[0]
    to_write.to_csv(os.path.join(EVENTS_PATH,file), index=False)
    

#Add columns about saccades to the files created above:
for i,k in itertools.product(sub_id, img_id):
    file='Sub_'+str(i)+'_Image_'+str(k)+'.csv'
    events=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
    trial_start=events.iloc[0,5]
    first_fixation_start=events.iloc[0,0]
    first_fixation_dur=events.iloc[0,2]
    events.loc[events.index[0],'SAC_LATENCY']=first_fixation_dur \
        if trial_start==first_fixation_start \
            else (first_fixation_start-trial_start) + first_fixation_dur
    x=events['FPOG_X'].diff()
    y=events['FPOG_Y'].diff()
    events['SAC_AMPLITUDE']=(x ** 2 + y ** 2) ** 0.5
    fix_dur_wo_last=events.iloc[:-1,2].reset_index(drop=True)
    fix_start_dif=events['Fixation_Start'].diff().dropna().reset_index(drop=True)
    events['SAC_DUR']=fix_start_dif-fix_dur_wo_last
    events.to_csv(os.path.join(EVENTS_PATH,file), index=False)
    
    
    '''sac_dur_min=dataset['SAC_DUR'].min() *1000
    if sac_dur_min<10:
     print(f'subject: {str(i)}, Image: {str(k)}')'''


#Visualize scanpath for all participants based on I-VT fixations:
for h,j in itertools.product(sub_id,img_id):
    file='Sub_'+str(h)+'_Image_'+str(j)+'.csv'
    events=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
    x=events['FPOG_X']
    y=events['FPOG_Y']
    fix_dur=events['FPOG_DUR']
    fig, ax = plt.subplots(figsize=(20, 11))
    ax.scatter(x,
               y,
               zorder=1
               ,marker='o',
               s=fix_dur*10000,
               color='lime',
               alpha=0.5)
    ax.plot(x,
            y,
            '-o',
            linewidth=3,
            color='blue')
    img = plt.imread(IMG_PATH+"\S"+str(j)+".jpg")
    plt.imshow(img, 
               zorder=0, 
               extent=[-960, 960, -540, 540],
               aspect='auto')
    for i in range(len(fix_dur)):
        ax.annotate(str(i+1),
                    xy=(fix_dur.iloc[i],
                        fix_dur.iloc[i]),
                    xytext=(x.iloc[i], 
                            y.iloc[i]),
                    fontsize=30,
                    color='black',
                    ha='center',
                    va='center')
    plt.xlabel('X coordinates (in pixels)', size=20)
    plt.ylabel('Y coordinates (in pixels)', size=20)
    plt.title('Scanpath for Subject '+str(h)+' , Image '+str(j), size=30)
    
    #draw a rectangle around the location of the star
    target_coords=pd.read_csv(BEHAVIORAL_FILE)
    slice=target_coords[(target_coords['Image']==j) & 
                        (target_coords['participant']==h)]
    left=int(slice['StarX'])-50 #X coordinate
    bottom=int(slice['StarY'])-50 #Y coordinate
    width=100
    height=100
    rect=mpatches.Rectangle((left,bottom),width, height, 
                            fill=False,
                            color='orange',
                            linewidth=5)
    plt.gca().add_patch(rect)
    my_img='Subject_'+str(h)+'_Image_'+str(j)+'.png'
    fig.savefig(os.path.join(IVT_SCANPATH,my_img))
    #plt.show()
    plt.close()