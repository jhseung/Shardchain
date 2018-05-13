import node
import main_block, shard_block
import transaction
import random
from config import NUMBER_OF_NODES, NUMBER_OF_SHARDS, NUMBER_OF_TRANSACTIONS, TIME_MAINBLOCK, MINING_REWARD, NETWORK_HASHRATE

class Master():
    def __init__(self):
        self.num_nodes = NUMBER_OF_NODES
        self.num_shards = NUMBER_OF_SHARDS
        self.num_tx = NUMBER_OF_TRANSACTIONS
        self.time_mainblock = TIME_MAINBLOCK
        self.mining_reward = MINING_REWARD
        self.nodes = []
        self.blockchain = self._instantiate_blockchain()
        self.blocks = {}
        self.network_hashrate = NETWORK_HASHRATE

    def _instantiate_blockchain(self):
        GENESIS_BLOCK = main_block.MainBlock(None)
        confirm_header(GENESIS_BLOCK, GENESIS_BLOCK.nonce)

        for k in range(0, NUMBER_OF_SHARDS):
            GENESIS_SHARD_BLOCK = shard_block.ShardBlock(k, None, None, None)
            GENESIS_SHARD_BLOCK.confirm_header(GENESIS_SHARD_BLOCK, GENESIS_SHARD_BLOCK.nonce)
            GENESIS_BLOCK.shards[k] = GENESIS_SHARD_BLOCK

        GENESIS_BLOCK.adjust_shard_length()
        return GENESIS_BLOCK

    def _instantiate_nodes(self):
        #generate NUMBER_OF_NODES nodes
        for i in range(NUMBER_OF_NODES):
            new_node = node(master_addr=self, [], 0.5, self.genesis_block, i+8000)
            self.nodes.append(new_node)

        #Assign each node some neighbors
        for i, node in enumerate(self.nodes):
            for x in range(random.randint(3, 6)):
                randint = random.randint(0, NUMBER_OF_NODES)
                while randint == i:
                    randint = random.randint(0, NUMBER_OF_NODES)
                node.neighbors.append(self.nodes[randint])

    def update_block(self, block):
        if block.nonce !=0:
            self.blocks[block.header] = block

    def run(self):
        raise NotImplementedError()

    def query_node(self, node):
        return
