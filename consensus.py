import random, hashlib, threading
from queue import Queue

class Miner(threading.Thread):
    def __init__(self, cur_node):
        self.cur_node = cur_node
        self.found_event = threading.Event()
        self.found_blocks = Queue()

    def get_found_event(self):
        return self.found_event

	def run(self):
        cur_nonce = random.randint(0, 1000000)
        while not found_event.is_set():
            cur_block = self.cur_node.current_mining_block
            bl, cur_nonce = mine(block, cur_nonce, rounds)
                if bl is not None:
                    self.found_blocks.put((cur_block, cur_nonce))
                    self.found_event.set()

def validate_pow(block, nonce):
    hashed = block.hash_contents() + nonce
    if int(hashed, 16) < int(block.difficulty, 16):
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
