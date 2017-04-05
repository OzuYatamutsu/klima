from run import *
from measurement_type import MeasurementType
from influx.influx_adapter import get_data_at_relative_time
from logging import getLogger
from flask import Flask, abort, jsonify

logger = getLogger(__name__)
app = Flask(__name__)

# Initialize thread
current_vals = {}
prog_thread: Thread = MainThread(current_vals)
prog_thread.start()


@app.route('/')
def hello_world():
    return 'TODO'


@app.route('/api/<string:metric_type>')
def get_current_temp_or_humidity(metric_type: str):
    if metric_type == 'temperature':
        return str(current_vals['current_temp'])
    elif metric_type == 'humidity':
        return str(current_vals['current_humidity'])
    else:
        abort(404)


@app.route('/api/<string:metric_type>/<string:timescale>')
def get_temp_or_humidity_at_time(metric_type: str, timescale: str):
    result = {}

    if metric_type == 'temperature':
        result = get_data_at_relative_time(MeasurementType.SENSOR_TEMPERATURE, timescale)
    elif metric_type == 'humidity':
        result = get_data_at_relative_time(MeasurementType.SENSOR_HUMIDITY, timescale)
    else:
        abort(404)

    if result == 0.0:
        return '', 204
    return jsonify(result)


@app.route('/api/<string:metric_type>/location')
def get_location_temp_or_humidity(metric_type: str):
    if metric_type == 'temperature':
        return str(current_vals['current_location_temp'])
    elif metric_type == 'humidity':
        return str(current_vals['current_location_humidity'])
    else:
        abort(404)


@app.route('/api/<string:metric_type>/location/<string:timescale>')
def get_location_temp_or_humidity_at_time(metric_type: str, timescale: str):
    result = {}

    if metric_type == 'temperature':
        result = get_data_at_relative_time(MeasurementType.LOCATION_TEMPERATURE, timescale)
    elif metric_type == 'humidity':
        result = get_data_at_relative_time(MeasurementType.LOCATION_HUMIDITY, timescale)
    else:
        abort(404)

    if result == 0.0:
        return '', 204
    return jsonify(result)


@app.route('/api/<string:metric_type>/location/diff')
def get_location_temp_or_humidity_diff(metric_type: str):
    if metric_type == 'temperature':
        return str(
            current_vals['current_temp'] - current_vals['current_location_temp']
        )
    elif metric_type == 'humidity':
        return str(
            current_vals['current_humidity'] - current_vals['current_location_humidity']
        )
    else:
        abort(404)


@app.route('/api/<string:metric_type>/location/diff/<string:timescale>')
def get_location_temp_or_humidity_diff_at_time(metric_type: str, timescale: str):
    result = {}

    if metric_type == 'temperature':
        temp_sensor = get_data_at_relative_time(MeasurementType.SENSOR_TEMPERATURE, timescale)
        temp_location = get_data_at_relative_time(MeasurementType.LOCATION_TEMPERATURE, timescale)
        if temp_sensor == 0.0 or temp_location == 0.0:
            result = 0.0
        else:
            result = {'time': temp_sensor['time'], 'value': temp_sensor['value'] - temp_location['value']}
    elif metric_type == 'humidity':
        humid_sensor = get_data_at_relative_time(MeasurementType.SENSOR_HUMIDITY, timescale)
        humid_location = get_data_at_relative_time(MeasurementType.LOCATION_HUMIDITY, timescale)
        if humid_sensor == 0.0 or humid_location == 0.0:
            result = 0.0
        else:
            result = {'time': humid_sensor['time'], 'value': humid_sensor['value'] - humid_location['value']}
    else:
        abort(404)

    if result == 0.0:
        return '', 204
    return jsonify(result)


@app.route('/api/<string:metric_type>/location/diff/avg/<string:timescale>')
def get_location_temp_or_humidity_diff_avg_at_time(metric_type: str, timescale: str):
    # TODO
    abort(501)


app.run()

# Shut down thread if Ctrl+C
prog_thread.join(1)
