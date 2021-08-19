import os
import itertools
import pandas as pd
from helper import *

def quadrant_finder(df,Roi_X,Roi_Y,Roi_L, Point_X, Point_Y):
    if Roi_X<0 and Roi_Y<0:
        #print('bottom left quadrant')
        def bottom_left():
            x_max=Roi_X-Roi_L
            x_min=Roi_X+Roi_L
            y_max=Roi_Y-Roi_L
            y_min=Roi_Y+Roi_L
            if x_max<=Point_X<=x_min and y_max<=Point_Y<=y_min:
                #print('this point is inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='TRUE'
            else:
                #print('this point is not inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='FALSE'
        return bottom_left()
    elif Roi_X<0 and Roi_Y>0:
        #print('top left quadrant')
        def top_left():
            x_max=Roi_X-Roi_L
            x_min=Roi_X+Roi_L
            y_max=Roi_Y+Roi_L
            y_min=Roi_Y-Roi_L
            if x_max<=Point_X<=x_min and y_min<=Point_Y<=y_max:
                #print('this point is inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='TRUE'
            else:
                #print('this point is not inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='FALSE'
        return top_left()
    elif Roi_X>0 and Roi_Y<0:
        #print('bottom right quadrant')
        def bottom_right():
            x_max=Roi_X+Roi_L
            x_min=Roi_X-Roi_L
            y_max=Roi_Y-Roi_L
            y_min=Roi_Y+Roi_L
            if x_min<=Point_X<=x_max and y_max<=Point_Y<=y_min:
                #print('this point is inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='TRUE'
            else:
                #print('this point is not inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='FALSE'
        return bottom_right()
    else:
        #print('top right quadrant')
        def top_right():
            x_max=Roi_X+Roi_L
            x_min=Roi_X-Roi_L
            y_max=Roi_Y+Roi_L
            y_min=Roi_Y-Roi_L
            if x_min<=Point_X<=x_max and y_min<=Point_Y<=y_max:
                #print('this point is inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='TRUE'
            else:
                #print('this point is not inside ROI')
                df.loc[df.index[ind],'Is_inside_ROI']='FALSE'
        return top_right()

             
for k,i in itertools.product(sub_id,img_id):
    for j in range(0,4):
        image=i.split('.')[0]
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv' 
        dataset=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
        target_coords=pd.read_csv(BEHAVIORAL_FILE)
        slice=target_coords[(target_coords['Image']==int(image)) & 
                            (target_coords['participant']==k)]
        Roi_X=int(slice['StarX']) #X coordinate
        Roi_Y=int(slice['StarY']) #Y coordinate
        Roi_L=100
        #quadrant_finder(Roi_X, Roi_Y)
        for ind in dataset.index:
            Point_X=dataset['FPOG_X'][ind]
            Point_Y=dataset['FPOG_Y'][ind]
            quadrant_finder(dataset, Roi_X, Roi_Y, Roi_L, Point_X, Point_Y)
        dataset.to_csv(os.path.join(EVENTS_PATH,file), index=False)
            
for k,i in itertools.product(sub_id,img_id):
    for j in range(0,4):
        image=i.split('.')[0]
        file='Sub_'+str(k)+'_Image_'+image+'_Block_'+str(j)+'.csv' 
        dataset=pd.read_csv(os.path.join(EVENTS_PATH,file),low_memory=False)
        trial_start_t=dataset.loc[0,'Trial_Start']
        trial_total_t=dataset.loc[0,'RT']
        search_initiation_t=dataset.loc[0,'SAC_LATENCY']
        true_only=dataset.query('Is_inside_ROI==True')
        for ind in true_only.index:
            if true_only.empty:
                continue
                fixation_start=dataset['Fixation_Start'][ind]
                verification_t=(trial_start_t+trial_total_t)-fixation_start
                scanning_t=trial_total_t-(search_initiation_t+verification_t)
            dataset.loc[dataset.index[ind],'Verification_time']=verification_t
            dataset.loc[dataset.index[ind],'Scanning_time']=scanning_t
            dataset.to_csv(os.path.join(EVENTS_PATH,file), index=False)
        
            
            


