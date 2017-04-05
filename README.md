# ![](icon.png) Klima
**Klima** is a utility that polls serial or filesystem devices for climate data, exposes them through a RESTful API, and (optionally) aggregates the data into [InfluxDB](https://github.com/influxdata/influxdb) for tracking climate data over time.

## API
All times returned are in UTC, all temperatures are in Celsius, and all humidity values are relative percentages.

### Display a summary page
```
GET /
```

#### Parameters

None.

#### Example

N/A

### Get the current sensor reading
```
GET /api/:sensor_type
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|           |

##### Example
```
GET /api/temperature
```
Get the current temperature.

##### Response
```json
{
  "time": "2017-04-04T00:00:01.429856Z",
  "value": 18.7
}
```

### Get the sensor reading at a previous time
This requires **historical data** to be configured, and for data to exist 
at the requested time. 

Otherwise, it returns a `204`.
```
GET /api/:sensor_type/:timescale
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|
| `timescale`   | A [relative timescale](https://docs.influxdata.com/influxdb/v1.2/query_language/spec/#durations) before the current time.|

##### Example
```
GET /api/humidity/5m
```
Get the relative humidity 5 minutes ago.

##### Response
```json
{
  "time": "2017-04-04T23:61:42.138746Z",
  "value": 45.0
}
```

### Fetch current climate data for the configured location
This _does not use sensors_, and requires **location** to be configured. Otherwise, it returns a `204`.
```
GET /api/:sensor_type/location
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|

##### Example
```
GET /api/temperature/location
```
Fetches the current temperature for the configured location (in `config.py`).

##### Response
```json
{
  "time": "2017-04-04T20:01:42.123481Z",
  "value": 16.1
}
```

### Fetch climate data for a previous time
This _does not use sensors_, requires both **location** and **historical data** to be configured, and for data to exist 
at the requested time. 

Otherwise, it returns a `204`.
```
GET /api/:sensor_type/location/:timescale
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|
| `timescale`   | A [relative timescale](https://docs.influxdata.com/influxdb/v1.2/query_language/spec/#durations) before the current time.|

##### Example
```
GET /api/temperature/location/16s
```
Fetches the current temperature for the configured location 16 seconds ago.

##### Response
```json
{
  "time": "2017-04-04T21:22:36.189163Z",
  "value": 16.0
}
```

### Get the difference between sensor data and climate/location data
This requires **location** to be configured. Otherwise, it returns a `204`.
```
GET /api/:sensor_type/location/diff
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|

##### Example
```
GET /api/humidity/location/diff
```
Gets the current difference between the outside and sensor relative humidity values.

##### Response
```json
{
  "time": "2017-04-03T06:14:00.582916Z",
  "value": -0.6
}
```

### Get the difference between sensor data and climate/location data at a previous time
This requires both **location** and **historical data** to be configured, and for data to exist 
at the requested time. 

Otherwise, it returns a `204`.
```
GET /api/:sensor_type/location/diff/:timescale
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|
| `timescale`   | A [relative timescale](https://docs.influxdata.com/influxdb/v1.2/query_language/spec/#durations) before the current time.|

##### Example
```
GET /api/humidity/location/diff/2d
```
Gets the difference between the outside and sensor relative humidity values 2 days ago.

##### Response
```json
{
  "time": "2017-04-02T01:22:06.859212Z",
  "value": 4.1
}
```

### Get the average difference between sensor data and climate/location data from a previous time
This requires both **location** and **historical data** to be configured, and for data to exist 
at the requested time. 

Otherwise, it returns a `204`.
```
GET /api/:sensor_type/location/diff/avg/:timescale
```

#### Parameters

| Name          |                        Description |
|---------------|------------------------------------|
| `sensor_type` | One of `temperature` or `humidity`.|
| `timescale`   | A [relative timescale](https://docs.influxdata.com/influxdb/v1.2/query_language/spec/#durations) before the current time.|

##### Example
```
GET /api/humidity/location/diff/avg/24h
```
Gets the average difference between outside and inside relative humidities over the past 24 hours.

##### Response
```json
{
  "time": "2017-04-04T05:10:13.502812Z",
  "value": -4.6
}
```

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

