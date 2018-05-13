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

        