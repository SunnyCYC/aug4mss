# -*- coding: utf-8 -*-
"""
Created on Sun May  3 16:07:42 2020
Note: This code is modified from this project : 
    https://github.com/sigsep/open-unmix-pytorch by Fabian-Robert Stöter, Antoine Liutkus, Inria and LIRMM, Montpellier, France

@author: CITI
"""
import os
import torch
import numpy as np
import soundfile as sf
import norbert
import json
from pathlib import Path
import scipy.signal
import model
import utils
import tqdm
from contextlib import redirect_stderr
import io

models_path = None #'/xxx/path_of_model_dir/'
cuda_num = None # 0
cuda_str = None # "cuda:"+str(cuda_num)
device = None # torch.device(cuda_str if torch.cuda.is_available() else "cpu")

def load_model(target, model_name='umxhq', device='cpu', chkpnt = False):
    """
    target model path can be either <target>.pth, or <target>-sha256.pth
    (as used on torchub)
    """
    model_path = Path(model_name).expanduser()
    if not model_path.exists():
        print("Can't find model! Please check model_path.")

    else:
        # load model from disk
        with open(Path(model_path, target + '.json'), 'r') as stream:
            results = json.load(stream)
        if not chkpnt: 
            target_model_path = next(Path(model_path).glob("%s*.pth" % target))
            state = torch.load(
                    target_model_path,
                    map_location=device
                    )
        else: # using chkpnt instead of pth
            target_model_path = next(Path(model_path).glob("%s*.chkpnt" % target))
            state = torch.load(
                    target_model_path,
#                    map_location=device
                    )['state_dict']

        max_bin = utils.bandwidth_to_max_bin(
            state['sample_rate'],
            results['args']['nfft'],
            results['args']['bandwidth']
        )

        unmix = model.OpenUnmix(
            n_fft=results['args']['nfft'],
            n_hop=results['args']['nhop'],
            nb_channels=results['args']['nb_channels'],
            hidden_size=results['args']['hidden_size'],
            max_bin=max_bin
        )

        unmix.load_state_dict(state)
        unmix.stft.center = True
        unmix.eval()
        unmix.to(device)
        return unmix


def istft(X, rate=44100, n_fft=4096, n_hopsize=1024):
    t, audio = scipy.signal.istft(
        X / (n_fft / 2),
        rate,
        nperseg=n_fft,
        noverlap=n_fft - n_hopsize,
        boundary=True
    )
    return audio
def separate(
    audio,
    targets=['violin', 'piano'],
    model_name=models_path,
    niter=1, softmask=False, alpha=1.0,
    residual_model=False, device=device
):
    """
    Performing the separation on audio input

    Parameters
    ----------
    audio: np.ndarray [shape=(nb_samples, nb_channels, nb_timesteps)]
        mixture audio

    targets: list of str
        a list of the separation targets.
        Note that for each target a separate model is expected
        to be loaded.

    model_name: str
        name of torchhub model or path to model folder, defaults to `umxhq`

    niter: int
         Number of EM steps for refining initial estimates in a
         post-processing stage, defaults to 1.

    softmask: boolean
        if activated, then the initial estimates for the sources will
        be obtained through a ratio mask of the mixture STFT, and not
        by using the default behavior of reconstructing waveforms
        by using the mixture phase, defaults to False

    alpha: float
        changes the exponent to use for building ratio masks, defaults to 1.0

    residual_model: boolean
        computes a residual target, for custom separation scenarios
        when not all targets are available, defaults to False

    device: str
        set torch device. Defaults to `cpu`.

    Returns
    -------
    estimates: `dict` [`str`, `np.ndarray`]
        dictionary of all restimates as performed by the separation model.

    """
    # convert numpy audio to torch
    audio_torch = torch.tensor(audio.T[None, ...]).float().to(device)

    source_names = []
    V = []

    for j, target in enumerate(tqdm.tqdm(targets)):
        unmix_target = load_model(
            target=target,
            model_name=model_name,
            device=device
        )
        Vj = unmix_target(audio_torch).cpu().detach().numpy()
        if softmask:
            # only exponentiate the model if we use softmask
            Vj = Vj**alpha
        # output is nb_frames, nb_samples, nb_channels, nb_bins
        V.append(Vj[:, 0, ...])  # remove sample dim
        source_names += [target]

    V = np.transpose(np.array(V), (1, 3, 2, 0))

    X = unmix_target.stft(audio_torch).detach().cpu().numpy()
    # convert to complex numpy type
    X = X[..., 0] + X[..., 1]*1j
    X = X[0].transpose(2, 1, 0)

    if residual_model or len(targets) == 1:
        V = norbert.residual_model(V, X, alpha if softmask else 1)
        source_names += (['residual'] if len(targets) > 1
                         else ['accompaniment'])

    Y = norbert.wiener(V, X.astype(np.complex128), niter,
                       use_softmask=softmask)

    estimates = {}
    for j, name in enumerate(source_names):
        audio_hat = istft(
            Y[..., j].T,
            n_fft=unmix_target.stft.n_fft,
            n_hopsize=unmix_target.stft.n_hop
        )
        estimates[name] = audio_hat.T

    return estimates