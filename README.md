# MixingSpecific_Aug4MSS


This repo contains the scripts and demo songs for paper titled 
"*Mixing-Specific Data Augmentation Techniques for Improved Blind Violin/Piano Source Separation*". | [**Paper (arXiv)**](https://arxiv.org/abs/2008.02480) | [**Demo Page**](https://sunnycyc.github.io/aug4mss_demo/) | [**Pretrained Models (GoogleDrive)**](https://drive.google.com/drive/folders/1YyLww3G7-Amu_bs8s9Wl3NceUcQuq3Or) |


The main purpose of this work is to allow users to apply mixing-specific data augmentation techniques to facilitate the training of a neural network model for source separation, in particular with the Open-Unmix model architecture [1]. The training scripts required for training your own models can be found from [the official repository of Open-Unmix](https://github.com/sigsep/open-unmix-pytorch).

## Modification for Training
Note that for our experiment scenario, we modified the model as follows:
* train.py:
    * change nb_channels to 1: for monaural cases
    * data.py:
        * nb-train-samples corresponds to the N in the paper
   

## Contents
The contents are oganized as follows:
* Pretraind_Models: 
    [ (Uploaded to GoogleDrive)](https://drive.google.com/drive/folders/1YyLww3G7-Amu_bs8s9Wl3NceUcQuq3Or?usp=sharing)
    * Random_N2000
    * Wet_N2000
* Demo_mp3_15sec:
    * [demo page](https://sunnycyc.github.io/aug4mss_demo/)
    * 15-sec version of the 16 test songs
* MedleyDB_Tsongs:
    * MedleyDB_16tsong_path.pickle
    * ExtractMedleyDB_16TestSongs.py:
for extracting the 16 MedleyDB[2, 3] songs.
* Augmentations: demo codes for proposed augmentation methods
    * chroma_distance.py
    * correlation2d.py
    * wet.py
    * implementation of non-silence is simple, as shown in [doc of librosa](https://librosa.github.io/librosa/generated/librosa.effects.split.html)

    

* Inference.py: demo code for using Pretrained_Models to separate the Demo_mp3_15sec
    * SeparateModules.py: modules modified from Open-Unmix test.py
    * the required modules should be downloaded from [Open-Unmix official repository](https://github.com/sigsep/open-unmix-pytorch):
        * utils.py
        * model.py


---




## Reference
[1] *F.-R. St ̈oter, S. Uhlich, A. Liutkus, and Y. Mitsufuji, “Open-Unmix - Areference implementation for music source separation,”Journal of OpenSource Software, vol. 4, no. 41, p. 1667, 2019.*

[2] *MedleyDB Original:
R. Bittner, J. Salamon, M. Tierney, M. Mauch, C. Cannam and J. P. Bello, "MedleyDB: A Multitrack Dataset for Annotation-Intensive MIR Research", in 15th International Society for Music Information Retrieval Conference, Taipei, Taiwan, Oct. 2014.*

[3] *MedleyDB 2.0
Bittner, R., Wilkins, J., Yip, H., & Bello, J. (2016). MedleyDB 2.0: New Data and a System for Sustainable Data Collection. New York, NY, USA: International Conference on Music Information Retrieval (ISMIR-16).*
