# opsdata

This is a template for creating [ObsPlus](www.github.com/niosh-mining/obsplus)
datasets. It allows you create, distribute, and version datasets, or instructions
for downloading datasets, with others simply and easily. 

# Example

In this example we will create a dataset for the 
[sulphur_peak](https://bit.ly/3bNDCnP) sequence, which occurred near the idyllic
town of [Soda Springs Idaho](https://en.wikipedia.org/wiki/Soda_Springs,_Idaho).


## Step 1: Install Dependencies

In order to proceed you need to first download the cookiecutter and twine python packages.
(we assume you have already installed ObsPlus):

```bash
pip install cookiecutter
pip install twine
```

## Step 2: Populate Template

Run cookiecutter to fill in the template.

```bash
cookiecutter gh:seismopy/opsdata
```

Follow the prompts when asked for name, email, etc.

The values entered for the example are:
- author_name: Derrick Chambers
- email: d-chambers@github.com
- dataset_name: sulphur_peak,
- project_url: github.com/d-chambers/opsdata_sulphur_peak,
- dataset_description: A 2017 earthquake sequence occurring in southern Idaho.
- version: 0.1.0

The created directory looks as follows:
```
- opsdata_sulphur_peak
    - opsdata_sulphur_peak
        - core.py
        - __init.py__
        - sulphur_peak
            - example_data_file.txt
        - version.py
    - LICENSE
    - README.md
    - test_data
    - requirements.txt
    - setup.py
    - tests
        - conftest.py
        - test_sulphur_peak.py

```

## Set 3: Fill in Readme

The next thing to do is fill out the `README.md` file. It contains
information about the dataset, including a summary, authors, references, etc.
Feel free to add additional headings and customize this in any way you wish.

The Sulphur Peak's page is shown below, but you may wish to add a bit more detail:

```
# Obsplus Dataset: sulphur_peak

A 2017 southern Idaho (USA) earthquake sequence. 

# More info

This dataset was collected by the University of Utah Seismograph Stations (UUSS) as well a 
temporary network installed by UUSS and the United States Geological Survey. More info
can be found at the 
[sequence's webpage](https://quake.utah.edu/monitoring-research/sulphur-peak-earthquake).

This dataset only includes events available from USGS with minimum magnitudes >= 4.0
and stations within 0.5 degrees of the approximate cluster.


# References

Koper, K. D., Pankow, K. L., Pechmann, J. C., Hale, J. M., Burlacu, R., Yeck, W. L., ... & 
Shearer, P. M. (2018). Afterslip enhanced aftershock activity during the 2017 earthquake
sequence near Sulphur Peak, Idaho. Geophysical Research Letters, 45(11), 5352-5361.

Shokrgozar, A., & Mashal, M. (2019, April). The Mw 5.3 Sulphur Peak Earthquake in Soda
Springs, Idaho: Perspectives from Earthquake Engineering. In Structures Congress (pp. 306-320).
```

You may also want to ensure the default licence (BSD) is adequate for you data. 

## Set 4: Create Download Methods

Next we need to create the code which will download the data. This dataset logic
lives in the `core.py` file. In the example this is in relative path
`opsdata_sulphur_peak/opsdata_sulphur_peak/core.py`. This class is well commented
and shows which methods need to be defined. The first few lines look like this:

```python
"""
ObsPlus instructions for downloading dataset.
"""
from pathlib import Path

from obsplus import DataSet

from opsdata_sulphur_peak import __version__, source_path


class Sulphur_peak(DataSet):
    """
    A 2017 earthquake sequence occurring in southern Idaho.
    """
    name = "sulphur_peak"
    base_path = Path(__file__).parent
    version = __version__

    # --- functions used to specify how data are downloaded

    def download_events(self):
        """ download event data and store them in self.event_path """
        Path(self.event_path).mkdir(exist_ok=True, parents=True)

    def download_waveforms(self):
        """ download waveform data and store them in self.waveform_path """
        Path(self.waveform_path).mkdir(exist_ok=True, parents=True)

    def download_stations(self):
        """ download station data and store them in self.station_path """
        Path(self.station_path).mkdir(exist_ok=True, parents=True)
```
We need to define how event, station, and waveform data are downloaded separately.
If your dataset doesn't have one of these types of data simply don't modify the
method.

Also, you can include any data files you wish in the distribution, but these
should be small in size. Included files should be added to the data directory,
on the same level as `core.py` which shares a name with the dataset. In this case
it is `opsdata_sulphur_peak/opsdata_sulphur_peak/sulphur_peak`. Paths to these
files can then be accessed with `source_path / 'file_name.txt'`. 

### Step 4.1: Download Events

Adding the download event logic, the code now looks like this:

```python
from pathlib import Path

import obsplus
import obspy
from obspy.clients.fdsn import Client

from opsdata_sulphur_peak import __version__, source_path


class Sulphur_peak(obsplus.DataSet):
    """
    A 2017 earthquake sequence occurring in southern Idaho.
    """
    name = "sulphur_peak"
    base_path = Path(__file__).parent
    version = __version__
    longitudes = (-111.6, -111.25)
    latitudes = (42.5, 42.7)
    starttime = obspy.UTCDateTime('2017-01-01')
    endtime = obspy.UTCDateTime('2019-01-01')
    min_magnitude = 4.0
    station_search_degrees = 0.5

    # --- functions used to specify how data are downloaded

    def download_events(self):
        """ download event data and store them in self.event_path """
        client = Client("IRIS")
        # Define inputs to event query
        event_params = dict(
            minlongitude=self.longitudes[0],
            maxlongitude=self.longitudes[1],
            minlatitude=self.latitudes[0],
            maxlatitude=self.latitudes[1],
            starttime=self.starttime,
            endtime=self.endtime,
            minmagnitude=self.min_magnitude,  # minimum magnitude
        )
        # Query iris for data and plot
        cat = client.get_events(**event_params)
        # save event to self.event_path
        obsplus.EventBank(self.event_path).put_events(cat)

```

### Step 4.2: Download Stations

The `download_stations` method for the example is:

```python
    def download_stations(self):
        """ download station data and store them in self.station_path """
        station_path = Path(self.station_path).mkdir(exist_ok=True, parents=True)
        client = Client("IRIS")

        station_params = dict(
            starttime=self.starttime,
            endtime=self.endtime,
            latitude=sum(self.latitudes) / 2.,
            longitude=sum(self.longitudes) / 2.,
            maxradius=self.station_search_degrees,  # radius in degrees
            channel='H*',  # only include channels that start with H
            level='response',  # indicates we want instrument responses
        )

        inv = client.get_stations(**station_params)
        inv.write(str(station_path / 'inventory.xml'), 'stationxml')
```

### Step 4.3: Download waveforms

The `download_stations` method for the example is:
 
```python
    def download_waveforms(self):
        """ download waveform data and store them in self.waveform_path """
        client = Client("IRIS")
        NSLC = ['network', 'station', 'location', 'channel']
        # Times before/after origin to include in waveforms
        time_before = 5  # time before origin to download
        time_after = 95  # time after origin to download
        # Since we need to use the inventory and catalog to determine which
        # channels/times to get data for, make sure those are downloaded first.
        if self.events_need_downloading:
            self.download_events()
        if self.stations_need_downloading:
            self.download_stations()
        # Load inventory and catalog into dataframes.
        inv_df = obsplus.stations_to_df(self.station_path)
        cat_df = obsplus.events_to_df(self.event_path)
        # Create bulk requests for each event and put into a wave bank.
        wbank = obsplus.WaveBank(self.waveform_path)
        for event_series in cat_df.iterrows():
            event_df = inv_df[NSLC]
            time = obsplus.utils.to_utc(event_series['time'])
            event_df['starttime'] = time - time_before
            event_df['endtime'] = time + time_after
            bulk = obsplus.utils.pd.get_waveforms_bulk_args(event_df)
            st = client.get_waveforms_bulk(bulk)
            wbank.put_waveforms(st)
```

## Set 5: Create Download Methods
 


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
