# gpu-monitor

## Description

This project is for monitoring the status of the gpu server being used.

## How to run

1. git clone

```bash
git clone https://github.com/ainize-team/gpu-monitor.git
cd gpu-monitor
```

2. build docker file

```bash
docker build -t gpu-monitor .
```

3. run gpu monitoring

```bash
docker run -d --gpus=all -e SERVER_NAME="YOUR_SERVER_NAME" -e WEBHOOK_URL="YOURE_WEBHOOK_URL" -e INTERVAL=60 -e UTILIZATION_THRESHOLD=40  -e TIME_THRESHOLD=3600 gpu-monitor
```

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## TODO

- [x] Function to get gpu information
- [x] Function to send the current server status to the slack bot
- [ ] Function that writes the current server state to a google spreadsheet.
- [x] Easy to use using Dockerfile
