<<<<<<< HEAD
import block, block_util, comms, consensus, communicator
=======
import block, block_util, comms, consensus, transaction
>>>>>>> a852a3989433b30f1e78ad50061e22905a36639d
import hashlib
from collections import defaultdict
import json

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

		self.seen_hashes = defaultdict(int)       # Hash values encountered from the flooding network
		self.communicator = communicator.Communicator(("localhost", port_no))
		self.pending_transactions = []

	def handle_transaction(self, transaction, pending_tran=False):
		if transaction.is_intershard == False:
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

	def run(self):
		while True:

			# Listen for incoming data
			received_data = self.communicator.listen()

			# Process received information
			for (data, addr) in received_data:
				data_in_dict = json.loads(data.decode("utf-8"))

				# Already seen this data before; ignore
				if hash_json(data) in self.seen_hashes:
					continue
				else: 

				# Relay to all my neighbors
				self.communicator.broadcast_json(self.neighbors, data_in_dict, exclude = [addr])

				# Process depending on data type
				data_type = in_json["type"]
				process_incoming_data(data_type, data_in_dict)
					
			

			raise NotImplementedError()

	def process_incoming_data(self, data_type, data_in_dict):

		if data_type == "tx":
			""" TODO
			If tx is in my current_shard,
				1) verify it (i.e. state transition is valid)
				2) store it somewhere
			"""
			pass

		elif data_type == "shard_block":
			""" TODO


			"""
			pass

		elif data_type == "main_block":
			pass

		else:
			pass	

def hash_json(data_in_bytes):
	return hashlib.sha256(data_in_bytes.encode('utf-8')).hexdigest()
