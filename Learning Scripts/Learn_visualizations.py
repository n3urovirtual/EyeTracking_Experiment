import os
import csv
import itertools
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.signal import savgol_filter
from helper import *

#Draw scatterplot using prepprocessed BPOG:
for i in img_id:
    file='Sub_1_Image_'+str(i)+'.csv'
    dataset=pd.read_csv(TRIALS_PATH+'/'+file,low_memory=False)
    x=dataset['BPOGX']
    y=dataset['BPOGY']
    fig, ax = plt.subplots(figsize=(20, 11))
    ax.scatter(x,
               y,
               zorder=1,
               marker='o',
               color='lime',
               alpha=0.5)
    img = plt.imread(IMG_PATH+"\S"+str(i)+".jpg")
    plt.imshow(img,
               extent=[-960, 960, -540, 540],
               aspect='auto')
    plt.xlabel('X coordinates (in pixels)', size=20)
    plt.ylabel('Y coordinates (in pixels)', size=20)
    plt.title('Scatterplot using (BPOGX,BPOGY) for Image '+str(i), size=30)
    #plt.text(-540,0,'Image S1', size=25)
    plt.show()
    plt.close()



#Draw scanpath using preprocessed GP3-HD fixation points (FPOGX,FPOGY):
for h,j in itertools.product(sub_id,img_id):
    file='Sub_'+str(h)+'_Image_'+str(j)+'.csv'
    dataset=pd.read_csv(os.path.join(TRIALS_PATH,file),low_memory=False)
    x=dataset.groupby('FPOGID')['FPOGX'].mean()
    y=dataset.groupby('FPOGID')['FPOGY'].mean()
    fix_dur=dataset.groupby('FPOGID')['FPOGD'].max()
    fig, ax = plt.subplots(figsize=(20, 11))
    ax.scatter(x,
               y,
               zorder=1,
               marker='o',
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
    plt.title('Scanpath of (FPOGX,FPOGY) for Subject '\
              +str(h)+' & Image '+str(j), size=30)
    my_img='Subject_'+str(h)+'_Image_'+str(j)+'.png'
    fig.savefig(os.path.join(RAW_SCANPATH,my_img))
    #plt.show()
    plt.close()