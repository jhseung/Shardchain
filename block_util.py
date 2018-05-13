import hashlib
import json
from config import NUMBER_OF_SHARDS
from shard_block import *
from main_block import *

""" Verifies the current block

Checks if:
1) All state transitions are valid
2) Hash value is smaller than the difficulty
3) Block number is nondecreasing wrt parent block

"""
def verify(block):
	raise NotImplementedError()

""" Returns the hash value of the block """
def get_hash(block):
	return block.hash_block()

""" Convert block to json """
def block_to_json(block):
	assert isinstance(block, shard_block.ShardBlock, main_block.MainBlock)
	if block.block_type == 'shard':
		return json.dumps({shard_id: block.shard_id,
						block_no: block.block_no,
						parent_hash: block.parent_hash,
						parent_block: block.parent_block,
						transactions: block.transactions,
						starting_state: block.starting_state,
						resulting_state: block.resulting_state,
						timestamp: block.timestamp,
						difficulty: block.difficulty,
						nonce: block.nonce,
						jsontype: block.jsontype})

	if self.block_type == 'main':
		return json.dumps({block_no: block.block_no,
						parent_hash: block.parent_hash,
						parent_block: block.parent_block,
						shards: block.shards,
						shard_length: block.shard_length,
						timestamp: block.timestamp,
						difficulty: block.difficulty,
						nonce: block.nonce,
						jsontype: block.jsontype})

"""
Returns appropriate shard for transaction

:param transaction: <Transaction> transaction to be assigned a shard
:return: <str> shard number
"""
def to_shard(account_id):
	return hashlib.sha256(account_id).hexdigest() % NUMBER_OF_SHARDS
