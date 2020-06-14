# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:40:18 2020

After assigning the required info in main(), 
this script can generate an correlation2d table for all violin/piano pairs

@author: CITI
"""

#%%
import librosa
import soundfile as sf
import numpy as np
from scipy import signal
import os 
import glob
from pathlib import Path
from multiprocessing import Pool
import pickle


def get_overlap_interval(a_interval, b_interval):
    """ 
    get the intervals when non-silence violin/piano stems overlap:
    input: violin non-silence interval, piano non-silence interval
    output: overlap intervals when violin and piano overlap
    """
    overlap_interval = []
    for s_a, e_a in a_interval:
        for s_b, e_b in b_interval:
            if s_a >= s_b and s_a <= e_b:
                start = s_a
                end = min(e_a, e_b)
                overlap_interval.append([start, end])
            elif s_b >= s_a and s_b <= e_a:
                start = s_b
                end = min(e_a, e_b)
                overlap_interval.append([start, end])
    return overlap_interval

def mergeNS(ori_audio, interval):
    """ 
    merge all the intervals into one audio
    """
    if len(interval) > 0 :
        merged_nsilence = ori_audio[interval[0][0]:interval[0][ 1]][:, np.newaxis]
        for start, end in interval[1:]:
            merged_nsilence = np.vstack([merged_nsilence, ori_audio[start:end][:, np.newaxis]])
        return merged_nsilence
    else:
        print("====== no overlap ======")
        return 0
        
def corr2d_worker(argslist, topdb = 30):
    # read violin, piano audio
    path_a, path_b = argslist
    audio_a, rate = sf.read(path_a)
    audio_b, rate = sf.read(path_b)
    
    # get the nonsilence intervals using librosa.effects.split
    a_interval = librosa.effects.split(audio_a, top_db = topdb)
    b_interval = librosa.effects.split(audio_b, top_db = topdb)
    
    # get the intervals when violin overlaps with piano
    overlap_interval = get_overlap_interval(a_interval, b_interval)
    
    # try to merge all the intervals to create nonsilence violin/piano stems
    try:
        merged_a = mergeNS(audio_a, overlap_interval)
        merged_b = mergeNS(audio_b, overlap_interval)
    except Exception:
        print("Error in mergeNS ")
        return "Error mns"
    # try to calculate corrlelation2d of derived stems, if no overlapped (len(merged_ab) ==0), error would occur
    try:
        correlation2d = signal.correlate2d(merged_a, merged_b, boundary = 'symm', mode = 'valid')
        print("===calculating corrcoef of {}, and {}===".format(Path(path_a).stem, Path(path_b).stem))
    except Exception:
        print("Error in corrcoef ")
        return "Error corr"
    return correlation2d, path_a, path_b


#%%
def main():

    # assign stem paths, table save_dir and table_pickle_fname
    pia_source_dir = None # like: '/xxx/'
    vio_source_dir = None # like: '/xxx/'
    save_dir = None # like: '/xxx/'
    pk_fn = 'corr2d_table.pickle'
    pk_sdir = os.path.join(save_dir, pk_fn)

    piano_clips = list(glob.glob(pia_source_dir+'/*.wav'))
    print("total num piano_clips :", len(piano_clips))
    violin_clips = list(glob.glob(vio_source_dir+'/*.wav'))
    print("total num violin_clips :", len(violin_clips))

    arglist = []
    for each_vio in violin_clips:
        for each_pia in piano_clips:
            arglist.append([each_vio, each_pia])
    
    pool = Pool(30)
    results = pool.map(corr2d_worker, arglist)
    pool.close()
    pool.join()
    
    with open(pk_sdir, 'wb') as file:
        pickle.dump(results, file)

if __name__ =='__main__':
    main()
