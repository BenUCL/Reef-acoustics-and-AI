import tensorflow as tf
import vggish_input
import vggish_params
import vggish_slim
import numpy as np
import urllib.request as urllib
import os

'''
Get an embedding from the AudioSet VGGish network. https://github.com/tensorflow/models/tree/master/research/audioset
'''

def downsample_feats(feat_mat, time_per_feat, target_time_per_feat):
    '''
    Downsample fine resolution audio features to average over longer timescales

    - NOTE: if target_time_per_feat is not divisible by time_per_feat this will round down:
    e.g. if time_per_feat = 0.96s and target_time_per_feat = 2s, then the actual features returned will be on a 1.92s resolution
    '''

    n_samples = int(target_time_per_feat / time_per_feat)
    if n_samples == 1:
        return feat_mat

    # Truncate observations to a round number of n_samples
    end =  n_samples * int(feat_mat.shape[0]/n_samples)

    if feat_mat.ndim == 2:
        # Higher dimensional features. Shape = (samples, features)
        feat_mat = feat_mat[:end,:]
        ptr = 0
        downsampled_feat = []
        while ptr + n_samples <= end:
            downsampled_feat.append(np.mean(feat_mat[ptr:ptr+n_samples,:],axis=0))
            ptr += n_samples

        downsampled_feat = np.asarray(downsampled_feat)
        return downsampled_feat
    elif feat_mat.ndim == 1:
        # 1 dimensional features
        feat_mat = feat_mat[:end]
        downsampled_feat = np.mean(feat_mat.reshape(-1, n_samples), 1)
        return downsampled_feat
    else:
        raise Exception('Can not downsample features with more than 2 dimensions')


def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)


class AudiosetAnalysis(object):
    def setup(self):
        # Paths to downloaded VGGish files.
        self.checkpoint_path = 'vggish_model.ckpt'
        self.pca_params_path = 'vggish_pca_params.npz'
        self.batch_size = 60

        # If we can't find the trained model files, download them
        if not os.path.exists(self.checkpoint_path):
            print('AudiosetAnalysis: Downloading model file {} (please wait - this may take a while)'.format(self.checkpoint_path))
            urllib.urlretrieve('https://storage.googleapis.com/audioset/vggish_model.ckpt', self.checkpoint_path)
        if not os.path.exists(self.pca_params_path):
            print('AudiosetAnalysis: Downloading params file {} (please wait - this may take a while)'.format(self.pca_params_path))
            urllib.urlretrieve('https://storage.googleapis.com/audioset/vggish_pca_params.npz', self.pca_params_path)

        # Define VGGish
        self.sess = tf.Graph().as_default()
        config = tf.ConfigProto(device_count={'CPU': 4})
        self.sess = tf.Session(config=config)

        # Load the checkpoint
        vggish_slim.define_vggish_slim()
        vggish_slim.load_vggish_slim_checkpoint(self.sess, self.checkpoint_path)
        self.features_tensor = self.sess.graph.get_tensor_by_name(vggish_params.INPUT_TENSOR_NAME)
        self.embedding_tensor = self.sess.graph.get_tensor_by_name(vggish_params.OUTPUT_TENSOR_NAME)

    def analyse_audio(self, wav_f):
        # Calculate log mel spectrogram as input to CNN
        print('AudiosetAnalysis: Calculating log mel spectrogram for {}'.format(wav_f))
        input_all = vggish_input.aud_file_to_examples(wav_f)

        print('AudiosetAnalysis: Calculating vggish features {} in batches of {}'.format(wav_f,self.batch_size))

        # For each 0.96s chunk of audio, calculate the VGGish embedding
        batch_idx = 0
        embedding_all = []
        while batch_idx < input_all.shape[0]:
            end_idx = np.min([input_all.shape[0], batch_idx+self.batch_size])
            input_batch = input_all[batch_idx:end_idx,:,:]
            batch_idx += self.batch_size

            [embedding_batch] = self.sess.run([self.embedding_tensor],
                                       feed_dict={self.features_tensor: input_batch})
            embedding_all.append(embedding_batch)

        embedding_all = np.vstack(embedding_all)

        # Calculate the mean feature vectors at different time scales
        time_per_feat = vggish_params.EXAMPLE_WINDOW_SECONDS

        res = dict()
        res['raw_audioset_feats_960ms'] = embedding_all
        res['raw_audioset_feats_4800ms'] = downsample_feats(embedding_all,time_per_feat,4.8)
        res['raw_audioset_feats_59520ms'] = downsample_feats(embedding_all,time_per_feat,59.52)
        res['raw_audioset_feats_299520ms'] = downsample_feats(embedding_all,time_per_feat,299.52)
        return res
