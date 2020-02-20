# -*- coding: utf-8 -*-
""" Top-level package for {{ cookiecutter.dataset_name }}."""
from pathlib import Path

from opsdata_{{ cookiecutter.dataset_name }}.version import __version__

source_path = Path(__file__).parent / "{{ cookiecutter.dataset_name }}"
