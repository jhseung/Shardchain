import node
import main_block, shard_block
import transaction
from config import NUMBER_OF_NODES, NUMBER_OF_SHARDS, NUMBER_OF_TRANSACTIONS, TIME_MAINBLOCK, MINING_REWARD

class Master():
    def __init__(self):
        self.num_nodes = NUMBER_OF_NODES
        self.num_shards = NUMBER_OF_SHARDS
        self.num_tx = NUMBER_OF_TRANSACTIONS
        self.time_mainblock = TIME_MAINBLOCK
        self.mining_reward = MINING_REWARD
    
    def _instantiate_nodes(self):
        raise NotImplementedError()
    
    def run(self):
        raise NotImplementedError()

    def query_node(self, node):
        return 