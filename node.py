import block, block_util, comms, consensus, transaction
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
		self.pending_transactions = []

	def handle_transaction(self, transaction, pending_tran=False):
		if transaction.isInter == False:
			mine(self)
		else:
			if pending_tran == False:
				shard_id_sender = block_util.to_shard(transaction.sender)
				shard_id_receiver = block_util.to_shard(transaction.receiver)
				if self.current_chain == shard_id_sender: #mine this block
					mine(self)
				elif self.current_chain != shard_id_sender and shard_id_sender != shard_id_receiver:
					self.pending_transactions.append(transaction)
			else:
				mine(self)

	def post_pending_transactions(self):
		for transaction in self.pending_transactions:
			handle_transaction(transaction, True)
		self.pending_transactions = []

	def mine(self):
		self.miner = consensus.Miner(self.current_mining_block)
		nonce = self.miner.mine_block()
