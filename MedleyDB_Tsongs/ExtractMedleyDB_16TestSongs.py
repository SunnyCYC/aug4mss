# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:40:38 2020

@author: CITI
"""

""" usage: 
    set output_dir, medleyDB_dir
        and the 16 testsongs adopted in the paper can be extract and save to output_dir"""
from pydub import AudioSegment
import os 
import numpy as np
import soundfile as sf
import pickle
from pathlib import Path

target_sr = 44100 # target sampling rate (hz)
output_dir = None # abs path for output_dir
medleyDB_dir = None # abs path for your MedleyDB, like: '/xxx/xxx/MedleyDB/'
song_info_pickle = 'MedleyDB_16tsong_path.pickle'

with open(song_info_pickle, 'rb') as file:
    Tsong_info = pickle.load(file)

def main():
    # confert 16 songs to monoarual, sr = 44100, and save to output_dir
    for eachsong in Tsong_info:
        for p_ind, p_path in enumerate(eachsong['piano_stempath']):
            for v_ind, v_path in enumerate(eachsong['violin_stempaths']):
                piano_path = os.path.join(medleyDB_dir, p_path)
                violin_path = os.path.join(medleyDB_dir, v_path)
                
                # mixture name using stem index:
                mixsong_fn = eachsong['songname']+ '_p'+ str(p_ind)+'_v'+str(v_ind)+'.wav'
                # create Reference folder in output_dir to save groundtruth stems
                ref_savedir = os.path.join(output_dir, mixsong_fn.replace('.wav', ''), "Reference")
                if not os.path.exists(ref_savedir):
                    Path(ref_savedir).mkdir(parents = True, exist_ok = True)
                try:
                    violin_stem = AudioSegment.from_file(violin_path).set_frame_rate(target_sr).set_channels(1)
                    piano_stem = AudioSegment.from_file(piano_path).set_frame_rate(target_sr).set_channels(1)
                except Exception:
                    print("Error in AudioSegment Loading")
                # save groundtruth(reference) stems
                violin_stem.export(os.path.join(ref_savedir, "violin.wav"), format = "wav")
                piano_stem.export(os.path.join(ref_savedir, "piano.wav"), format = "wav")
                # save mixture
                mix_wav = violin_stem.overlay(piano_stem)
                mix_wav.export(os.path.join(output_dir, mixsong_fn), format = "wav")
                
if __name__ == '__main__':
    main()