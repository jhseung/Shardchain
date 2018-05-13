import block_util

class Transaction:
    """
    :sender: <str> sender's account address
    :recipient: <str> recipient's account address
    :amount: <float> amount of money to send
    """
    def __init__(self,
                sender,
                recipient,
                amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.is_intershard = self.is_intershard()
    
    def is_intershard(self):
        if block_util.to_shard(self.sender) == block_util.to_shard(self.recipient):
            return True
        else:
            return False