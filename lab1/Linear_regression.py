__author__ = 'Den'

from numpy import sum

iterations = 1000
alpha = 0.00000001


dataset = [{'meters': int(s.split(',')[0]), 'rooms': int(s.split(',')[1]), 'price' : int(s.split(',')[2])} for s in open('prices.txt').readlines()]

def linear_regression(learning_set):
    global iterations, alpha
    theta = (0, 0, 0)
    h = lambda meters, rooms: theta[0] + meters * theta[1] + rooms * theta[2]
    for i in range(iterations):
        theta = (theta[0] - sum([(h(x['meters'], x['rooms']) - x['price']) for x in learning_set]) * alpha / len(learning_set),
                 theta[1] - sum([(h(x['meters'], x['rooms']) - x['price']) * x['meters'] for x in learning_set]) * alpha / len(learning_set),
                 theta[2] - sum([(h(x['meters'], x['rooms']) - x['price']) * x['rooms'] for x in learning_set]) * alpha / len(learning_set))
    return h, theta




for i in range(4):
    testing_set = dataset[i * (len(dataset) // 4) : (i + 1) * (len(dataset) // 4)]
    learning_set = dataset[:i * (len(dataset) // 4)] + dataset[(i + 1) * (len(dataset) // 4):]
    h, theta = linear_regression(learning_set)
    error = sum([abs(h(x['meters'], x['rooms']) - x['price']) / x['price'] for x in testing_set]) / len(testing_set)
    print('Split', i, ':', error, 'theta:', theta)