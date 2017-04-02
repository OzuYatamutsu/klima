# ![](icon.png) Klima
**Klima** is a utility that polls serial or filesystem devices for climate data, exposes them through a RESTful API, and (optionally) aggregates the data into [InfluxDB](https://github.com/influxdata/influxdb) for tracking climate data over time.

## API
All routes indicate `GET` requests unless otherwise specified. For `{timescale}` arguments, refer to [InfluxDB's documentation on duration literals](https://docs.influxdata.com/influxdb/v1.2/query_language/spec/#durations) for valid options. For endpoints which require additional configuration, returns a `501` unless configured in `config.py`. For `{temperature,humidity}` options, replace with the metric you are trying to query (`temperature` for temperature, `humidity` for humidity).

| Route                                                       | Description                                                                                                                                                                                                                                                                                                                             | Example                                      | Example explanation                                                             |
|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|---------------------------------------------------------------------------------|
| `/`                                                         | Displays a summary page of all data.                                                                                                                                                                                                                                                                                                    | N/A                                          | N/A                                                                             |
| `/api/{temperature,humidity}`                               | Displays the current temperature or humidity reading from the sensor.                                                                                                                                                                                                                                                                   | `GET /api/temperature`                       | Returns current temperature reading                                             |
| `/api/{temperature,humidity}/{timescale}`                   | _Requires historical data._ Displays the temperature or humidity at `{timescale}` before now. Requires historical data to be configured _at the timescale queried_ -- otherwise returns a `204`.                                                                                                                                        | `GET /api/temperature/5m`                    | Returns the temperature 5 minutes ago                                           |
| `/api/{temperature,humidity}/location`                      | _Requires location._ Displays the current outside temperature or humidity for the configured location.                                                                                                                                                                                                                                  | `GET /api/humidity/location`                 | Returns the current outside humidity                                            |
| `/api/{temperature,humidity}/location/diff`                 | _Requires location._ Displays the difference between the current sensor temperature or humidity and the current outside temperature or humidity for the configured location.                                                                                                                                                            | `GET /api/humidity/location/diff`            | Returns the current difference between sensor and outside humidity              |
| `/api/{temperature,humidity}/location/diff/{timescale}`     | _Requires location and historical data._ Displays the difference between the current sensor temperature or humidity and the current outside temperature or humidity at `{timescale}` before now for the given location. Requires historical data and location to be configured _at the timescale queried_ -- otherwise returns a `204`. | `GET /api/humidity/location/diff/2d`         | Returns the difference between sensor and outside humidity 2 days ago           |
| `/api/{temperature,humidity}/location/diff/avg/{timescale}` | _Requires location and historical data._ Calculates the average difference between sensor data and current outside temperature or humidity for a given timescale.                                                                                                                                                                       | `GET /api/temperature/location/diff/avg/24h` | Displays the 24 hour average difference between outside and inside temperatures |

## Sample output
TODO

## Requirements
**Klima** is written in Python 3. Collecting serial data through [filesystem device hooks](https://en.wikipedia.org/wiki/Everything_is_a_file) probably only works on Linux (although I haven't tried).

### Getting up and running
To save historical data, you'll need to install InfluxDB from your favorite package manager, e.g.:
```
sudo apt-get install influxdb
```
It will create a default root user and password, but you may want to create your own credentials and database manually yourself - see [here](https://docs.influxdata.com/influxdb/v1.2/query_language/authentication_and_authorization/) to set it up via the CLI, then enter the relevant information into `config.py`. 

If you don't need historical data collection, set `influx_settings.enabled` to `False`.

To install required libraries:

```
pip install -r requirements.txt
```

Then, modify the config values that apply to you in `config.py`. Finally:

```
python run.py
```

You may need to replace `python` and `pip` with `python3` and `pip3`, respectively, depending on the default version of python installed on your system.

