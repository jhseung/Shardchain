import block, block_util, comms, consensus, communicator
import transaction ,transaction_util
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
				 mainblock = None,
		         port_no):
		self.master_addr = master_addr
		self.neighbors = neighbors
		self.current_chain = None
		self.current_mining_block = None
		self.mainblock = mainblock
		self.activity_level = activity_level

		self.seen_hashes = defaultdict(int)       # Hash values encountered from the flooding network
		self.communicator = communicator.Communicator(("localhost", port_no))
		self.pending_transactions = []

		self.transactions_to_issue = []
		self.transaction_issue_freq = 1
		self.hash_rate = 100

	# def mine(self):
	# 	self.miner = consensus.Miner(self.current_mining_block)
	# 	nonce = self.miner.mine_block()
	# 	if nonce is not None:
	# 		self.current_mining_block.confirm_header(nonce)
	# 		#Propagate block
	# 		return
	# 	else:
	# 		#Handle unsuccessful mining attempt
	# 		return

	# def handle_transaction(self, transaction, pending_tran=False):
	# 	if transaction.is_intershard == False:
	# 		mine(self)
	# 	else:
	# 		if pending_tran == False:
	# 			shard_id_sender = block_util.to_shard(transaction.sender)
	# 			shard_id_receiver = block_util.to_shard(transaction.receiver)
	# 			if self.current_chain == shard_id_sender: #mine this block
	# 				mine(self)
	# 			elif self.current_chain != shard_id_sender and shard_id_sender != shard_id_receiver:
	# 				self.pending_transactions.append(transaction)
	# 		else:
	# 			mine(self)

	def post_pending_transactions(self):
		for transaction in self.pending_transactions:
			handle_transaction(transaction, True)
		self.pending_transactions = []

	def run(self):

		# Start issuing transactions
		tx_issuer = threading.Thread(target = issue_transactions,
									 args = (self.communicator, self.transactions_to_issue, self.neighbors, self.transaction_issue_freq))
		tx_issuer.start()

		while True:
			# Start mining
			miner = 
			miner.start
			# Listen for incoming data
			received_data = self.communicator.listen()

			# Process received information
			for (data, addr) in received_data:
				data_in_dict = json.loads(data.decode("utf-8"))

				# Already seen this data before; ignore
				if hash_json(data) in self.seen_hashes:
					continue
				else:
				#Propagate

				# Relay to all my neighbors
				self.communicator.broadcast_json(self.neighbors, data_in_dict, exclude = [addr])

				# Process depending on data type

				data_type = data_in_dict["jsontype"]

				process_incoming_data(data_type, data_in_dict)



			raise NotImplementedError()

	"""Determine if shard has filled up to q_k since the last mainblock was mined"""
	def did_fill_q_k(self, shardblock, mainblock):
		prev_block_no = mainblock.parent_block.shards[shardblock.shard_id].block_no
		return shardblock.block_no - prev_block_no == mainblock.shard_length[shardblock.shard_id]


	"""Return shard id of any shard that is not filled up yet"""
	def open_shards(self, mainblock):
		for shard_id in mainblock.shards:
			if not self.did_fill_q_k(mainblock.shards[shard_id], mainblock):
				return shard_id
		return -1

	def process_incoming_data(self, data_type, data_in_dict):
		#If the data type is a transaction
		if data_type == "tx":
			#Convert data to a transaction object
			tx = transaction_util.json_to_tx(data_in_dict)

			#If the sender is in the shard that the node is currently mining on, then add the transaction into the block
			if block_util.to_shard(tx.sender) == self.current_chain:
				self.current_mining_block.add_transaction(tx)

		#If the data type is a shard block
		elif data_type == "shard_block":
			#Convert data to shardblock object
			block = block_util.json_to_block(data_in_dict)

			# If the block's shard is same as the shard we are mining on
			# And if POW was good
			# And if the block we received is a later block than our current block
			if self.current_chain == block.shard_id and consensus.validate_pow(block) and self.current_mining_block.block_no < block.block_no:
				# If our shard did not fill up then just mine on this block on this shard
				if not self.did_fill_q_k(block, self.mainblock):
					self.current_mining_block = block
				# If the shard is full
				else:
					# Get a new shard id (-1 is if ALL shards are full)
					new_shard_id = open_shards(self.mainblock)
					if not new_shard_id == -1:
						self.current_chain = new_shard_id
					# If all shards are full then just mine the main block
					else:
						self.current_mining_block = self.mainblock
		#If data type is a main block
		elif data_type == "main_block":
			block = block_util.json_to_block(data_in_dict)
			#If block's POW was good and block we received is a later block than our current block
			if consensus.validate_pow(block) and self.mainblock.block_no < block.block_no:
				#Update mainblock
				self.mainblock = block
			#handle stuff?



def issue_transactions(communicator, tx_list, neighbors, freq):
	for tx in tx_list:
		time.sleep(freq)
		communicator.broadcast_tx(neighbors, tx)


def hash_json(data_in_bytes):
	return hashlib.sha256(data_in_bytes.encode('utf-8')).hexdigest()
