# StageCached EEG Preprocessing

A stage-cached EEG preprocessing framework for the NeurIPS BCI Competition 2026 warm-up work. The canonical pipeline targets the PROTEUS dataset (41 EEG channels, 500 Hz) and uses MNE-Python.

## Design

The pipeline is organized as independently cached stages:

1. Load and normalize MATLAB recordings.
2. Build MNE Raw objects with channel metadata and montage.
3. Detect and interpolate bad channels.
4. Apply pre-ICA filtering and re-referencing.
5. Fit and cache ICA on a dedicated high-pass filtered copy.
6. Inspect or automatically reject ICA artifacts, then reconstruct the signal.
7. Apply final analysis-band filtering.

Every stage records a parameter/version-sensitive cache key and upstream cache identifier. A later stage can resume from its own valid cache without silently using artifacts produced by incompatible upstream settings.

## Repository layout

- src/stagecached_eeg_preprocessing/core.py: canonical PROTEUS pipeline and cached stages.
- src/stagecached_eeg_preprocessing/__init__.py: public API and safe default launcher.
- src/stagecached_eeg_preprocessing/__main__.py: module entry point.
- src/Preprocessing_PROTEUS.py: backward-compatible import/execute shim.
- data/PROTEUS/preprocessing_config.py: dataset channel/order metadata.
- data/PROTEUS/README.md: dataset conversion and format notes.
- tests/test_smoke.py: no-data import/configuration smoke test.

Raw MAT recordings, generated caches, figures, local experiment outputs, and conversion archives are intentionally excluded from Git.

## Installation

Python 3.12+ is required. Run uv sync.

The package declares the preprocessing dependencies. If automatic bad-channel detection or automatic ICA component labeling is enabled, install optional packages with: uv add pyprep mne-icalabel

## Dataset setup

Place converted PROTEUS P01.mat through P10.mat files under data/PROTEUS/. They are not part of this repository. Consult data/PROTEUS/README.md for the expected MATLAB schema, units, label mapping, and provenance.

## Run

The default launcher begins from raw MAT loading and performs automatic bad-channel detection/interpolation. Adjust default_steps() in src/stagecached_eeg_preprocessing/__init__.py to deliberately enable later stages.

Run the module with: uv run python -m stagecached_eeg_preprocessing

The backward-compatible path is: uv run python src/Preprocessing_PROTEUS.py

## Validation

Run: uv run python -m pytest tests -q

Build the package with: uv build

The smoke test does not need the raw dataset; it validates package import, PROTEUS metadata, and Raw construction with synthetic data.

## Notes

- Manual bad-channel and ICA decisions are stored separately in configs/PROTEUS/.
- Cache/result directories are generated locally and ignored by Git.
- Legacy Scherer and ShallowNet prototypes remain in the local working directory but are intentionally excluded from this focused framework release.
