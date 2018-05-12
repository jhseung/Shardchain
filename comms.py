import socket

""" Broadcast transaction signed with key """
def broadcast_tx(socket, neighbor_list, tx):


""" Broadcast mined block (faulty or not) """
def broadcast_block(socket, neighbor_list, block):


""" Request block block_no """
def request_block(socket, req_target, block_no):


""" Request chain head """
def request_most_recent_block(socket, req_target):


