'''APPLY PYTHAGOREAN THEOREM IN SMOOTHED MEMORY DATA'''

import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from helper import img_id,sub_id,TRIALS_PATH

#Apply PT into smoothed memory data to find sample-to-sample distance:
    
for k,i in itertools.product(sub_id, img_id):
    file='Sub_'+str(k)+'_Image_'+i.split('.')[0]+'_Block_3.csv' #Block 0,1,2,3
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    dataset['Sampling_Rate']=dataset['TIME'].diff().fillna(0).to_numpy()
    x=dataset['BPOGX'].diff().fillna(0).to_numpy()
    y=dataset['BPOGY'].diff().fillna(0).to_numpy()
    sample_2_sample_distance= (x ** 2 + y ** 2) ** 0.5
    distance=np.nan_to_num(sample_2_sample_distance)
    dataset['Distance2']=distance
    dataset['Velocity_in_px2']= dataset['Distance2']/dataset['Sampling_Rate']
    dataset['Velocity_in_deg2']= dataset['Velocity_in_px2']*0.025
    vel=dataset['Velocity_in_deg2'].fillna(0)
    sav_vel=savgol_filter(vel, 11, 2)
    dataset['Smoothed_Velocity_in_deg2']=sav_vel.tolist()
    dataset['Fix_or_Sac']=np.where(dataset['Smoothed_Velocity_in_deg2']>120, 
                                   'Sac',
                                   'Fix')
    dataset=dataset[dataset['Velocity_in_deg2']!=0]
    dataset.to_csv(os.path.join(TRIALS_PATH,file), index=False)
    

'''
for k,i in itertools.product(sub_id, img_id):
    file='Sub_'+str(k)+'_Image_'+i.split('.')[0]+'_Block_0.csv'
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,11))
    fig.suptitle(f'Subject:{str(k)} , Image:{i.split(".")[0]}, , Block: 1',size=30)
    time=dataset['Sampling_Rate'].cumsum()
    smoothed_velocity1=dataset['Velocity_in_deg2']
    smoothed_velocity2=dataset['Smoothed_Velocity_in_deg2']
    ax1.plot(time, smoothed_velocity1)
    ax2.plot(time, smoothed_velocity2)
    #plt.axhline(90, color='red')
    #plt.title(f'Subject:{str(k)} , Image:{i.split(".")[0]} , Block: 1')
    ax2.axhline(120, color='red')
    ax1.set_title('Unsmoothed velocity',size=15)
    ax2.set_title('Smoothed velocity',size=15)
    plt.show()
    plt.close()
  
    

for i,k in itertools.product(sub_id, img_id):
    file='Sub_'+str(i)+'_Image_'+str(k)+'.csv'
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    time=dataset['Sampling_Rate'].cumsum().fillna(0)
    velocity=dataset['Velocity_in_deg']
    plt.plot(time, velocity)
    plt.axhline(90, color='red')
    plt.title(f'Subject:{str(i)} , Image:{str(k)}')
    plt.xlabel('Time (sec)')
    plt.ylabel('Velocity values')
    plt.show()
    plt.close()'''
   


