from sklearn import datasets

iris = datasets.load_iris()

digits = datasets.load_digits()

print digits.data
# [[  0.   0.   5. ...,   0.   0.   0.]
#  [  0.   0.   0. ...,  10.   0.   0.]
#  [  0.   0.   0. ...,  16.   9.   0.]
#  ..., 
#  [  0.   0.   1. ...,   6.   0.   0.]
#  [  0.   0.   2. ...,  12.   0.   0.]
#  [  0.   0.  10. ...,  12.   1.   0.]]

print digits.target
# [0 1 2 ..., 8 9 8]

