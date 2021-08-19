'''APPLY SAVITZKY-GOLAY FILTER IN MEMORY DATA (PER TRIAL)

import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from helper import *

#Apply savitzky golay filter and add a new column for smoothed BPOGX, BPOGY:
for i,k in itertools.product(sub_id, img_id):
    file='Sub_'+str(i)+'_Image_'+str(k)+'.csv'
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    #print(f'Processing data from participant {i}.Please wait...')
    bpogx=dataset['BPOGX']
    bpogy=dataset['BPOGY']
    sav_bpogx=savgol_filter(bpogx, 11, 2)
    dataset['SAV_BPOGX']=sav_bpogx.tolist()
    sav_bpogy=savgol_filter(bpogy, 11, 2)
    dataset['SAV_BPOGY']=sav_bpogy.tolist()
    dataset.to_csv(os.path.join(TRIALS_PATH,file), index=False)
    
    #Visualize unsmoothed and smoothed scatterplots using BPOG:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    fig.suptitle('Scatterplots for (BPOGX,BPOGY) for Participant '+str(i)+
                 ' Image '+str(k), size=30)
    
    #ax1.plot(dataset['BPOGX'], dataset['BPOGY'])
    x=dataset['BPOGX']
    y=dataset['BPOGY']
    ax1.scatter(x, 
                y,
                zorder=1,
                marker='o', 
                color='lime',
                alpha=0.5)
    img1 = plt.imread(IMG_PATH+"\S"+str(k)+".jpg")
    ax1.imshow(img1, 
               extent=[-960, 960, -540, 540],
               aspect='auto')
    ax1.set_title('BPOG', size=15)
    
    #ax2.plot(dataset['SAV_BPOGX'],dataset['SAV_BPOGY'])
    sav_x=dataset['SAV_BPOGX']
    sav_y=dataset['SAV_BPOGY']
    ax2.scatter(sav_x,
                sav_y,
                zorder=1,
                marker='o', 
                color='lime',
                alpha=0.5)
    img2 = plt.imread(IMG_PATH+"\S"+str(k)+".jpg")
    ax2.set_title('smoothed BPOG', size=15)
    ax2.imshow(img2, 
               extent=[-960, 960, -540, 540],
               aspect='auto')
    plt.show()
    plt.close()'''


