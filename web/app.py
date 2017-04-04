from threading import Thread
from run import *
from logging import getLogger
from flask import Flask, abort

logger = getLogger(__name__)
app = Flask(__name__)

# Initialize thread
main_thread = Thread(target=main)
main_thread.daemon = True
main_thread.start()

@app.route('/')
def hello_world():
    return 'TODO'


@app.route('/api/<string:metric_type>')
def get_current_temp_or_humidity(metric_type: str):
    if metric_type == 'temperature':
        return str(current_temp)
    elif metric_type == 'humidity':
        return str(current_humidity)
    else:
        abort(404)


@app.route('/api/<string:metric_type>/<string:timescale>')
def get_temp_or_humidity_at_time(metric_type: str, timescale: str):
    # TODO
    abort(501)


@app.route('/api/<string:metric_type>/location')
def get_location_temp_or_humidity(metric_type: str):
    if metric_type == 'temperature':
        return str(current_location_temp)
    elif metric_type == 'humidity':
        return str(current_location_humidity)
    else:
        abort(404)


@app.route('/api/<string:metric_type>/location/diff')
def get_location_temp_or_humidity_diff(metric_type: str):
    # TODO
    abort(501)


@app.route('/api/<string:metric_type>/location/diff/<string:timescale>')
def get_location_temp_or_humidity_diff_at_time(metric_type: str, timescale: str):
    # TODO
    abort(501)


@app.route('/api/<string:metric_type>/location/diff/avg/<string:timescale>')
def get_location_temp_or_humidity_diff_avg_at_time(metric_type: str, timescale: str):
    # TODO
    abort(501)


app.run()

# Blocks execution - if we get here, we probably got a Ctrl+C
# TODO: BELOW DOES NOTHING, WE NEED TO SEND THREAD A SIGNAL
logger.info("KeyboardInterrupt - Closing streams and shutting down.")
if temp_sensor is not None:
    logger.debug('Closing temp sensor.')
    temp_sensor.close()
if humid_sensor is not None:
    logger.debug('Closing humid sensor.')
    humid_sensor.close()
