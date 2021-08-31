# gpu-monitor

## Description

This project is for monitoring the status of the gpu server being used.

## How to run
1. Install required libraries
```shell
pip install -r requirements.txt
```

2. Execute the code following command.
```shell
python app.py --webhook_url <SLACK_WEB_HOOK_URL> --server_name <SERVER_NAME>
```

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## TODO

* [x] Function to get gpu information
* [x] Function to send the current server status to the slack bot
* [ ] Function that writes the current server state to a google spreadsheet.
* [ ] Easy to use using Dockerfile