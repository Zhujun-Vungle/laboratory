import pandas as pd 
import numpy as np 
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report

column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

data = pd.read_csv('data.csv', names = column_names)


data = data.replace(to_replace='?', value = np.nan)
data = data.dropna(how='any')

# split data to test and train
x_train, x_test, y_train, y_test = train_test_split(data[column_names[1:10]], data[column_names[10]], test_size=0.25, random_state=33)

# standardlize data
ss = StandardScaler()

x_train = ss.fit_transform(x_train)
x_test = ss.fit_transform(x_test)

lr = LogisticRegression()
sgdc = SGDClassifier()

lr.fit(x_train, y_train)
lr_y_predict = lr.predict(x_test)


sgdc.fit(x_train, y_train)
sgdc_y_predict = sgdc.predict(x_test)

print lr.score(x_test, y_test)
print classification_report(y_test, lr_y_predict, target_names=["Benign", "Maligant"])
