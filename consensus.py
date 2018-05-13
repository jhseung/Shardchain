import random, hashlib

class Miner():
    def __init__(self, block):
        self.block = block
        self.nonce = random.randint(0,100000000)

	def mine_block(self, rounds=1000, start_nonce=0):
		bl, a_nonce = mine(block, start_nonce, rounds)
        if bl is not None:
            return a_nonce
        return None

def validate_pow(block, nonce):
    hashed = block.hash_contents() + nonce
    if int(hashed,16) < int(block.difficulty,16):
        return True
    else:
        return False

def mine(block, nonce, difficulty, rounds=1000):
    assert isinstance(nonce, int)
    for i in range(rounds):
        if validate_pow(block, nonce):
            return block, nonce
        nonce += i
    return None, nonce
