''' Event Detection and collation into separate files'''

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from helper import *


# Categorize fixations and saccades based on their order:
for k,i in itertools.product(sub_id, img_id):
    for j in range(0,4):
        image=i.split('.')[0]
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv' 
        dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
        category = dataset['Fix_or_Sac']
        watch_next = category != category.shift()
        rank_order = watch_next.cumsum().groupby(category).rank(method='dense')
        dataset['Group'] =  category +"_"+ rank_order.astype(int).astype(str)
        dataset.to_csv(os.path.join(TRIALS_PATH,file), index=False)


#Create separate files for each participant's set of saccades and fixations:
for k,i in itertools.product(sub_id, img_id):
    for j in range(0,4):
        image=i.split('.')[0]
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv'
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
        events['Idx'] = events['Event_ID'].str.rsplit("_").str[-1].astype(int)
        events.sort_values('Idx',inplace=True)
        events.drop('Idx', axis = 1,inplace=True)
        to_write=events[events['FPOG_DUR']> 0.050]
        to_write.loc[to_write.index[0], 'Trial_Start'] = trials['TIME'].iloc[0]
        to_write.loc[to_write.index[0], 'Clutter'] = trials['CLUTTER'].iloc[0]
        to_write.to_csv(os.path.join(EVENTS_PATH,file), index=False)


#Visualize scanpath for all participants based on I-VT fixations:
for k,i in itertools.product(sub_id,img_id):
    for j in range(0,4):
        image=i.split('.')[0]
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv' 
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
        title='Scanpath for Subject '+str(k)+' ,Image '+image+' ,Block '+str(j)
        plt.title(title, size=30) #Block 1,2,3,4
        my_img='Subject_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.png'
        fig.savefig(os.path.join(IVT_SCANPATH,my_img))
        #plt.show()
        plt.close()