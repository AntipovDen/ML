__author__ = 'dantipov'

from matplotlib import pyplot as plt

dimension = 28 * 28
learning_set_size = 60000  # we can read it, but why?
test_set_size = 10000  # we can read it, but why?
alpha = 8.75 * 10. ** (-10)  # learning rate that was taken by testing


# it's just for test
def print_digit(digit):
    for row in range(28):
        for column in range(28):
            print(str(digit[row * 28 + column]).ljust(4), end='')
        print()


def rank(x, weights):
    return sum([x[i] * weights[i] for i in range(dimension)]) + weights[-1]


def learn(learning_set, learning_labels, learning_set_size):
    weights = [0] * (dimension + 1)
    for i in range(learning_set_size):
        error_i = alpha * (learning_labels[i] - rank(learning_set[i], weights))
        for j in range(dimension):
            weights[j] += error_i * learning_set[i][j]
        weights[-1] += error_i
    return weights


def read_dataset(set_file, labels_file, set_size):
    f = open(labels_file, 'br')
    f.read(8)
    labels = list(f.read(set_size))
    f.close()

    f = open(set_file, 'br')
    f.read(16)
    pixels = list(f.read(set_size * dimension))
    images = [pixels[n * dimension:(n + 1) * dimension] for n in range(set_size)]
    f.close()
    return images, labels


learn_dataset_file = 'digits/train-images-idx3-ubyte'
learn_labels_file = 'digits/train-labels-idx1-ubyte'
test_dataset_file = 'digits/t10k-images-idx3-ubyte'
test_labels_file = 'digits/t10k-labels-idx1-ubyte'


learn_dataset, learn_labels = read_dataset(learn_dataset_file, learn_labels_file, learning_set_size)
perceptrone = learn(learn_dataset, learn_labels, learning_set_size)


test_dataset, test_labels = read_dataset(test_dataset_file, test_labels_file, test_set_size)

# show error distribution
errors = [0 for i in range(100)]
for i in range(test_set_size):
    error = abs(rank(test_dataset[i], perceptrone) - test_labels[i])
    if error < 10.0: errors[round(error * 10)] += 1
plt.plot([i * 0.1 for i in range(100)], errors, 'b-')
plt.show()
for i in range(1, 100):
    errors[i] += errors[i - 1]
plt.plot([i * 0.1 for i in range(100)], errors, 'b-')
plt.show()

# show the rank results
results = [[0] * 10 for i in range(10)]
for i in range(test_set_size):
    cur_rank = round(rank(test_dataset[i], perceptrone))
    if cur_rank < 0: cur_rank = 0
    elif cur_rank > 9: cur_rank = 9
    results[test_labels[i]][cur_rank] += 1

print("___|___0___1___2___3___4___5___6___7___8___9")
for i in range(10):
    print("  " + str(i) + "|", end='')
    for j in results[i]:
        print(str(j).rjust(4), end='')
    print()
