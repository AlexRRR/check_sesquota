# check_sesquota
A simple Nagios Plugin for monitoring Amazon SES Quota limits

## Installation
```pip install requirements.txt````

AWS credentials may be passed as parameters or be installed in ~/.boto file or ~/.aws/credentials see http://boto.readthedocs.org/en/latest/boto_config_tut.html
for more info.

## Usage
``` python check_sesquota.py -c 10 -w 20  -r eu-west-1````

*note* us-east1 is the default region.
