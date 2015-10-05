__author__ = 'dantipov'

eps = 5

def issubset(subset, set):
    i_set = 0
    for i in subset:
        while i_set < len(set) and set[i_set] < i:
            i_set += 1
        if i_set == len(set) or set[i_set] > i:
            return False
    return True


def subsets_in_L(set, L):
    k = len(set)
    for s in L:
        if issubset(s, set):
            k -= 1
    return k == 0

f = open("supermarket.arff")

item_names = [i for i in f.readline().split('\'')[1:-1] if i != ',']
item_numbers = {item_names[i] : i for i in range(len(item_names))}
transactions = {}

for s in f.readlines():
    id, good = int(s.split(',')[-1]), s.split('\'')[1]
    if good in item_names:
        if transactions.__contains__(id):
            transactions[id].append(item_numbers[good])
        else:
            transactions[id] = [item_numbers[good]]

for id in transactions:
    transactions[id].sort()

#apriori begins here
result = []
count = [0] * len(item_names)
for t in transactions:
    for i in transactions[t]:
        count[i] += 1
L = [[i] for i in range(len(item_names)) if count[i] > eps]
items = [i for i in range(len(item_names)) if count[i] > eps]
k = 2
print(len(items))
print(items)

while len(L) > 0:
    #set of candidates rules
    print(k)
    C = [(i + [j]) for i in L for j in range(i[-1] + 1, len(item_names)) if j in items and subsets_in_L(i + [j], L)]

    count = [0] * len(C)
    for id in transactions:
        if len(transactions[id]) >= k:
            for i in range(len(C)):
                if issubset(C[i], transactions[id]):
                    count[i] += 1

    print(count)
    L = [C[i] for i in range(len(C)) if count[i] >= eps]
    count = [c for c in count if c >= eps]

    for i in range(len(L)):
        result.append((count[i], L[i]))
    k += 1

for r in result:
    print(r[0], r[1])

