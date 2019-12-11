#!/bin/sh
mkdir -p mnist
cd mnist
wget https://pjreddie.com/media/files/mnist_train.csv
cut -d, -f2- mnist_train.csv > mnist_train_feature
cut -d, -f1 mnist_train.csv > mnist_train_labels
