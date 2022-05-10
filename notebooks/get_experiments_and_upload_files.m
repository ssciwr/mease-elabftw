% Example of using the mease_elabftw python library from matlab

% note: python needs to be on the matlab path
% e.g. run matlab from a command line inside the measelab conda environment

% note: mease_elabftw needs to be installed
% e.g. run `pip install mease_elabftw` from a command line inside the measelab conda environment

% note: you also need to have exported a valid alebftw API token
% e.g. `export ELABFTW_TOKEN=abc123abc123abc123` on the command line before running matlab

% list all experiments by user
py.mease_elabftw.list_experiments("Liam")

% get all info for an experiment
exp = struct(py.mease_elabftw.util.get_experiment(156))

% upload a file to an experiment
py.mease_elabftw.upload_file(1128, "test.txt")
