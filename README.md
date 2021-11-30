# mease-elabftw

[![tests](https://github.com/ssciwr/mease-elabftw/workflows/Tests/badge.svg)](https://github.com/ssciwr/mease-elabftw/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/ssciwr/mease-elabftw/branch/main/graph/badge.svg?token=xJTHCFXzrz)](https://codecov.io/gh/ssciwr/mease-elabftw)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ssciwr_mease-elabftw&metric=alert_status)](https://sonarcloud.io/dashboard?id=ssciwr_mease-elabftw)

Python library for extracting
[metadata](https://doc.elabftw.net/metadata.html) from
[eLabFTW](https://www.elabftw.net/) experiments and converting it to
[NWB](https://nwb-schema.readthedocs.io/en/latest/) metadata, for use with
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

## Use in Python

Get nwb metadata from an elabftw experiment to use in [mease-lab-to-nwb](https://github.com/ssciwr/mease-lab-to-nwb):

```pycon
>>> import mease_elabftw
>>> from pprint import pprint
>>> pprint(mease_elabftw.list_experiments("Liam"))
['163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)',
 '156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)']
>>> pprint(mease_elabftw.get_nwb_metadata(156))
{'Ecephys': {},
 'NWBFile': {'experimenter': 'Liam Keegan',
             'identifier': '20211001-8b6f100d66f4312d539c52620f79d6a503c1e2d1',
             'institution': 'Heidelberg University, Physiology and '
                            'Pathophysiology',
             'lab': 'Medical Biophysics, Groh/Mease',
             'session_description': 'test fake experiment with json metadata',
             'session_start_time': '2021-10-01 11:13:47',
             'virus': 'AAVretr ChR2-tdTomato:\n'
                      '  * Virus in -80 storage: AAVrg-CAG-hChR2-tdTomato (AAV '
                      'Retrograde)\n'
                      '  * Origin: Addgene\n'
                      '  * Comments: retrograde\n'
                      '  * Expression Quality: \n'
                      '  * product number: \n'
                      'AAVretr Flpo:\n'
                      '  * Virus in -80 storage: AAVretr EF1a-Flpo\n'
                      '  * Origin: Addgene\n'
                      '  * Comments: retrograde Flip\n'
                      '  * Expression Quality: \n'
                      '  * product number: 55637-AAVrg\n'},
 'Subject': {}}
```

## Use from terminal

List all experiments on elabftw belonging to user "Liam":

```bash
liam@ssc:~$ elabftw-list Liam
163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)
156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)
```
