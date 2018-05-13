import node
import main_block, shard_block
import transaction
import random
from config import NUMBER_OF_NODES, NUMBER_OF_SHARDS, NUMBER_OF_TRANSACTIONS, TIME_MAINBLOCK, MINING_REWARD

class Master():
    def __init__(self):
        self.num_nodes = NUMBER_OF_NODES
        self.num_shards = NUMBER_OF_SHARDS
        self.num_tx = NUMBER_OF_TRANSACTIONS
        self.time_mainblock = TIME_MAINBLOCK
        self.mining_reward = MINING_REWARD
        self.nodes = []

        GENESIS_BLOCK = main_block.init(None)
        confirm_header(GENESIS_BLOCK.nonce)

        self.genesis_block = GENESIS_BLOCK
        self.blockchain = [self.genesis_block]

    def _instantiate_nodes(self):
        #generate NUMBER_OF_NODES nodes
        for i in range(NUMBER_OF_NODES):
            new_node = node(None, [], 0.5, self.genesis_block, i+8000)
            self.nodes.append(new_node)

        #Assign each node some neighbors
        for i, node in enumerate(self.nodes):
            for x in range(random.randint(3, 6)):
                randint = random.randint(0, NUMBER_OF_NODES)
                while randint == i:
                    randint = random.randint(0, NUMBER_OF_NODES)
                node.neighbors.append(self.nodes[randint])

    def run(self):
        raise NotImplementedError()

    def query_node(self, node):
        return
