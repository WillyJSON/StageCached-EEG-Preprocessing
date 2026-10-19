import numpy as np

from stagecached_eeg_preprocessing import core, default_steps


def test_proteus_metadata_is_consistent():
    assert len(core.subjects) == 10
    assert len(core.ch_names) == len(core.ch_types) == 41
    assert core.sfreq == 500
    assert default_steps()["is_load_cached_mat"]


def test_build_valid_raw_with_proteus_shape():
    data = {"synthetic": [{"X": np.zeros((41, 100), dtype=np.float32)}]}
    raws = core.build_valid_raw(
        data_dic=data,
        ch_names=core.ch_names,
        ch_types=core.ch_types,
        sfreq=core.sfreq,
        montage_name=core.montage_name,
    )
    raw = raws["synthetic0"]
    assert raw.get_data().shape == (41, 100)
    assert raw.info["sfreq"] == 500
