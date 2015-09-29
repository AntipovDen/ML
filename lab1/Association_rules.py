__author__ = 'dantipov'

eps = 2

def set_in_multiset(set, multiset):
    for set1 in multiset:
        if set == set1:
            return True
    return False

def subsets_in_L(set, L):
    for element in set:
        set.remove(element)
        if not set_in_multiset(set, L):
            return False
        set.add(element)
    return True

f = open("supermarket.arff")

#items = [i for i in f.readline().split('\'')[1:-1] if i != ',']
items = [i for i in f.readline().split('\'')[1:100] if i != ',']
transactions = {}

for s in f.readlines():
    id, good = int(s.split(',')[-1]), s.split('\'')[1]
    if good in items and transactions.__contains__(id):
        transactions[id].append(good)
    else:
        transactions[id] = [good]


#apriori begins here
result = []
L = [{i} for i in items]
k = 2
while len(L) > 0:
    C = [{*i, j} for j in items for i in L if j not in i and subsets_in_L({*i, j}, L)]
    count = [0] * len(C)
    for id in transactions:
        for i in range(len(C)):
            if C[i].issubset(transactions[id]):
                count[i] += 1
    L = [C[i] for i in range(len(C)) if count[i] >= eps]
    for c in L:
        if not set_in_multiset(c, result):
            result.append(c)
    k += 1

for r in result:
    print(r)
