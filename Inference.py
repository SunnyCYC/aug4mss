# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:08:33 2020

@author: CITI
"""

#%%

from SeparateModules import *
import os
import glob
import soundfile as sf
from pathlib import Path
import torch
import time

source_dir = './Demo_mp3_15sec'
tsong_list = glob.glob(os.path.join(source_dir, "*.mp3"))

cuda_num = 0
cuda_str = "cuda:"+str(cuda_num)
device = torch.device(cuda_str if torch.cuda.is_available() else "cpu")
samplerate = 44100

model_dir = './Pretrained_Models' # directory of model folders
model_list = ['random_N2000', 'wet_N2000'] # folder name of models for inferencing


def getEstimates_fromMpth(models_path, testsonglist):
    for tsong in testsonglist:
        output_dir = Path(os.path.join(tsong.replace(".mp3", ""), "Estimates", os.path.basename(models_path)))
        if not os.path.exists(output_dir):
            output_dir.mkdir(exist_ok = True, parents = True)
            tsong_audio, rate = sf.read(tsong, always_2d = True)
            start_t = time.time()
            estimates = separate(audio=tsong_audio, targets = ['violin', 'piano'], 
                         device = device, model_name = models_path)
            end_t = time.time()
            total_time=end_t-start_t
            print("Takes {} secs to separate song:{}".format(total_time, Path(tsong).stem))
            for target, estimate in estimates.items():
                sf.write(
                    str(output_dir / Path(target).with_suffix('.mp3')),
                    estimate,
                    samplerate)
if __name__=='__main__':
    # inference and save estimates
    for eachmethod in model_list:
        model_path = os.path.join(model_dir, eachmethod)
        print("===Inferencing using :{}===".format(eachmethod))
        getEstimates_fromMpth(model_path, tsong_list)