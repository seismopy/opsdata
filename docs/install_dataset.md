# Installing Datasets

## Discovering Datasets.

Datasets are typically installed to pypi with the "opsdata" prefix so you can
simply use pip to search for available packages like so:

```shell script
pip search [opsdata*]
```

This also has the advantage of displaying datasets installed into the active
environment and version information.

## Installing Datasets

Once you know the name of the dataset it can be installed with pip:

```shell script
pip install opsdata-sulphur-peak
```

## Using dataset

Now the datasets can be loaded and used in python.

```python
import obsplus

# The first time the following line is run the dataset will be downloaded
ds = obsplus.load_dataset('sulphur_peak')
# get events
catalog = ds.event_client.get_events()
# get stations
inventory = ds.staion_client.get_stations()
# get waveforms
st = ds.waveform_client.get_waveforms()
```
