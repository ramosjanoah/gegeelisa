from flask import Blueprint, jsonify, request
from service import WikipediaGraphService
from helper import *

graph_controller_blueprint = Blueprint('graph_controller', 'graph_controller_blueprint', url_prefix='/graph/')

@graph_controller_blueprint.route('/nodes/<string_id>', methods=['POST'])
def build_node(string_id):
    try:
        serializer = WikipediaGraphService.init_and_expand_node(string_id)
        return jsonify(serializer.serialize(StatusCodeCreated)), StatusCodeCreated
    except GegeException as e:
        return jsonify(e.serialize()), e.http_code

@graph_controller_blueprint.route('/nodes/<string_id>', methods=['GET'])
def retrieve_node(string_id):
    try:
        serializer = WikipediaGraphService.retrieve_node_by_string_id(string_id)
        return jsonify(serializer.serialize()), StatusCodeOK
    except GegeException as e:
        return jsonify(e.serialize()), e.http_code


@graph_controller_blueprint.route('/nodes/<string_id>', methods=['PATCH'])
def expand_node(string_id):
    try:
        serializer = WikipediaGraphService.expand_node_by_string_id(string_id)
        return jsonify(serializer.serialize()), StatusCodeOK
    except GegeException as e:
        return jsonify(e.serialize()), e.http_code

@graph_controller_blueprint.route('/nodes/<string_id>/adjacents', methods=['GET'])
def retrieve_adjacent_nodes(string_id):
	try:
		offset = int(request.args.get('offset') or 0)
		limit = int(request.args.get('limit') or 3)
	except:
		e = InvalidParameter('offset or limit')
		return jsonify(e.serialize()), e.http_code

	try:
		serializer = WikipediaGraphService.retrieve_adjacent_nodes_by_string_id(string_id, offset, limit)
		return jsonify(serializer.serialize()), StatusCodeOK
	except GegeException as e:
		return jsonify(e.serialize()), e.http_code


@graph_controller_blueprint.route('/first-node', methods=['GET'])
def get_first_node():
	try:
		serializer = WikipediaGraphService.retrieve_node_by_string_id("fibonacci_number")
		return jsonify(serializer.serialize()), StatusCodeOK
	except GegeException as e:
		return jsonify(e.serialize()), e.http_code


@graph_controller_blueprint.route('/first-node', methods=['POST'])
def build_first_node():
	try:
		serializer = WikipediaGraphService.init_and_expand_node('fibonacci_number')
		return jsonify(serializer.serialize()), StatusCodeCreated
	except GegeException as e:
		return jsonify(e.serialize()), e.http_code

