# Rio Buses GPS Data Collection

## Description

Project for the extraction of GPS points from buses in the city of Rio de Janeiro.

The GPS points are collected from the [endpoint](http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes) provided by Rio de Janeiro City Hall.

The [API](http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes) only provides the GPS positions of the buses in real time. No historical data is available.

The main objective of this project is to store the raw data to create a historical dataset of buses trajectories for further analysis.

## Script Steps

The script executes 4 main steps:

1. Requests current GPS positions from API.
2. Stores the GPS points in a temporary local file.
3. Uploads the temporary local file to a given S3 bucket
4. Delete the temporary file.

## Project Structure

```
.
├── README.md
├── requirements.txt
└── rio_gps
    ├── __init__.py
    ├── config
    │   ├── config.cfg
    │   ├── logging.cfg
    ├── entry.py
    ├── persistence.py
    └── request.py
```

The project has three modules:

* `request.py`: retrieves GPS data from the API.
* `persitence.py`: provides functions to write temporary local files and upload to AWS S3.
* `entry`: implements the execution flow.
  
The folder `config` contains the configuration files.

## How to use it

### Requirements

* `python >= 3.6`
* `boto3`
* `requests`

### Script Execution

The script demans only two arguments, the configuration file and the logging configuration file.

Use the following command to run it:

```bash
python entry.py --config /path/to/config/file --logging-config /path/to/logging_config/file
```

### Current Deploy

The project currently runs in an EC2 machine at AWS.

The execution occurs at every 40 seconds.
