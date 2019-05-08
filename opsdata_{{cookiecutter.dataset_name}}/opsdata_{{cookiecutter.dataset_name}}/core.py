"""
ObsPlus instructions for downloading dataset.
"""
import obsplus
from obsplus import DataSet


class {{ cookiecutter.dataset_name.capitalize() }}(DataSet):
    """
    {{ cookiecutter.dataset_description }}
    """
    name = "{{ cookiecutter.dataset_name }}"

    def download_events(self):
        """ A function to download event data  and store it in self.event path """
        super().download_events()

    def download_waveforms(self):
        """ A function to download waveform data """
        super().download_waveforms()

    def download_stations(self):
        """ A function to download waveform data """
        super().download_stations()
