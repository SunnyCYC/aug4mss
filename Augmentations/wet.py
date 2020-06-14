# -*- coding: utf-8 -*-
"""
Created on Mon May  4 11:58:09 2020

@author: CITI
"""

#%%
"""
assume non-processed random clipped data arranged like:
    main_audio_dir/train/piano/stems.wav
    main_audio_dir/train/violin/stems.wav
    main_audio_dir/valid/piano/stems.wav
    main_audio_dir/valid/violin/stems.wav

this script will go through all stems in all folders, 
    and apply augmentation with probability of 30% 
    
    output would be arranged like:
        outupt_main_dir/train/piano/stems.wav
                       /train/violin/stems.wav
                       /valid/piano/stems.wav
                       /valid/violin/stems.wav

"""
from pathlib import Path
import torch.utils.data
import random
import os
import soundfile as sf
import sox
import colorednoise as cn
import glob


class NrSoxAugmentation(object):
    def __init__(self, output_dir, threshold = 0.3):
        self.output_dir = output_dir
        # constrast
        self.contrast_bool = random.random() < threshold
        self.contrast_val = random.randint(1, 70)
        # equalizers
        self.eq_bool = random.random() < threshold
        self.eq_freq1 = random.randint(32, 4096)
        self.eq_freq2 = random.randint(32, 4096)
        self.width_q = 2
        self.gain_db1 = random.uniform(-10, 5)
        self.gain_db2 = random.uniform(-10, 5)
        # reverb
        self.reverb_bool= random.random() < threshold
        self.reverb_val = random.randint(1, 70)
        # pinknoise
        self.pinknoise_bool = random.random() < threshold
        self.pn_vol = random.uniform(0.01, 0.04)

    def transform(self, input_dir):
        tfm = sox.Transformer()
        if self.contrast_bool:
            tfm.contrast(self.contrast_val)
        if self.eq_bool:
            tfm.equalizer(self.eq_freq1, self.width_q, self.gain_db1)
            tfm.equalizer(self.eq_freq2, self.width_q, self.gain_db2)
        if self.reverb_bool:
            tfm.reverb(self.reverb_val)
        if self.pinknoise_bool:
            # if pinknoise is required, output and temp wav to load and add pinknoise
            output_fname_tmp = Path(input_dir).stem+"_tmp.wav"
            output_fdir_tmp = os.path.join(self.output_dir, output_fname_tmp )
            tfm.build(input_dir, output_fdir_tmp)
            
            audio_clean, rate = sf.read(output_fdir_tmp)
            pinknoise =cn.powerlaw_psd_gaussian(1, len(audio_clean))
            audio_noisy = audio_clean + self.pn_vol * pinknoise
            output_fname = Path(input_dir).stem+".wav"
            output_fdir = os.path.join(self.output_dir, output_fname)
            sf.write(output_fdir, audio_noisy, rate)
            # delete the tmp file
            try :
                os.remove(output_fdir_tmp)
            except OSError as e:
                print(e)
            else:
                print("removed:", output_fdir_tmp)
        else:
            output_fname = Path(input_dir).stem+".wav"
            output_fdir = os.path.join(self.output_dir, output_fname)
            tfm.build(input_dir, output_fdir)

def main():
    
    main_audio_dir = None # like:'/xxx/'
    split_dirs =['train', 'valid']
    instruments = ['violin', 'piano']
    
    # output dirs
    process_name = "WetStems"
    output_audio_dir = None # like:'/xxx/'
    outupt_main_dir = os.path.join(output_audio_dir, process_name)

    for eachsplit in split_dirs:
        for eachinstru in instruments:
            print("====processing {}, {} split====".format(eachinstru, eachsplit))
            input_wavsdir = os.path.join(main_audio_dir, eachsplit, eachinstru)
            input_wavs_glob = os.path.join(input_wavsdir, "*.wav")
            input_clips = list(glob.glob(input_wavs_glob))
            
            # output dir
            if eachinstru == "violin":
                clip_output_dir = Path(outupt_main_dir)/Path(eachsplit)/Path("violin")
            elif eachinstru == "piano":
                clip_output_dir = Path(outupt_main_dir)/Path(eachsplit)/Path("piano")
            clip_output_dir.mkdir(parents = True, exist_ok = True)
            for eachclip in input_clips:
                """ apply sox aug here """
                NSA = NrSoxAugmentation(clip_output_dir)
                NSA.transform(eachclip)

if __name__ =='__main__':
    main()
