from sklearn.datasets import load_digits

digits=load_digits()

digits.data
# Out[214]: 
# array([[  0.,   0.,   5., ...,   0.,   0.,   0.],
#        [  0.,   0.,   0., ...,  10.,   0.,   0.],
#        [  0.,   0.,   0., ...,  16.,   9.,   0.],
#        ..., 
#        [  0.,   0.,   1., ...,   6.,   0.,   0.],
#        [  0.,   0.,   2., ...,  12.,   0.,   0.],
#        [  0.,   0.,  10., ...,  12.,   1.,   0.]])

from sklearn.datasets import load_digits

digits=load_digits()

digits.data
# Out[214]: 
# array([[  0.,   0.,   5., ...,   0.,   0.,   0.],
#        [  0.,   0.,   0., ...,  10.,   0.,   0.],
#        [  0.,   0.,   0., ...,  16.,   9.,   0.],
#        ..., 
#        [  0.,   0.,   1., ...,   6.,   0.,   0.],
#        [  0.,   0.,   2., ...,  12.,   0.,   0.],
#        [  0.,   0.,  10., ...,  12.,   1.,   0.]])

from sklearn.cross_validation import train_test_split

x_train, x_test, y_train, y_test=train_test_split(digits.data, digits.target, test_size=0.25, random_state=33)

from sklearn.preprocessing import StandardScaler

from sklearn.svm import LinearSVC

ss = StandardScaler()

x_train=ss.fit_transform(x_train)

x_test=ss.transform(x_test)
lsvc=LinearSVC()

lsvc.fit(x_train, y_train)
y_predict=lsvc.predict(x_test)


from sklearn.metrics import classification_report

classification_report(y_test, y_predict,target_names=digits.target_names.astype(str))
# Out[236]: '             precision    recall  f1-score   support\n\n          0       0.92      1.00      0.96        35\n          1       0.96      0.98      0.97        54\n          2       0.98      1.00      0.99        44\n          3       0.93      0.93      0.93        46\n          4       0.97      1.00      0.99        35\n          5       0.94      0.94      0.94        48\n          6       0.96      0.98      0.97        51\n          7       0.92      1.00      0.96        35\n          8       0.98      0.84      0.91        58\n          9       0.95      0.91      0.93        44\n\navg / total       0.95      0.95      0.95       450\n'






