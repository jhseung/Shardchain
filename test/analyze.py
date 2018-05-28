import json, heapq

with open('data.json') as f:
    data = json.load(f)

reverse_data = {}

num_tx = 0
max_tx = 0
transactions = []
for k,v in data.iteritems():
    num_tx += int(v)
    max_tx = max(int(v), max_tx)
    if v in reverse_data:
        reverse_data[v].append(k)
    else:
        reverse_data[v] = [k]
    transactions.append(int(v))

def print_tx_data(num):
    N = num
    largest_n = heapq.nlargest(N,transactions)
    total_tx_by_N = sum(largest_n)
    percentage_of_total = total_tx_by_N * 100.0 / num_tx

    print "Total transactions: {0}".format(num_tx)
    print "Total transactions by top {0} accounts: {1}".format(N,total_tx_by_N)
    print "Percentage of transactions by {0} largest accounts take up {1}%\n".format(N, percentage_of_total)

test_nums = [5,10,20,50,100,200]
for i in test_nums:
    print_tx_data(i)
