from flask import Blueprint, jsonify
from model import *
from helper import *
from service import WikipediaScrapeService, WikipediaGraphService

debug_controller_blueprint = Blueprint('debug_controller', 'debug_controller_blue', url_prefix='/_internal/debug/')

@debug_controller_blueprint.route('/ok', methods=['GET', 'POST'])
def give_ok():
    return 'OK\n'

@debug_controller_blueprint.route('/build/<page_id>', methods=['GET'])
def build(page_id):
    try:
        w1 = WikipediaGraphService.expand_node_by_string_id(page_id)
        return 'OK\n'
    except GegeException as e:
        return jsonify(e.serialize())


@debug_controller_blueprint.route('/get/<page_id>', methods=['GET'])
def get(page_id):
    try:
        result = WikipediaGraphService.retrieve_node(page_id)
        return jsonify(result.serialize())
    except GegeException as e:
        return jsonify(e.serialize())
