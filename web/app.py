from run import *
from config import influx_settings, location_settings
from measurement_type import MeasurementType
from influx.influx_adapter import get_data_at_relative_time
from logging import getLogger
from flask import Flask, abort, jsonify, render_template

logger = getLogger(__name__)
app = Flask(__name__)

# Initialize thread
current_vals = {}
prog_thread: Thread = MainThread(current_vals)
prog_thread.start()


@app.route('/')
def hello_world():
    current_temp = str(current_vals['current_temp'])
    current_humidity = str(current_vals['current_humidity'])
    location_temp = str(current_vals['current_location_temp'])
    location_humidity = str(current_vals['current_location_humidity'])

    return render_template('index.html',
                           current_temp=current_temp, current_humidity=current_humidity,
                           location_temp=location_temp, location_humidity=location_humidity
    )


@app.route('/api/<string:sensor_type>')
def get_current_temp_or_humidity(sensor_type: str):
    if sensor_type == 'temperature':
        return str(current_vals['current_temp'])
    elif sensor_type == 'humidity':
        return str(current_vals['current_humidity'])
    else:
        abort(404)


@app.route('/api/<string:sensor_type>/<string:timescale>')
def get_temp_or_humidity_at_time(sensor_type: str, timescale: str):
    result = {}

    if not influx_settings['enabled']:
        return '', 204
    if sensor_type == 'temperature':
        result = get_data_at_relative_time(MeasurementType.SENSOR_TEMPERATURE, timescale)
    elif sensor_type == 'humidity':
        result = get_data_at_relative_time(MeasurementType.SENSOR_HUMIDITY, timescale)
    else:
        abort(404)

    if result == 0.0:
        return '', 204
    return jsonify(result)


@app.route('/api/<string:sensor_type>/location')
def get_location_temp_or_humidity(sensor_type: str):
    if not location_settings['enabled']:
        return '', 204
    if sensor_type == 'temperature':
        return str(current_vals['current_location_temp'])
    elif sensor_type == 'humidity':
        return str(current_vals['current_location_humidity'])
    else:
        abort(404)


@app.route('/api/<string:sensor_type>/location/<string:timescale>')
def get_location_temp_or_humidity_at_time(sensor_type: str, timescale: str):
    result = {}

    if not location_settings['enabled'] or not influx_settings['enabled']:
        return '', 204
    if sensor_type == 'temperature':
        result = get_data_at_relative_time(MeasurementType.LOCATION_TEMPERATURE, timescale)
    elif sensor_type == 'humidity':
        result = get_data_at_relative_time(MeasurementType.LOCATION_HUMIDITY, timescale)
    else:
        abort(404)

    if result == 0.0:
        return '', 204
    return jsonify(result)


@app.route('/api/<string:sensor_type>/location/diff')
def get_location_temp_or_humidity_diff(sensor_type: str):
    if not location_settings['enabled']:
        return '', 204
    if sensor_type == 'temperature':
        return str(
            current_vals['current_temp'] - current_vals['current_location_temp']
        )
    elif sensor_type == 'humidity':
        return str(
            current_vals['current_humidity'] - current_vals['current_location_humidity']
        )
    else:
        abort(404)


@app.route('/api/<string:sensor_type>/location/diff/<string:timescale>')
def get_location_temp_or_humidity_diff_at_time(sensor_type: str, timescale: str):
    result = {}

    if not location_settings['enabled'] or not influx_settings['enabled']:
        return '', 204
    if sensor_type == 'temperature':
        temp_sensor = get_data_at_relative_time(MeasurementType.SENSOR_TEMPERATURE, timescale)
        temp_location = get_data_at_relative_time(MeasurementType.LOCATION_TEMPERATURE, timescale)
        if temp_sensor == 0.0 or temp_location == 0.0:
            result = 0.0
        else:
            result = {'time': temp_sensor['time'], 'value': temp_sensor['value'] - temp_location['value']}
    elif sensor_type == 'humidity':
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


@app.route('/api/<string:sensor_type>/location/diff/avg/<string:timescale>')
def get_location_temp_or_humidity_diff_avg_at_time(sensor_type: str, timescale: str):
    result = {}

    if not location_settings['enabled'] or not influx_settings['enabled']:
        return '', 204
    if sensor_type == 'temperature':
        temp_sensor_avg = get_data_at_relative_time(MeasurementType.SENSOR_TEMPERATURE, timescale, True)
        temp_location_avg = get_data_at_relative_time(MeasurementType.LOCATION_TEMPERATURE, timescale, True)
        if temp_sensor_avg == 0.0 or temp_location_avg == 0.0:
            result = 0.0
        else:
            result = {'time': temp_sensor_avg['time'], 'value': temp_sensor_avg['value'] - temp_location_avg['value']}
    elif sensor_type == 'humidity':
        humid_sensor_avg = get_data_at_relative_time(MeasurementType.SENSOR_HUMIDITY, timescale, True)
        humid_location_avg = get_data_at_relative_time(MeasurementType.LOCATION_HUMIDITY, timescale, True)
        if humid_sensor_avg == 0.0 or humid_location_avg == 0.0:
            result = 0.0
        else:
            result = {'time': humid_sensor_avg['time'], 'value': humid_sensor_avg['value'] - humid_location_avg['value']}
    else:
        abort(404)

    if result == 0.0:
        return '', 204
    return jsonify(result)


app.run()

# Shut down thread if Ctrl+C
prog_thread.join(1)
