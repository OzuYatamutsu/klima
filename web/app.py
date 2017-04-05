from run import *
from logging import getLogger
from flask import Flask, abort

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
    # TODO
    abort(501)


@app.route('/api/<string:metric_type>/location')
def get_location_temp_or_humidity(metric_type: str):
    if metric_type == 'temperature':
        return str(current_vals['current_location_temp'])
    elif metric_type == 'humidity':
        return str(current_vals['current_location_humidity'])
    else:
        abort(404)


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
    # TODO
    abort(501)


@app.route('/api/<string:metric_type>/location/diff/avg/<string:timescale>')
def get_location_temp_or_humidity_diff_avg_at_time(metric_type: str, timescale: str):
    # TODO
    abort(501)


app.run()

# Shut down thread if Ctrl+C
prog_thread.join(1)
