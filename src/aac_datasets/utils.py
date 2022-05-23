#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from typing import Any

from torch import nn, Tensor
from torch.nn.utils.rnn import pad_sequence

from aac_datasets.audiocaps import AudioCaps
from aac_datasets.clotho import Clotho
from aac_datasets.macs import MACS


def download_audiocaps(
    root: str = ".",
    verbose: int = 1,
    ffmpeg: str = "ffmpeg",
    youtube_dl: str = "youtube-dl",
    load_tags: bool = True,
) -> None:
    AudioCaps.FFMPEG_PATH = ffmpeg
    AudioCaps.YOUTUBE_DL_PATH = youtube_dl

    for subset in AudioCaps.SUBSETS:
        _ = AudioCaps(root, subset, download=True, verbose=verbose, load_tags=load_tags)


def download_clotho(root: str = ".", verbose: int = 1, version: str = "v2.1") -> None:
    for subset in Clotho.SUBSETS_DICT[version]:
        _ = Clotho(root, subset, download=True, verbose=verbose, version=version)


def download_macs(root: str = ".", verbose: int = 1) -> None:
    _ = MACS(root, download=True, verbose=verbose)


class Collate:
    def __init__(self, pad_value: float = 0.0) -> None:
        super().__init__()
        self.pad_value = pad_value

    def __call__(self, batch: list[tuple]) -> tuple:
        audio_batch = [item[0] for item in batch]
        captions_batch = [item[1] for item in batch]

        is_tensor = [isinstance(audio, Tensor) for audio in audio_batch]
        if not all(is_tensor):
            raise TypeError(f"Invalid audio type in Collate. (found {is_tensor=})")

        audio_batch = pad_sequence(audio_batch, batch_first=True, padding_value=self.pad_value)
        return audio_batch, captions_batch


class RandomSelect(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    def forward(self, captions: list[Any]) -> Any:
        index = random.randint(0, len(captions) - 1)
        return captions[index]
