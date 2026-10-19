"""PROTEUS settings for the existing Preprocessing.py reader/build functions.
Run from the repository root. Use separate PROTEUS cache/result folders.
"""
from pathlib import Path

subjects = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
data_folder = Path("./data/PROTEUS")
ch_names = ['C2', 'CP2', 'P2', 'Pz', 'CPz', 'Cz', 'C1', 'CP1', 'P1', 'P3', 'PO7', 'P5', 'TP7', 'CP5', 'CP3', 'C3', 'PO8', 'P6', 'P4', 'TP8', 'CP6', 'CP4', 'C6', 'C4', 'FC6', 'FC4', 'FC2', 'F6', 'F4', 'F2', 'AF4', 'AF3', 'F5', 'F3', 'F1', 'Fz', 'FC5', 'FC3', 'FC1', 'FCz', 'C5']
ch_types = ['eeg'] * len(ch_names)
sfreq = 500
montage_name = "colin27_1005"
convert_index = True
convert_shape = True
scale_factor = 1e-6
classes = ['HAND', 'SUB', 'WORD']
label_map = {'mi': 1, 'sub': 2, 'word': 3}
cache_folder = Path("./cache/PROTEUS")
results_folder = Path("./results/PROTEUS")
