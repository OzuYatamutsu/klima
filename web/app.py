from threading import Thread
from run import main
from flask import Flask
app = Flask(__name__)

# Initialize thread
main_thread = Thread(target=main)
main_thread.start()


@app.route('/')
def hello_world():
    return 'Hello, World!'


app.run()
