__author__ = 'dantipov'

eps = 5

f = open("supermarket.arff")

items = [i for i in f.readline().split('\'')[1:-1] if i != ',']
transactions = {}

for s in f.readlines():
    id, good = int(s.split(',')[-1]), s.split('\'')[1]
    if transactions.__contains__(id):
        transactions[id].append(good)
    else:
        transactions[id] = [good]

#apriori begins here
result = []
L = [{i} for i in items]
k = 2
while len(L) > 0:
    C = [{*i, j} for j in items if j not in i for i in L ]

