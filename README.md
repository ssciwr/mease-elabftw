# mease-elabftw

[![tests](https://github.com/ssciwr/mease-elabftw/workflows/Tests/badge.svg)](https://github.com/ssciwr/mease-elabftw/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/ssciwr/mease-elabftw/branch/main/graph/badge.svg?token=xJTHCFXzrz)](https://codecov.io/gh/ssciwr/mease-elabftw)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ssciwr_mease-elabftw&metric=alert_status)](https://sonarcloud.io/dashboard?id=ssciwr_mease-elabftw)

Work-in-progress script / simple python library for extracting
[metadata](https://doc.elabftw.net/metadata.html) from
[eLabFTW](https://www.elabftw.net/) experiments and converting it to
[NWB](https://nwb-schema.readthedocs.io/en/latest/) format, for use with
the [mease-lab-to-nwb](https://github.com/ssciwr/mease-lab-to-nwb) SpikeInterface pipeline.

## How to use

To use, you need to generate an API key in eLabFTW (User Panel -> API Keys -> GENERATE AN API KEY),
and then set the environment variable `ELABFTW_TOKEN` to this key, e.g.

```bash
export ELABFTW_TOKEN=abc123abc123abc123
```

Example of use:

```pycon
>>> import mease_elabftw
>>> mease_elabftw.list_experiments("Liam")
['163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)', '156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)']
>>> mease_elabftw.get_metadata(156)
{'Session start time': {'type': 'date', 'value': '2021-01-01'}, 'Session description': {'type': 'text', 'value': 'description of session'}}
```
