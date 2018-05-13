import socket

""" Broadcast transaction signed with key """
def broadcast_tx(socket, neighbor_list, tx):
    pass

""" Broadcast mined block (faulty or not) """
def broadcast_block(socket, neighbor_list, block):
    pass

""" Request block block_no """
def request_block(socket, req_target, block_no):
    pass

""" Request chain head """
def request_most_recent_block(socket, req_target):
    pass
