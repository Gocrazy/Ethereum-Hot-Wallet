# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, request
from contextlib import contextmanager
from requests.exceptions import ConnectionError, ConnectTimeout
from web3 import Web3, HTTPProvider
import json
import requests
import logging
from helpers import convert_filter_keys

app = Flask(__name__)
app.config['geth_url'] =  'http://127.0.0.1:8545'

def logging(message):
	print("log: %s" % message)


@contextmanager
def context_handler(*exceptions):
  try:
    yield
  except ValueError as valueError:
  	logging(type(valueError))
  	abort(400, {'message': 'parameter hash value is invalid.'});
  except ConnectTimeout as connectionTimeout:
  	logging("ConnectionTimeout %s" % app.config['geth_url'])
  	abort(500, {'message': 'Internal Server Error'});
  except ConnectionError as connectionError:
  	logging("ConnectionError %s" % app.config['geth_url'])
  	abort(500, {'message': 'Internal Server Error'});
  else:
  	pass


@app.route("/admin.nodeinfo", methods=["GET"])
def admin_nodeinfo():
	w3 = Web3(HTTPProvider(app.config['geth_url']))
	return jsonify({'message': 'ok', 'result': convert_filter_keys(w3.admin.nodeInfo, ['enode', 'name'])})


@app.route("/block")
def block():
	# set up connection of geth client.
	w3 = Web3(HTTPProvider(app.config['geth_url']))
	with context_handler(Exception):
		# query: getBlock by block number.
		# get block number parameter from GET request.
		block_number = int(request.args.get('number', -1))
		block = w3.eth.getBlock(block_number)
		# Null Traction object.
		if block is None:
			abort(404, {'message': 'Block number %i not found' % block_number})

	return jsonify({'message': 'ok', 'result': convert_filter_keys(block, ['difficulty', 'gasLimit', 'gasUsed', 'hash', 'miner', 'parentHash', 'totalDifficulty'])})

@app.route("/transaction", methods=['GET'])
def transaction():
	w3 = Web3(HTTPProvider(app.config['geth_url']))
	with context_handler(Exception):
		hash = str(request.args.get('hash', ''))
		trasaction = w3.eth.getTransaction(hash)
		if trasaction is None:
			abort(404, {'message': 'Transaction hash %s not found' % hash})
	
	return jsonify({'message': 'ok', 'result': convert_filter_keys(trasaction, ['blockHash', 'blockNumber', 'from', 'gas', 'gasPrice', 'hash', 'nonce', 'to', 'value'])})

@app.route("/miner", methods=["PUT", "DELETE"])
def miner():
	w3 = Web3(HTTPProvider(app.config['geth_url']))
	if request.method == "PUT":
		numberOfThread = 4
		w3.miner.start(numberOfThread)
		return jsonify({'message': 'miner start'})
	elif request.method == "DELETE":
		w3.miner.stop()
		return jsonify({'message': 'miner stop'})

	return jsonify({'message': 'not thnig'})

@app.errorhandler(400)
def custom400(error):
	return jsonify({'error': {'message': error.description['message']}}), 400

@app.errorhandler(404)
def custom404(error):
	print('404 handler')
	return jsonify({'error': {'message': error.description['message']}, 'result': None}), 404

@app.errorhandler(500)
def internal_error(error):
	return jsonify({'error': {'message': error.description['message']}}), 500

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5678)