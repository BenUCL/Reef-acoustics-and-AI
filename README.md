# About the project

This GitHub repository contains material to support the upcoming publication: [Williams et al. (2024)](https://www.biorxiv.org/content/10.1101/2024.02.02.578582v1). Unlocking the soundscape of coral reefs with artificial intelligence.  Whilst created with coral reef soundscapes in mind, methods used in this investigation could be applied to any soundscape.

If you use any of these methods or code from this study then please cite the article.

# Tutorial
You may wish to begin applying machine learning led analysis to your own soundscape data. Read on to learn how to get started...

### Why soundscape analysis?
Passive acoustic monitoring data can be analysed in two broad ways. Often bioacousticians may manually listen to recordings and label individual sounds (e.g fish noise, bird species) then potentially train a detector on this. However, this can be slow, tricky and only allows bioacousticians to label a tiny subset of their true data. Alternatively, the whole soundscape can be used and compared, this sacrifices the granularity of individual sounds for big picture outputs at scale. Our paper focuses on the latter.

### Our recommended machine learning approach for soundscape analysis
In the associated paper, we show pairing pretrained neural networks with unsupervised learning algorithms provides the most insightful outputs. This retains an almost equal performance to training neural nets from scratch, whilst being orders of magnitude more computatinally efficient to run. 

### How to run the tutorial
This tutorial will guide users on how to begin using this analysis, using sample data from the worlds largest reef restoration program [buildingcoral.com](https://www.buildingcoral.com/) used in [Williams et al (2022)](https://doi.org/10.1016/j.ecolind.2022.108986). In the Tutorial folder you will find three key components, you can open these up and hit 'Open in colab':
1. Colab Demo: This is an introduction to using Google Colab. Colab allows users to run all the analysis from a web browser using data stored in Google Drive. Much easier than installing and settig up a local Python environment! 
2. Feature extraction: We show how to access the sample data and extract feature embeddings from this using a pretrained neural network. The outputs are saved to GDrive.
3. Unsupervised learning: We show how to run UMAP visualisation which useful for visually exploring patterns in data. This notebook then shows how to cluster the data, useful for a quantitative output of findings.

<p align="center">
  <img src="https://github.com/BenUCL/Reef-acoustics-and-AI/blob/main/Tutorial/sample_data_umap.png?raw=true" width="400" height="300" style="margin-right: 10px;" />
  <img src="https://github.com/BenUCL/Reef-acoustics-and-AI/blob/main/Tutorial/sample_data_clustering.png?raw=true" width="400" height="300" />
</p>

In the outputs from the tutorial (above) we are seeing UMAP and clustering outputs of 5s recordings from healthy, degraded and restored reefs. We see healthy and degraded reef soundscapes overlap at points, but mostly diverge. Interestingly we then see recordings from actively restored coral reefs are more likely to be assigned to clusters dominated by healthy recordings. With minimal effort compared to annotating recorders, UMAP and unsupervised clustering can provide powerful insights such as these for a multitude of tasks.


# Code used during the study
The Code folder contains all code used during the study for transparency. Note, as Google Colab's default environment updates, the code will no longer run in Colab. Instead, the tutorial should suffice if you are aiming to apply the findings of this study to new use cases. The code is organised as follows:

```
Code/
│── Audioset/                     # Code from Sethi et al (2020) containing code to work with the VGGish CNN. We only import some of this code as modules.
│── misc/                          # Miscellaneous analysis scripts.
│   ├── split_downsample_audio.ipynb   #  Audio preprocessing. This was used to split longer audio files into desired length (e.g 1min) and downsample to required frequency (16kHz).
│   ├── boxplots.ipynb                 # Produces accuracy boxplots for the trained CNN classifiers.
│   ├── calc_tccn_acc.ipynb            # Used to read in the results csv containing predictions from the T-CNN and calculates each training runs accuracy. Also produces confusion matrix plots.
│── custom_trained_cnn/            # Scripts for training the VGGish CNN from scratch.
│   ├── audio_preprocessing.ipynb      # Splits data into training, validation, and test sets then extracts log-mel spectrograms
│   ├── cnn_training.ipynb             # Trains the VGGish CNN from scratch on the preprocessed data.
│── compound_index/                # Scripts for compound index feature extraction and classification.
│   ├── compound_index_extraction.ipynb   # Used to extract the compound index features from raw audio.
│   ├── rf_compound_index_*.ipynb        # Trains and evaluates RF classifiers for different datasets/tasks using the compound index features.
│── pretrained_cnn/                 # Scripts for using a pretrained CNN for classification
│   ├── pretrained_cnn_extraction.ipynb  # Used to extract features from raw audio using the VGGish pretrained CNN.
│   ├── rf_pretrained_cnn_*.ipynb       # Trains and evaluates RF classifiers for different datasets/tasks using the pretrained CNN features.
│── unsupervised_learning/          # Scripts for unsupervised learning methods.
│   ├── clustering.ipynb                 # Runs affinity propagation clustering & Chi-square tests
│   ├── UMAP_*.ipynb                     # Notebooks used to run the affinity propagation clustering and run the chiq-sq test for each country and task combination.
│── vggish-env.yml                 # YAML file for setting up a local environment for VGGish feature extraction or training.
```

# Data
All data can be downloaded from the [Zenodo repository](https://zenodo.org/records/14841479). This repository contains:
1. **raw-audio-indonesia.zip**: The raw audio files from the Indonesian dataset. To access the raw Australian and French Polynesian audio files please go to these repositories:
   - [Australian dataset](https://zenodo.org/records/10539938)
   - [French Polynesian dataset](https://zenodo.org/records/10539938)
   
2. **outputs.zip**:
   - cnn_predictions.zip: The predictions from each training run of the CNN for each dataset and task.
   - precomputed_features.zip: The features extracted with the compound index, pretrained CNN, and trained CNN for all datasets.

3. **Supplementary 2 (interactive UMAP plots).zip**: The interactive UMAP plots which can be used to explore temporal trends from the data.

4. **tutorial_sample_data.zip**: 262 sample audio files used in the tutorial.

