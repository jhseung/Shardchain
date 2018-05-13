import time
import json, random, hashlib
import block_util
import shard_block
from config import NUMBER_OF_SHARDS

class MainBlock:
	"""
	:block_no: <str> current block number
	:parent_hash: <str> header of previous block
	:parent_block: <MainBlock> pointer to previous block
	:shards: <dict> key-value mapping of shards
		key - shard ID using to_shard function
		value - pointer to latest block in particular shard
	:q_sub_k: <dict> key-value mapping of shard to length cap
		key - shard ID using to_shard function
		value - int representing min length cap of shard
	:timestamp: <float> timestamp of when block was instantiated
	:difficulty: ???
	:nonce: ???
	"""
	def __init__(self,
				 block_no,
				 parent_hash,
				 parent_block = None,
				 shards = {}, #contains key-value mapping of shards
				 shard_length = {}, #respective shard length for shard
				 timestamp = time.time(),
				 difficulty = 0,
				 nonce = 0):

		self.block_no = block_no
		self.parent_hash = parent_hash
		self.parent_block = parent_block
		self.shards = shards
		self.shard_length = shard_length
		self.timestamp = timestamp
		self.difficulty = difficulty
		self.nonce = nonce
		self.block_type = 'main'

	def retrieve_shard(self, sender=None, k=None):
		if k is not None:
			return self.shards[k]
		if sender is not None:
			for shard in self.shards:
				for addr in shard:
					if addr == sender:
						return shard
		return None

	def _is_valid_shard(self, shard):
		latest_shard_block = self.shards[shard.shard_id]
		prev_mined_block = self.parent_block.shards[shard.shard_id]
		min_length = self.shard_length[shard.shard_id]
		for _ in range(min_length):
			latest_shard_block = latest_shard_block.parent_block
		if latest_shard_block == prev_mined_block:
			return True
		else:
			return False

	def add_shard(self, shard):
		if not self._is_valid_shard(shard):
			return
		else:
			self.shards[shard.shard_id] = shard
			return

	def hash_block(self):
		block_string = json.dumps(self.shards, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	def proof_of_work(self):
		added_nonce = self.hash_block() + self.timestamp + self.nonce
		return hashlib.sha256(added_nonce).hexdigest()

	def mine_block(self):
		while True:
			if len(self.shards) != NUMBER_OF_SHARDS:
				time.sleep(0.1)
			else:
				self.nonce = self.nonce + random.uniform(0,1)
				hashed = self.proof_of_work()
				if hashed[:self.difficulty] == "0" * self.difficulty:
					return

	def retrieve_parents(self, n):
		pointer = self.parent_block
		for x in range(n):
			array.append(pointer)
			pointer = pointer.parent_block
		return array

	def adjust_shard_length(self):
		N = 10 #some random constant
		Eth_Transactions_Per_Block = 138
		shard_transaction_map = {}
		for shard_id in self.shards:
			transactions_per_shard = 0
			parents = self.retrieve_parents(N)
			for parent_block in parents:
				transactions_per_shard = transactions_per_shard + len(parent_block.shards[shard_id].transactions)
			shard_transaction_map[shard_id] = transactions_per_shard / (N*Eth_Transactions_Per_Block)
			self.shard_length[shard_id] = shard_transaction_map[shard_id]
