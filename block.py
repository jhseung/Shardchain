import time

class Block:
	def __init__(self, 
				 block_no, 
				 parent_block_no, 
				 parent_hash,
				 parent_block = None,
				 transactions = [],
				 starting_state = {},
				 resulting_state = {}, 
				 timestamp = time.time(),
				 difficulty = 0,
				 nonce = 0):

		self.block_no = block_no
		self.parent_block_no = parent_block_no
		self.parent_hash = parent_hash
		self.parent_block = parent_block
		self.transactions = transactions
		self.starting_state = starting_state
		self.resulting_state = resulting_state
		self.timestamp = timestamp
		self.difficulty = difficulty
		self.nonce = nonce

