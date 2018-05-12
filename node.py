import block, block_util, comms


""" Represents a node in the network

All nodes are full nodes; i.e. all nodes retain the full BC and the resulting states after each block
"""
class Node:
	def __init__(self, 
		         master_addr
		         neighbors = [],
		         private_key = None,
		         public_key = None,
		         passphrase = None,
		         activity_level = 0.5,
		         port_no):

		self.master_addr = master_addr
		self.neighbors = neighbors
		self.transactions_to_add = None
		self.current_chain = None
		self.current_mining_block = None
		self.private_key = private_key
		self.public_key = public_key
		self.activity_level = activity_level
		self.socket = socket.socket()
		self.socket.connect((socket.gethostname(), port_no))

		return public_key, socket

	def run(self):
		while True:
			
