########## Change as appropriate

# Path to the location where your audio file are stored:
audio_dir = r'/lustre/home/ucbtbw0/Indonesia2018/sliced_files/' 

# Path to folder containing vggish setup files and 'AudiosetAnalysis' downloaded from sarebs supplementary
vggish_files = r'/lustre/home/ucbtbw0/Indonesia2018/scripts/pretrained_vggish/' 

# Output folder for results:
output_folder_1sec = r'/lustre/home/ucbtbw0/Indonesia2018/pretrained_NN_results/Pretrained1secfeats_' 
output_folder_1min = r'/lustre/home/ucbtbw0/Indonesia2018/pretrained_NN_results/Pretrained1minfeats_'


########## Imports
import os

#Navigate to the folder containing setup files, including AudiosetAnalysis downloaded from sarebs supplementary
os.chdir(vggish_files) 

#import packages/modules
from AudiosetAnalysis import AudiosetAnalysis
import pandas as pd
import time

#probably can import time stuff more neatly
from datetime import datetime
from datetime import timedelta
from datetime import time
from time import strftime
import time




##########
# Setup the audioset analysis - RUN THIS ONCE PER SESSION, otherwise it will error
an = AudiosetAnalysis()
an.setup()




########## Run feature extraction
#select files
all_fs = os.listdir(audio_dir) #list of all files in directory
audio_fs = [f for f in all_fs if '.wav' in f.lower() or '.mp3' in f.lower()] #list of all audio files in dir: .wav or .mps

#initiate empty dataframes to save results
results_df_1sec = pd.DataFrame()
results_df_1min = pd.DataFrame() 

#file_names = [] #initiate list of file names
for f in audio_fs:
    path = os.path.join(audio_dir, f)
    print(f) #print file name
    
    #extract timestamp from filename
    #BaF1.1055H.1678278701.180827.NT1057.wav
    t2 = f.split(".")[4][2:6]
    t1 = f.split(".")[3]
    t = t1+t2+'00'
    recording_start_time = pd.to_datetime(t, format='%y%m%d%H%M%S') 
    slice_time = recording_start_time - timedelta(milliseconds=960)
    mean_slice_time = recording_start_time - timedelta(minutes=1)
    
    #calculate feature values
    results = an.analyse_audio(path)
    
    ###Saving results
    #These loops takes the current filename, rips the timestamp, appends the corresponding length of time being analysed
    #(0.96s or 1min) additively, saves the 0.96s and longer time being averaged to lists, saves these as df's
     
    #For 0.96s results:
    r1sec = results['raw_audioset_feats_960ms']
    for count, r1sec in enumerate(r1sec):
        slice_time = slice_time + timedelta(milliseconds=960)
        string_time = slice_time.strftime('%H.%M.%S.%f')[:-4]
        result_name = f[:-4] + string_time[5:11] + '.wav'
        #result_name = f[:-4] + 'T' + string_time + '.wav' #for tims naming conv, before sliced filed were made
        #result_name = f[:-4]+'T'+str(count+1)+'.wav' #use this line if not using ST timestamped files
        results_df_1sec[result_name] = pd.Series(results['raw_audioset_feats_960ms'][count])
    
    #For 1min results:
    r1min = results['raw_audioset_feats_59520ms']
    for count, r1min in enumerate(r1min):
        #store the timestamp
        mean_slice_time = mean_slice_time + timedelta(minutes=1)
        string_time = mean_slice_time.strftime('%H.%M.%S.%f')[:-4]
        #result_name = f#[:-4] + string_time[5:11] + '.wav'
        #result_name = f[:-4] + 'T' + string_time + '.wav'
        #result_name = f[:-4]+'T'+str(count+1)+'.wav' #use this line if not using ST timestamped files
        results_df_1min[f] = pd.Series(results['raw_audioset_feats_59520ms'][count])


print('1min results preview:')
print(results_df_1min.head())
print('1sec results preview:')
print(results_df_1sec.head())


########## Save timestamped csv's with results
results_df_1sec.to_csv(output_folder_1min+time.strftime("_%y_%m_%d-%H_%M_%S")+'.csv')
results_df_1min.to_csv(output_folder_1sec+time.strftime("_%y_%m_%d-%H_%M_%S")+'.csv')