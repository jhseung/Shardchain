import random, hashlib, threading

class Miner(threading.Thread):
    def __init__(self, cur_node):
        self.cur_node = cur_node
        self.found_event = threading.Event()
        return found_event

	def run(self):
        cur_nonce = random.randint(0, 1000000)
        while not found_event.is_set():
            bl, cur_nonce = mine(block, cur_nonce, rounds)
                if bl is not None:
                    return final_nonce
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
