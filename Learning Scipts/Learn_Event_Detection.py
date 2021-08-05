''' Event Detection and collation into separate files'''

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from helper import *


# Categorize fixations and saccades based on their order:
for k,i in itertools.product(sub_id, img_id):
    print(f'Participant {str(k)} Image {i}')
    file='Sub_'+str(k)+'_Image_'+i.split('.')[0]+'_Block_3.csv' #Block 0,1,2,3
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    category = dataset['Fix_or_Sac']
    watch_next = category != category.shift()
    rank_order = watch_next.cumsum().groupby(category).rank(method='dense')
    dataset['Group'] =  category +"_"+ rank_order.astype(int).astype(str)
    dataset.to_csv(os.path.join(TRIALS_PATH,file), index=False)


#Create separate files for each participant's set of saccades and fixations:
for k,i in itertools.product(sub_id, img_id):
    file='Sub_'+str(k)+'_Image_'+i.split('.')[0]+'_Block_3.csv' #Block 0,1,2,3
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    events=pd.DataFrame()
    events['Timestamp_Start']=dataset.groupby('Group')['TIME'].min()
    index= dataset.groupby('Group')['Group']
    events['Event_ID']=index.first()
    only_fixations=dataset.query("Group.str.startswith('F').values")
    time_fix_max=only_fixations.groupby('Group')['TIME'].max()
    time_fix_min=only_fixations.groupby('Group')['TIME'].min()
    events['FPOG_DUR']=time_fix_max-time_fix_min
    events['FPOG_X']=only_fixations.groupby('Group')['BPOGX'].mean()
    events['FPOG_Y']=only_fixations.groupby('Group')['BPOGY'].mean()
    only_saccades=dataset.query("Group.str.startswith('S').values")
    time_sac_max=only_saccades.groupby('Group')['TIME'].max()
    time_sac_min=only_saccades.groupby('Group')['TIME'].min()
    events['SAC_DUR']=time_sac_max-time_sac_min
    events['event'] = events.Event_ID.str.rsplit("_").str[0]
    events['idx'] = events.Event_ID.str.rsplit("_").str[-1].astype(int)
    events.sort_values(['event', 'idx'],inplace=True)
    events.drop(['event', 'idx'], axis = 1,inplace=True)
    final=events[(events['FPOG_DUR']> 0.050) | (events['SAC_DUR'] > 0.010)]
    final.to_csv(os.path.join(EVENTS_PATH,file), index=False)


#Visualize scanpath for all participants based on I-VT fixations:
for k,i in itertools.product(sub_id,img_id):
    img_num=i.split('.')[0]
    file='Sub_'+str(k)+'_Image_'+img_num+'_Block_3.csv' #Block 0,1,2,3
    set=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
    dataset=set.query("Event_ID.str.startswith('F').values")
    x=dataset['FPOG_X']
    y=dataset['FPOG_Y']
    fix_dur=dataset['FPOG_DUR']
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
    img = plt.imread(IMG_PATH+"\S"+img_num+".jpg")
    plt.imshow(img, 
               zorder=0, 
               extent=[-960, 960, -540, 540],
               aspect='auto')
    for j in range(len(fix_dur)):
        ax.annotate(str(j+1),
                    xy=(fix_dur.iloc[j],
                        fix_dur.iloc[j]),
                    xytext=(x.iloc[j], 
                            y.iloc[j]),
                    fontsize=30,
                    color='black',
                    ha='center',
                    va='center')
    plt.xlabel('X coordinates (in pixels)', size=20)
    plt.ylabel('Y coordinates (in pixels)', size=20)
    plt.title('Scanpath for Subject '+str(k)+' ,Image '+img_num+ ' ,Block 4', size=30) #Block 1,2,3,4
    my_img='Subject_'+str(k)+'_Image_'+img_num+'_Block_4.png' #Block 1,2,3,4
    fig.savefig(os.path.join(IVT_SCANPATH,my_img))
    #plt.show()
    plt.close()