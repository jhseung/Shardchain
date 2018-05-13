import block, block_util, comms, consensus
import hashlib

""" Represents a node in the network

All nodes are full nodes; i.e. all nodes retain the full BC and the resulting states after each block
"""
class Node:
	"""
	:master_addr: ?
	:neighbors: <list> of <Node>
	:current_chain: <str> id of current shard
	:current_mining_block: <ShardBlock> longest canonical chain
	:activity_level:
	"""
	def __init__(self, 
		         master_addr,
		         neighbors = [],
		         activity_level = 0.5,
		         port_no):
		self.master_addr = master_addr
		self.neighbors = neighbors
		self.current_chain = None
		self.current_mining_block = None
		self.activity_level = activity_level
		self.socket = socket.socket()
		self.socket.connect((socket.gethostname(), port_no))

	def mine(self):
		self.miner = consensus.Miner(self.current_mining_block)
		nonce = self.miner.mine_block()

	def run(self):
		while True:
			raise NotImplementedError()

	def broadcast_tx(self, transaction):
		for n in self.neighbors:
			#TODO: broadcast transaction to neighbors
			pass

	def receive_tx(self, transaction):
		#self.broadcast_tx(transaction)
		if block_util.to_shard(transaction) == self.current_chain:
			self.current_mining_block.add_transaction(transaction)
			self.current_mining_block.mine_block() #Make multi-threaded
		