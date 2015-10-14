__author__ = 'dantipov'


def merge(x, y):
    res = []
    i1, i2 = 0, 0
    while i1 < len(x) or i2 < len(y):
        if i1 == len(x) or i2 < len(y) and x[i1] > y[i2]:
            res.append(y[i2])
            i2 += 1
        elif i2 == len(y) or x[i1] < y[i2]:
            res.append(x[i1])
            i1 += 1
        else:
            res.append(x[i1])
            i1 += 1
            i2 += 1
    return res


def intersect(set1, set2):
    return {i for i in set1 if i in set2}


def issubset(subset, superset):
    i1, i2 = 0, 0
    while i1 < len(subset) and i2 < len(superset) and len(superset) - i2 >= len(subset) - i1:
        if subset[i1] == superset[i2]:
            i1 += 1
        i2 += 1
    return i1 == len(subset)

eps = 3

f = open("supermarket.arff")

item_names = [i for i in f.readline().split('\'')[1:-1] if i != ',']
item_numbers = {item_names[i]: i for i in range(len(item_names))}
transactions = {}

for s in f.readlines():
    basket_id, good = int(s.split(',')[-1]), s.split('\'')[1]
    if good in item_names:
        if basket_id in transactions:
            transactions[basket_id].append(item_numbers[good])
        else:
            transactions[basket_id] = [item_numbers[good]]

for basket_id in transactions:
    transactions[basket_id].sort()

# apriori begins here
result = []
transaction_lists = [set() for i in range(len(item_names))]
for t in transactions:
    for i in transactions[t]:
        transaction_lists[i].add(t)
L = [[i] for i in range(len(item_names)) if len(transaction_lists[i]) > eps]
transaction_lists = [transaction_lists[i] for i in range(len(transaction_lists)) if len(transaction_lists[i]) > eps]
items = [i for i in range(len(item_names)) if len(transaction_lists[i]) > eps]
k = 2


while len(L) >= k:
    # set of candidates rules
    C = []
    new_transaction_lists = []
    for i in range(0, len(L) - k):
        for j in range(i + 1, len(L) - k + 1):
            candidate = merge(L[i], L[j])
            if k == 2:
                C.append(candidate)
                new_transaction_lists.append(intersect(transaction_lists[i], transaction_lists[j]))
            elif len(candidate) == k and candidate not in C:
                counter = 0
                subsets = []
                for l in range(j + 1, len(L)):
                    if issubset(L[l], candidate):
                        counter += 1
                        subsets.append(l)
                    if counter == k - 2:
                        C.append(candidate)
                        transaction_list = intersect(transaction_lists[i], transaction_lists[j])
                        for m in subsets:
                            transaction_list = intersect(transaction_list, transaction_lists[m])
                        new_transaction_lists.append(transaction_list)
                        break

    transaction_lists = new_transaction_lists
    print("candidates done")

    L = [C[i] for i in range(len(C)) if len(transaction_lists[i]) > eps]
    transaction_lists = [t for t in transaction_lists if len(t) > eps]

    for i in range(len(L)):
        result.append((len(transaction_lists[i]), L[i]))
    k += 1

result.sort()
for r in result:
    print(r[0], [item_names[i] for i in r[1]])
