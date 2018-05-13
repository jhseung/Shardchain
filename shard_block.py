import time, hashlib
import copy
from config import ETH_TX_BLOCK

class ShardBlock:
    """
    :shard_id: id of the shard chain it is on
	:block_no: <str> current block number
	:parent_hash: <str> header of previous block
	:parent_block: <MainBlock> pointer to previous block
	:transactions: <list> list of <Transaction> objects
    :starting_state: <dict> key(account id)-value(amount) dictionary
        at the beginning of the block, without the transactions
    :resulting_state: <dict> key(account id)-value(amount) dictionary
        that updates upon each issued transaction
	:timestamp: <float> timestamp of when block was instantiated
	:difficulty: ???
	:nonce: ???
	"""
    def __init__(self,
                 shard_id,
				 parent_block_no,
				 parent_hash,
				 parent_block = None,
				 transactions = [],
				 starting_state = {},
				 timestamp = time.time(),
				 difficulty = 0,
				 nonce = 0):
        self.shard_id = shard_id
        self.parent_block_no = parent_block_no
        self.block_no = -1
        self.parent_hash = parent_hash
        self.parent_block = parent_block
        self.transactions = transactions
        self.starting_state = starting_state
        self.resulting_state = copy.deepcopy(starting_state) #copying dic to maintain starting_state for now
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        self.jsontype = 'shard'

    """
    Verifies if a transaction is valid
    A transaction is invalid if:
    1. Sender's address is not already inside of the block's account balance dict
    2. Amount in sender's account is less than the transaction amount
    3. Transaction's amount is less than 0.

    :param transaction: <Transaction> transaction
    :return: <bool>
    """
    def _is_transaction_valid(self, transaction):
        if transaction.sender not in self.starting_state:
            return False
        if self.starting_state[transaction.sender] < transaction.amount:
            return False
        if transaction.amount < 0:
            return False
        if len(self.transactions) > ETH_TX_BLOCK:
            return False
        return True

    """
    Adds transaction to block's list of transactions
    If transaction is invalid, does not add. (perhaps raise exception later?)

    :param transaction: <Transaction> transaction being added
    :return: None
    """
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        if not self._is_transaction_valid(transaction):
            print "INVALID TRANSACTION"
            return
        self.starting_state[transaction.sender] -= transaction.amount
        if transaction.recipient not in self.starting_state and not transaction.is_intershard:
            self.resulting_state[transaction.recipient] = transaction.amount
        elif transaction.recipient in self.starting_state and not transaction.is_intershard:
            self.resulting_state[transaction.recipient] = self.resulting_state[transaction.recipient] +\
            transaction.amount

    """
	Hashes the <dict> containing all head blocks of the shardchains
	:return: <str> hash of shards
	"""
    def hash_contents(self):
        txs = list(map(lambda x : x.sender + x.recipient + str(x.amount), self.transactions))
        header = self.parent_hash + txs + self.timestamp
        return hashlib.sha256(header).hexdigest()

    """
    Confirms if the header and validity of the block if
	1) hashing the block contents and nonce returns a value lower than difficulty
	2) number of shard headers match NUMBER_OF_SHARDS

	If valid, sets class variable header to be of header and nonce to be of valid nonce
	:nonce: <int> or <str> that satisfies block
	"""
    def confirm_header(self, nonce):
        if self.block_no != -1:
            return
    	to_hash = self.hash_contents() + nonce
        hashed = hashlib.sha256(to_hash).hexdigest()
        if int(hashed,16) < int(self.difficulty,16):
			self.header = hashed
			self.nonce = nonce
            self.block_no = self.parent_block_no + 1

    """
	Confirms if block is a valid block.
	"""
	def is_valid_block(self):
		hashed = hashlib.sha256(self.hash_contents() + self.nonce)
		if int(hashed,16) < int(self.difficulty,16):
			return True
		return False

    def __eq__(self, other):
        return isinstance(other, ShardBlock) and self.hash_contents() == other.hash_contents()

    def __hash__(self):
        return self.hash_contents()
