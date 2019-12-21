from view import view_blueprint
from controller import graph_controller_blueprint, debug_controller_blueprint
from gegeelisa import gegeelisa
from helper import *
from env import env

gegeelisa.register_blueprint(view_blueprint)
gegeelisa.register_blueprint(graph_controller_blueprint)

if env['DEBUG_MODE']: gegeelisa.register_blueprint(debug_controller_blueprint)

if __name__ == '__main__':
    gegeelisa.run(host='0.0.0.0', port=1234)
