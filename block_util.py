import block

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
	raise NotImplementedError()

""" Convert block to json """
def to_json(block):
	raise NotImplementedError()
