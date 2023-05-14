# About the project

This GitHub repository contains material to support the upcoming publication: Williams et al. (2023). Unlocking the soundscapes of coral reefs with artificial intelligence.  Whilst created with coral reef soundscapes in mind, methods used in this investigation could be applied to any soundscape field.

This repository provides code that can be used to complete the full analysis used in the project. Better still, you can download all the code alongside sample data from the Zenodo repository (https://zenodo.org/record/7810650). You can then upload this to your own Google Drive account and run all the analysis from your web browser using Google Colab, without the need to download and install python or any other software, see further instructions below. 

This Github repo contains: 

1. Code to perform all analysis.
2. The Audioset package also required for analyis, adapted by [Sethi et al. (2020)](https://www.pnas.org/doi/full/10.1073/pnas.2004702117) from [Hershey et al. (2017)](https://arxiv.org/abs/1609.09430).
3. The full_dataset_features.zip which contains csv's of feature sets calculated from all three datasets using the compound index, pretrained CNN and features extracted by purpose trained CNNs.

Additional items in the Zenodo repository are:

3. audio_dir: 1.4GB of sample audio files – this is the full dataset used in previous work [Williams et al (2022)](https://doi.org/10.1016/j.ecolind.2022.108986).
4. Results folder: 
    - CNN_predictions: *csv* files of the trained CNN class prediction for the habitat and site tasks for all three datasets. These predictions are used in the Trained_CNN accuracy_calculator_script 
    - minibatch_files: folders ready for the writing and pickling of minibatches for the train, validation and test sets created using the CNN_minibatch_creation and used by the CNN_training script. The train folder is already populated for users who want to jump straight to testing the creation of a custom pretrained CNN detaied below using the sample audio.
    - trained_CNN_saved_model: produced by the produce_a_custom_pretrained_CNN script when using the sample audio. These files will be overwritten with identical files if users choose to run this script. 
    - If you executre the feature extraction scripts on the sample audio, they will be written here.

# Citing
If you use any code from this project, please cite: (tbc)

# Useage
The performance of three methods at supervised classifier and unsupervised clustering tasks were compared in this paper. To run the full workflow download the 'BenUCL/Reef-acoustics-and-AI-v1.1.zip' and 'sample_audio.zip' from the [Zenodo repository](https://zenodo.org/record/7810650). Unzip these and place the sample_audio folder into the other folder. Rename this ‘Reef soundscapes with AI’ and upload them to the MyDrive folder in your Google Drive (saving elsewhere on your drive, or with a different name, will prevent scripts from being able to find the right file path). The scripts will run on the sample audio now included in this folder on your Google Drive.

The workflow to replicate this analysis can be undertaken as follows:

### Compound index classifier
1.	Perform feature extraction from example audio using a suite of compound indices using the Feature_extraction_with_compound_index.ipynb script. This will save a *.csv* file called *compound_index_features* to the */Results* folder. The *.csv* files for the full datasets used in this study are used from here on to reproduce the investigations results. These are saved in the */Results/full_dataset_features*. However, you could adapt the downstream scripts to run on your own feature sets from other audio.
2.	Next, a machine learning classifier is trained to identify the classes (e.g healthy and degraded) using the *Random forests compound index _ .ipynb*. Here, ‘_’ represents the dataset (Indo, Aus or Poly) and task (habitat or site identifier). This performs cross validation and outputs accuracy scores for all repeats.

### Pretrained CNN classifier
1.	Same as above, but instead of accessinf *compound index* scripts, access the *pretrained CNN* scripts.
2.	This will extract features from audio with the VGGish pretrained CNN, using 
### Trained CNN classifier

1.	Start with the *CNN minibatch creation.ipynb* script. This performs log-mel spectrogram extraction on the example audio, splits these in minibatches and saves these as pickle files in the */Results/minibatches_* folders, where '_' represents the training, validation or test folder.
2.	The *CNN_training.ipynb* script can then be used to train the CNN classifier on the example audio, where it learns to classify healthy and degraded reefs. This outputs predictions for test data to the */Results/Colab_CNN_predictions* folder in a .csv file. The .csv files for the full datasets used in this study are used from here on to reproduce the investigations results. These are saved in the */Results/full_dataset_features/NEW...*. However, you could adapt the downstream scripts to run on your own feature sets from other audio.
3.	The *Trained CNN accuracy calculator.ipynb* script is then used to take these .csv’s, pool predictions for each minute, and output an accuracy. This script uses the predictions for the full datasets used in this study in the *Results/CNN_predictions* folder.


### Creating your own pretrained CNN

1.	Custom pretrained CNN’s were produced from each dataset to perform unsupervised clustering. This was done by training the classifier to predict which site (which should always be known) that recordings came from. The scripts are currently set up to perform this on the example audio.
2.	First, the *CNN minibatch creation.ipynb* script must be executed as above, under the Trained classifier heading.
3.	The *Produce a custom pretrained CNN.ipynb* script can then be run. This contains further instructions on what to do so as to use this model on your own audio.


### UMAP and unsupervised clustering
1.	UMAP plots are created using the *UMAP_.ipynb* scripts, where ‘_’ represents the datasets (Indo, Aud or Poly) to be used. These use the already calculated features sets for each method in the */Results/full_dataset_features* folder. Once again, these can be easily adapted to run on your own feature sets.
2.	Unsupervised clustering is performed using the *Unsupervised clustering.ipynb* script, using the already calculated features sets from this investigations data.

