# opsdata

This is a template for creating [ObsPlus](www.github.com/niosh-mining/obsplus)
datasets. It allows you to share datasets, or instructions for downloading datasets,
with others simply and easily. Without much effort you can even make them pip-installable.

In order to proceed you need to first download cookiecutter:

```bash
pip install cookiecutter
```

then create your dataset:

```bash
cookiecutter gh:seismopy/opsdata
```

Follow the prompts when asked for name, email, etc.

Now you can open up the newly created package (which will be created in the
current working directory with the name assigned to `dataset_name`)
and do the following:

1) add the logic needed for downloading station, event, and/or waveform data
in the places indicated by the comments, and/or

2) add the data (in any obspy-readable format) to the data directory in the
appropriate subdirectory, or at the top level if the data cannot be classified
by waveform, station, or event tags. Only add small datasets (<200 mb),
else prefer option 1 for larger data sections.

3) Fill in the information in the readme.

## Uploading to PyPI

In order to upload to pypi you need to first create a
[pypi account](https://pypi.org/account/register/). Then, from the newly created
directory, you can simply run the following commands:

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Notes
This was originally based on [this](https://github.com/audreyr/cookiecutter-pypackage)
cookiecutter template. We appreciate the all the great work the folks behind the
[cookiecutter project](https://github.com/audreyr/cookiecutter) have done.
