''' Event Detection and collation into separate files'''

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

#Create separate files for each participant's fixations:
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
        write_f=events[events['FPOG_DUR']> 0.050]
        #add some descriptive variables as well:
        write_f.loc[write_f.index[0], 'Trial_Start'] = trials['TIME'].iloc[0]
        write_f.loc[write_f.index[0], 'Clutter'] = trials['CLUTTER'].iloc[0]
        total_trial_time=trials.iloc[-1,1]-trials.iloc[0,1]
        write_f.loc[write_f.index[0], 'RT'] = total_trial_time
        write_f.loc[write_f.index[0], 'Accuracy'] = trials['CS'].iloc[-1]
        write_f.to_csv(os.path.join(EVENTS_PATH,file), index=False)


#Add columns about saccades to the files created above:
for k,i in itertools.product(sub_id, img_id):
    for j in range(0,4):
        image=i.split('.')[0]
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv'
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
        img = plt.imread(IMG_PATH+"\S"+image+".jpg")
        plt.imshow(img, 
                   zorder=0, 
                   extent=[-960, 960, -540, 540],
                   aspect='auto')
        for h in range(len(fix_dur)):
            ax.annotate(str(h+1),
                        xy=(fix_dur.iloc[h],
                            fix_dur.iloc[h]),
                        xytext=(x.iloc[h], 
                                y.iloc[h]),
                        fontsize=30,
                        color='black',
                        ha='center',
                        va='center')
        plt.xlabel('X coordinates (in pixels)', size=20)
        plt.ylabel('Y coordinates (in pixels)', size=20)
        title='Scanpath for Subject '+str(k)+' /Image '+image+' /Block '+str(j)
        plt.title(title, size=30)
        #draw a rectangle around the location of the star
        target_coords=pd.read_csv(BEHAVIORAL_FILE)
        slice=target_coords[(target_coords['Image']==int(image)) & 
                            (target_coords['participant']==k)]
        left=int(slice['StarX']) #X coordinate
        bottom=int(slice['StarY']) #Y coordinate
        width=200
        height=200
        rect=mpatches.Rectangle((left-100,bottom-100),
                                width, 
                                height, 
                                fill=False,
                                color='orange',
                                linewidth=2)
        circle=mpatches.Circle((left,bottom),radius=10,color='red')
        plt.gca().add_patch(rect)
        plt.gca().add_patch(circle)
        output_img='Subject_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.png'
        fig.savefig(os.path.join(IVT_SCANPATH,output_img))
        #plt.show()
        plt.close()