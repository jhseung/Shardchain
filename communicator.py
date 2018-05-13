import socket, select
from block_util import *
from transaction_util import *

class Communicator:
	def __init__(self, node_host, node_port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((node_host, node_pott))
		sock.setblocking(0)
		self.sock = sock

	def listen(self):
		readable, _, _ = select.select([self.sock], [], [])
		return [s.recvfrom(2048) for s in readable]

	""" Broadcast transaction signed with key """
	def broadcast_tx(self, neighbor_list, tx, exclude = []):
		for addr in neighbor_list:
			if addr not in exclude:
				sock.send(tx_to_json(tx), addr)

	""" Broadcast mined block (faulty or not) """
	def broadcast_block(self, neighbor_list, block, exclude = []):
	    for addr in neighbor_list:
			if addr not in exclude:
	    		sock.send(block_to_json(block), addr)

	def broadcast_json(self, neighbor_list, json_str, exclude = []):
		for addr in neighbor_list:
			if addr not in exclude:
	    		sock.send(json_str, addr)

	""" Request block block_no """
	def request_block(self, req_target, block_no):
	    raise NotImplementedError()

	""" Request chain head """
	def request_most_recent_block(self, req_target):
		raise NotImplementedError()