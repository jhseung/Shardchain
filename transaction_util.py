import json, transaction

def tx_to_json(tx):
	assert isinstance(tx, transaction.Transaction)
	return json.dumps({sender: tx.sender
					   recipient: tx.recipient,
					   amount: tx.amount,
					   jsontype: tx.jsontype})