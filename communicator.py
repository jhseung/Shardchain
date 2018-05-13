import socket, select
from block_util import *
from transaction_util import *

class Communicator:
	def __init__(self, sock):
		self.sock = sock

	def listen(self):


	""" Broadcast transaction signed with key """
	def broadcast_tx(self, neighbor_list, tx):
		for addr in neighbor_list:
			sock.send(tx_to_json(tx), addr)

	""" Broadcast mined block (faulty or not) """
	def broadcast_block(self, neighbor_list, block):
	    for addr in neighbor_list:
	    	sock.send(block_to_json(block), addr)

	""" Request block block_no """
	def request_block(self, req_target, block_no):
	    raise NotImplementedError()

	""" Request chain head """
	def request_most_recent_block(self, req_target):
		raise NotImplementedError()