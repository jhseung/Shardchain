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
	if block.jsontype == 'shard':
		return json.dumps({shard_id: block.shard_id,
						parent_block_no: block.parent_block_no,
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

	if self.jsontype == 'main':
		return json.dumps({block_no: block.block_no,
						parent_hash: block.parent_hash,
						parent_block: block.parent_block,
						shards: block.shards,
						shard_length: block.shard_length,
						timestamp: block.timestamp,
						difficulty: block.difficulty,
						nonce: block.nonce,
						jsontype: block.jsontype})


def json_to_block(json_input):
	try:
		decoded = json.loads(json_input)
		if (decoded["jsontype"] == 'shard'):
			return ShardBlock(decoded["shard_id"],decoded["parent_block_no"], decoded["parent_hash"],
				decoded["parent_block"],decoded["transactions"],decoded["starting_state"],decoded["timestamp"],
				decoded["difficulty"], decoded["nonce"])
		if (decoded["jsontype"] == 'main'):
			return ShardBlock(decoded["block_no"], decoded["parent_hash"], decoded["parent_block"],
				decoded["shards"],decoded["shard_length"],decoded["timestamp"],
				decoded["difficulty"], decoded["nonce"])

	except (ValueError, KeyError, TypeError):
		print "JSON format error"


"""
Returns appropriate shard for transaction

:param account_id: <account_id>
:return: <str> shard number
"""
def to_shard(account_id):
	return hashlib.sha256(account_id).hexdigest() % NUMBER_OF_SHARDS
