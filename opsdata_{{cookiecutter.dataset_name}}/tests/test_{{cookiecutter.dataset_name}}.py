#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `{{ cookiecutter.dataset_name }}` obsplus dataset.
"""
from pathlib import Path

import obsplus
import pytest
from obsplus.interfaces import EventClient, WaveformClient, StationClient

CLIENT_TYPE = {
    "waveform": WaveformClient,
    "event": EventClient,
    "station": StationClient,
}


@pytest.fixture(scope="session")
def dataset():
    """
    Load the new dataset via obsplus plugin.
    """
    return obsplus.load_dataset("{{ cookiecutter.dataset_name }}")


@pytest.fixture(scope="session")
def clients(dataset):
    """ return a dict of clients. """
    clients = dict(
        waveform=dataset.waveform_client,
        event=dataset.event_client,
        station=dataset.station_client,
    )
    return clients


def test_dataset(dataset):
    """ A simple tests to make sure the data have been loaded. """
    assert Path(dataset.data_path).exists()


def test_return_clients(clients):
    """ Ensure each client type is returned. """
    for cli_type, client in clients.items():
        expected_type = CLIENT_TYPE[cli_type]
        assert isinstance(client, expected_type) or client is None
