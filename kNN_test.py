import csv
import random
import math
import operator

def loadDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        print 'Data set: ' + repr(len(dataset))
        for x in range(len(dataset)):
            if random.random() < 0.2:
                for y in range(57):
                    dataset[x][y] = float(dataset[x][y])
                if random.random() < split:
                    trainingSet.append(dataset[x])
                else:
                    testSet.append(dataset[x])

def cosineDistance(instance1, instance2, length):
    distance = 0
    a = 0
    b = 0
    for x in range(length):
        a += pow(instance1[x],2)
        b += pow(instance2[x],2)
        distance += instance1[x] * instance2[x]
    a = math.sqrt(a)
    b = math.sqrt(b)
    distance = float(distance) / float(a * b)
    return 1 - distance

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = cosineDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0

def main():
    trainingSet = []
    testSet = []
    split = 0.67
    loadDataset('spambase.data.csv', split, trainingSet, testSet)
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))

    testcase = input("Masukkan jumlah testcase : ")


    for t in range(testcase):
        predictions = []
        k = input("Masukkan nilai k : ")
        # print ("\n")

        for x in range(len(testSet)):
           # print "Data test: " + repr(testSet[x])
           neighbors = getNeighbors(trainingSet, testSet[x], k)
           result = getResponse(neighbors)
           predictions.append(result)
           # print('Prediksi =' + repr(result) + ', Sebernarnya =' + repr(testSet[x][-1]))
           # print "-------------------------------------------------"

        accuracy = getAccuracy(testSet, predictions)
        print('Akurasi: ' + repr(accuracy) + '%' + '\n')

main()