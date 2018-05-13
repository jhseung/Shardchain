import json, transaction

def tx_to_json(tx):
	assert isinstance(tx, transaction.Transaction)
	return json.dumps({sender: tx.sender,
					   recipient: tx.recipient,
					   amount: tx.amount,
					   jsontype: tx.jsontype})

def json_to_tx(json_input):
	try:
		decoded = json.loads(json_input)
		return Transaction(decoded["sender"],decoded["recipient"], decoded["amount"])

	except (ValueError, KeyError, TypeError):
		print "JSON format error"

