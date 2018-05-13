import time
import copy

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
				 block_no, 
				 parent_block_no, 
				 parent_hash,
				 parent_block = None,
				 transactions = [],
				 starting_state = {},
				 timestamp = time.time(),
				 difficulty = 0,
				 nonce = 0):
        self.shard_id = shard_id
        self.block_no = block_no
		self.parent_hash = parent_hash
		self.parent_block = parent_block
		self.transactions = transactions
		self.starting_state = starting_state
		self.resulting_state = copy.deepcopy(starting_state) #copying dic to maintain starting_state for now
		self.timestamp = timestamp
		self.difficulty = difficulty
		self.nonce = nonce

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
        if transaction.sender not in starting_state:
            return False
        if starting_state[transaction.sender] < transaction.amount:
            return False
        if not isinstance(transaction.amount, float) or transaction.amount < 0:
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
        if not _is_transaction_valid(transaction):
            print "INVALID TRANSACTION"
            return
        self.starting_state[transaction.sender] -= transaction.amount
        if transaction.recipient not in starting_state:
            self.starting_state[transaction.recipient] = transaction.amount
        else:
            self.starting_state[transaction.recipient] = self.starting_state[transaction.recipient] +\
            transaction.amount
    
    """
    Creates a SHA256 hash of the block
    :return: <str> 
    """
    def hash_block(self):
        txs = list(map(lambda x : x.sender + x.recipient + str(x.amount), self.transactions))
		header = self.parent_hash + self.txs + self.timestamp
        return hashlib.sha256(header).hexdigest()
    
    def __eq__(self, other):
        return isinstance(other, ShardBlock) and hash_block() == other.hash_block()

    def __hash__(self):
        return hash_block()