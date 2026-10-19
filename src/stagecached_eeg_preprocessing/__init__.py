"""Public interface for the StageCached EEG preprocessing framework."""

from .core import *  # Re-export reusable stage functions for notebooks/scripts.
from .core import main as _run_pipeline


def default_steps() -> dict[str, bool]:
    """Return the conservative default stage selection for a fresh dataset run."""
    return {
        "is_load_cached_mat": True,
        "is_build_valid_raw": True,
        "is_view_waveforms": False,
        "is_exclude_bads_and_interpolate": True,
        "is_pre_filter": False,
        "is_set_reference": False,
        "is_ica_cache": False,
        "is_gen_components_topomap": False,
        "is_gen_properties": False,
        "is_mark_artifacts_and_build": False,
        "is_after_filter": False,
    }


def main() -> None:
    """Run the documented conservative default pipeline configuration."""
    _run_pipeline(
        is_dic=default_steps(),
        start="is_load_cached_mat",
        auto_mark_bads=True,
        auto_ica=True,
    )


__all__ = [name for name in globals() if not name.startswith("_")]
