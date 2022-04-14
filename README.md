# mease-elabftw

[![pypi](https://img.shields.io/pypi/v/mease-elabftw.svg)](https://pypi.org/project/mease-elabftw)
[![docs](https://readthedocs.org/projects/mease-elabftw/badge/?version=latest)](https://mease-elabftw.readthedocs.io/en/latest/?badge=latest)
[![tests](https://github.com/ssciwr/mease-elabftw/workflows/Tests/badge.svg)](https://github.com/ssciwr/mease-elabftw/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/ssciwr/mease-elabftw/branch/main/graph/badge.svg?token=xJTHCFXzrz)](https://codecov.io/gh/ssciwr/mease-elabftw)
[![sonar](https://sonarcloud.io/api/project_badges/measure?project=ssciwr_mease-elabftw&metric=alert_status)](https://sonarcloud.io/dashboard?id=ssciwr_mease-elabftw)

A Python library for interacting with [eLabFTW](https://www.elabftw.net/) experiments:

- Create [NWB](https://nwb-schema.readthedocs.io/en/latest/) metadata from an eLabFTW experiment
- Upload files (e.g. analysis result from HPC) to an eLabFTW experiment
- List eLabFTW experiments from the command line

## Setup

```bash
python -m pip install mease-elabftw
```

To authenticate requests to the eLabFTW server you also need to generate an API key in eLabFTW (User Panel -> API Keys -> GENERATE AN API KEY),
and then set the environment variable `ELABFTW_TOKEN` to this key, e.g.

```bash
export ELABFTW_TOKEN=abc123abc123abc123
```

## Use in Python

Get nwb metadata from an elabftw experiment to use in [mease-lab-to-nwb](https://github.com/ssciwr/mease-lab-to-nwb):

```pycon
>>> import mease_elabftw
>>> mease_elabftw.list_experiments("Liam")
['163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)', '156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)']
>>> metadata = mease_elabftw.get_nwb_metadata(156)
>>> metadata["NWBFile"]["session_description"]
test fake experiment with json metadata
>>> metadata["NWBFile"]["identifier"]
20211001-8b6f100d66f4312d539c52620f79d6a503c1e2d1
```

## Use from terminal

List all experiments on elabftw belonging to user "Liam":

```bash
$ elabftw-list Liam
163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)
156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)
```
