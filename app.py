import argparse
import gunicorn.app.base
import os
import threading
import time

from flask import Flask, request
from multiprocessing import Array, Manager, Value
from signal import SIGHUP


app = Flask(__name__)


@app.route('/variable', methods=['GET'])
def get_variable():
    global data 
    worker_pid = os.getpid()
    variable_name = request.args.get('var', default=None, type=str)
    if variable_name in data:
        variable_value = data[variable_name]
        if variable_name == 'multiprocess_array':
            variable_value = ','.join([str(x) for x in variable_value])
        return_str = f'{worker_pid} | {variable_value}'
        return return_str, 200
    else:
        return '', 404
    

@app.route('/variable', methods=['PUT'])
def update_variable():
    global data
    json_request = request.json
    for k, v in json_request.items():
        if k == 'global_data':
            data[k] = v
        elif k == 'multiprocess_value':
            with data[k].get_lock():
                data[k].value = float(v)
        elif k == 'multiprocess_array':
            data[k][0] = int(v)
        elif k == 'multiprocess_manager':
            data[k]['manager_key'] = v
        else:
            return '', 404
        return str(data[k]), 200


def __worker_thread():
    global data
    print('Starting background thread')
    while True:
        time.sleep(5)
        with open('additional_config.txt', 'r') as f:
            data['sighup_data'] = f.read()
        os.kill(data['master_pid'], SIGHUP)


# App Initialization
def initialize():
    global data 
    data = {}
    data['master_pid'] = os.getpid()
    data['global_data'] = "This is global data"
    data['multiprocess_value'] = Value('d', 0.0)
    data['multiprocess_array'] = Array('i', range(5))
    manager_dict = Manager().dict()
    manager_dict['manager_key'] = 'manager_value'
    data['multiprocess_manager'] = manager_dict
    with open('additional_config.txt', 'r') as f:
        data['sighup_data'] = f.read()

    # For the background thread
    t = threading.Thread(target=__worker_thread)
    t.daemon = True
    t.start()
    data['background_thread'] = t


# Custom Gunicorn application: https://docs.gunicorn.org/en/stable/custom.html
class HttpServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    global data
    parser = argparse.ArgumentParser()    
    parser.add_argument('--num-workers', type=int, default=5)
    parser.add_argument('--port', type=str, default='8080')
    args = parser.parse_args()
    options = {
        'bind': '%s:%s' % ('0.0.0.0', args.port),
        'workers': args.num_workers,
    }
    initialize()
    HttpServer(app, options).run()