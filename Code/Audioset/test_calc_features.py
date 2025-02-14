'''
# See https://github.com/sarabsethi/audioset_soundscape_feats_sethi2019/tree/master/calc_audioset_feats for installation instructions
'''

from AudiosetAnalysis import AudiosetAnalysis
import os

# Get all mp3 or wav files in our audio directory
audio_dir = (r'C:\Users\bw339\OneDrive - University College London\UCL PhD\Extras\Sarebs Study\test_audio') #change this to the file location of your audio files
all_fs = os.listdir(audio_dir)
audio_fs = [f for f in all_fs if '.wav' in f.lower() or '.mp3' in f.lower()]

# Setup the audioset analysis
an = AudiosetAnalysis()
an.setup()

# Analyse each audio file in turn, and print the shape of the results
for f in audio_fs:
    path = os.path.join(audio_dir, f)
    results = an.analyse_audio(path)

    # Results are stored in a dictionary - keys tell you the feature time resolutions in milliseconds
    for res in results.items():
        print('{}: {}'.format(res[0],res[1].shape))
