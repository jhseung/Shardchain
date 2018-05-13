import socket
from block_util import *
from transaction_util import *

""" Broadcast transaction signed with key """
def broadcast_tx(sock, neighbor_list, tx):
	for addr in neighbor_list:
		sock.send(tx_to_json(tx), addr)
    

""" Broadcast mined block (faulty or not) """
def broadcast_block(sock, neighbor_list, block):
    for addr in neighbor_list:
    	sock.send(block_to_json(block), addr)

""" Request block block_no """
def request_block(sock, req_target, block_no):
    pass

""" Request chain head """
def request_most_recent_block(sock, req_target):
    pass
