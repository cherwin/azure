# azure

## Install dependencies
```
pip install -r requirements.txt
```

## Export environment variables
```shell
export AZDO_TOKEN="xxxx"
export AZDO_ORG_URL="https://dev.azure.com/<org>"

# Only do this if you actually want to make changes to your backlog
export AZDO_DESTRUCTIVE=1
```

## Run
```
./number_work_items.py -h
usage: number_work_items.py [-h] project team

positional arguments:
  project     The project name
  team        The team name

options:
  -h, --help  show this help message and exit
```
