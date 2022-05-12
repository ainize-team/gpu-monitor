# gpu-monitor

## Description

This project is for monitoring the status of the gpu server being used.

## How to run

1. git clone

```bash
git clone https://github.com/ainize-team/gpu-monitor.git
cd gpu-monitor
```

2. set virtual environment

```bash
python -m venv .venv
. .venv/bin/activate
```

3. install packages

```bash
pip install -r requirements.txt
```

4. run gpu monitoring

```bash
python app.py --server_name ${serverName} --webhook_url ${webhook_url} --interval ${interval} --utilization_threshold ${utilization_threshold} --time_threshold ${time_threshold}
```

## Example

```bash
python app.py --server_name a100 --webhook_url https://hooks.slack.com/services... --interval 600 --utilization_threshold 80 --time_threshold 1200
```

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## TODO

- [x] Function to get gpu information
- [x] Function to send the current server status to the slack bot
- [ ] Function that writes the current server state to a google spreadsheet.
- [ ] Easy to use using Dockerfile
