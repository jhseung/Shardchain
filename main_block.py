import time
import json, random, hashlib
import block_util
import shard_block
from config import NUMBER_OF_SHARDS, EPOCH_LENGTH, ETH_TX_BLOCK
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
				 parent_hash,
				 parent_block = None,
				 shards = {}, #contains key-value mapping of shards
				 shard_length = {}, #respective shard length for shard
				 timestamp = time.time(),
				 difficulty = 0,
				 nonce = 0):

		self.block_no = -1
		self.parent_hash = parent_hash
		self.parent_block = parent_block
		self.shards = shards
		self.shard_length = shard_length
		self.timestamp = timestamp
		self.difficulty = difficulty
		self.nonce = nonce
		self.jsontype = 'main'

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

	"""
	Adds shard to block if it is a valid shard
	:shard: <ShardBlock>
	"""
	def add_shard(self, shard):
		if self._is_valid_shard(shard):
			self.shards[shard.shard_id] = shard

	"""
	Hashes the <dict> containing all head blocks of the shardchains
	:return: <str> hash of shards
	"""
	def hash_contents(self):
		block_string = json.dumps(self.shards, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()

	"""
	Confirms if the header and validity of the block if
	1) hashing the block contents and nonce returns a value lower than difficulty
	2) number of shard headers match NUMBER_OF_SHARDS

	If valid, sets class variable header to be of header and nonce to be of valid nonce
	:nonce: <int> or <str> that satisfies block
	"""
	def confirm_header(self, nonce):
		if self.block_no != -1:
			return
		to_hash = self.hash_contents() + nonce
		hashed = hashlib.sha256(to_hash).hexdigest()
		if int(hashed,16) < int(self.difficulty,16) and \
		   len(self.shards) == NUMBER_OF_SHARDS :
			self.header = hashed
			self.nonce = nonce
			self.block_no = self.parent_block.block_no + 1

	"""
	Confirms if block is a valid block.
	"""
	def is_valid_block(self):
		hashed = hashlib.sha256(self.hash_contents() + self.nonce)
		if int(hashed,16) < int(self.difficulty,16) and \
		   len(self.shards) == NUMBER_OF_SHARDS :
			return True
		return False

	"""
	Retrieves the last n parents from our current block
	"""
	def retrieve_parents(self, n):
		pointer = self.parent_block
		array = []
		for _ in range(n):
			array.append(pointer)
			pointer = pointer.parent_block
		return array

	"""
	Determines the fixed lengths for each shard k by computing the average total transactions per shard over
	the past EPOCH_LENGTHs. 
	"""
	def adjust_shard_length(self):
		shard_transaction_map = {}
		for shard_id in self.shards:
			transactions_per_shard = 0
			parents = self.retrieve_parents(EPOCH_LENGTH)
			for parent_block in parents:
				transactions_per_shard = transactions_per_shard + len(parent_block.shards[shard_id].transactions)
			shard_transaction_map[shard_id] = transactions_per_shard / (EPOCH_LENGTH*ETH_TX_BLOCK)
			self.shard_length[shard_id] = shard_transaction_map[shard_id]
