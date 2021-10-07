# mease-elabftw

[![tests](https://github.com/ssciwr/mease-elabftw/workflows/Tests/badge.svg)](https://github.com/ssciwr/mease-elabftw/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/ssciwr/mease-elabftw/branch/main/graph/badge.svg?token=xJTHCFXzrz)](https://codecov.io/gh/ssciwr/mease-elabftw)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ssciwr_mease-elabftw&metric=alert_status)](https://sonarcloud.io/dashboard?id=ssciwr_mease-elabftw)

Work-in-progress simple python library for extracting
[metadata](https://doc.elabftw.net/metadata.html) from
[eLabFTW](https://www.elabftw.net/) experiments and converting it to
[NWB](https://nwb-schema.readthedocs.io/en/latest/) format, for use with
the [mease-lab-to-nwb](https://github.com/ssciwr/mease-lab-to-nwb) SpikeInterface pipeline.

## Setup

To install:

```bash
python -m pip install git+https://github.com/ssciwr/mease-elabftw
```

You also need to generate an API key in eLabFTW (User Panel -> API Keys -> GENERATE AN API KEY),
and then set the environment variable `ELABFTW_TOKEN` to this key, e.g.

```bash
export ELABFTW_TOKEN=abc123abc123abc123
```

This key is needed to authenticate requests to the eLabFTW server.

## Use

```pycon
>>> import mease_elabftw
>>> mease_elabftw.list_experiments("Liam")
['163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)', '156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)']
>>> mease_elabftw.get_metadata(156)
{'Ecephys Device name': {'value': 'Device_ecephys'}, 'ElectrodeGroup name': {'value': 'ElectrodeGroup'}, 'session_description': {'value': 'session description'}, 'ElectrodeGroup device': {'value': 'Device_ecephys'}, 'ElectrodeGroup location': {'value': 'location'}, 'ElectricalSeries_raw name': {'value': 'ElectricalSeries_raw'}, 'ElectricalSeries_raw rate': {'value': '1000.0'}, 'ElectrodeGroup description': {'value': 'description'}, 'ElectricalSeries_raw description': {'value': 'ADDME'}}
```
