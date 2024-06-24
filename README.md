# ip-cameras-private

## Python 3 script able to check the availability of several IP Cameras via RTSP

### Details

* ProcessPoolExecutor used in order to connect to the cameras in parallel and reduce the amount of time needed to complete this task
* It provides some stats at the end of the execution. Check [sample_execution_results.txt](https://github.com/mvarrone/ip-cameras-private/blob/master/sample_execution_results.txt)
* Each camera is represented as a Python 3 dictionary, stored in *credentials.json* file. This file is a list of dictionaries containing the following structure:

    *Example:*

        {
                "protocol": "rtsp",
                "username": "admin",
                "password": "password",
                "domain": "domain.dyndns.org",
                "port": 554,
                "path": "/Streaming/Channels/",
                "camera_number": 101
        }

### RTSP IP Camera URL example

```python
rtsp://admin:password@domain.dyndns.org:554/Streaming/Channels/101
```