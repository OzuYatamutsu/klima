# ![](icon.png) Klima
**Klima** is a utility that polls serial or filesystem devices for climate data, exposes them through a RESTful API, and (optionally) aggregates the data into [InfluxDB](https://github.com/influxdata/influxdb) for tracking climate data over time.

### API
TODO

### Sample output
TODO

### Requirements
**Klima** is written in Python 3. Collecting serial data through [filesystem device hooks](https://en.wikipedia.org/wiki/Everything_is_a_file) probably only works on Linux (although I haven't tried).

#### Getting up and running
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

