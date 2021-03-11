import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('data.csv')
x = dataset.iloc[:, 2: 32].values
y = dataset.iloc[:, 1].values

from sklearn.preprocessing import LabelEncoder
labelencoder_y=LabelEncoder()
y=labelencoder_y.fit_transform(y)

from sklearn.model_selection import train_test_split
X, x_test, Y, y_test =  train_test_split(x, y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc_x=StandardScaler()
X=sc_x.fit_transform(X)
x_test=sc_x.transform(x_test)

# K-Nearest Neighbour
def dist(x1,x2):
    return np.sqrt(sum((x1-x2)**2))
def knn(query_x,X,Y,k=5):
    vals=[]
    m=X.shape[0]
    
    for i in range(m):
        d=dist(query_x,X[i])
        vals.append((d,Y[i]))
        
    vals=sorted(vals)
    vals=vals[:k]
    vals=np.array(vals)
    
    new_vals = np.unique(vals[:,1],return_counts=True)
    #print(new_vals)
    
    index = new_vals[1].argmax()
    pred = new_vals[0][index]
    
    return pred

size=int(x_test.shape[0])
anslist=[]
for i in range(size):
    query_x=x_test[i]
    q=int(knn(query_x,X,Y))
    anslist.append(q)
    
dict={"Outcome" : anslist}
y_knn = pd.DataFrame(dict)
  
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_knn)

acc_knn = (cm[0][0] + cm[1][1])*100/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])

# Logistic Regression
def hypothesis(x,w,b):
    '''accepts input vector x, input weight vector w and bias b'''
    
    h = np.dot(x,w) + b
    return sigmoid(h)

def sigmoid(z):
    return 1.0/(1.0 + np.exp(-1.0*z))

def error(y_true,x,w,b):
    
    m = x.shape[0]
    
    err = 0.0
    
    for i in range(m):
        hx = hypothesis(x[i],w,b)
        if hx!=1.0:
            err += y_true[i]*np.log2(hx) + (1-y_true[i])*np.log2(1-hx)
    return -err/m


def get_grads(y_true,x,w,b):
    
    grad_w = np.zeros(w.shape)
    grad_b = 0.0
    
    m = x.shape[0]
    
    for i in range(m):
        hx = hypothesis(x[i],w,b)
        
        grad_w += (y_true[i] - hx)*x[i]
        grad_b +=  (y_true[i]-hx)
        
    
    grad_w /= m
    grad_b /= m
    
    return [grad_w,grad_b]


# One Iteration of Gradient Descent
def grad_descent(x,y_true,w,b,learning_rate=0.1):
    
    err = error(y_true,x,w,b)
    [grad_w,grad_b] = get_grads(y_true,x,w,b)
    
    w = w + learning_rate*grad_w
    b = b + learning_rate*grad_b
    
    return err,w,b
    
def predict(x,w,b):
    
    confidence = hypothesis(x,w,b)
    if confidence<0.5:
        return 0
    else:
        return 1
    
def get_acc(x_tst,y_tst,w,b):
    
    y_pred = []
    
    for i in range(y_tst.shape[0]):
        p = predict(x_tst[i],w,b)
        y_pred.append(p)
        
    y_pred = np.array(y_pred)
    
    return  float((y_pred==y_tst).sum())/y_tst.shape[0]

# Intialising Loss Acc Weight and Bias
loss = []
acc = []

W = 2*np.random.random((X.shape[1],))
b = 5*np.random.random()

# Weight Updation Process
for i in range(1000):
    l,W,b = grad_descent(X,Y,W,b,learning_rate=0.1)
    acc.append(get_acc(x_test,y_test,W,b))
    loss.append(l)
y_pred = []    
for i in range(x_test.shape[0]):
        p = predict(x_test[i],W,b)
        y_pred.append(p)
        
y_pred = np.array(y_pred)

plt.plot(loss)
plt.ylabel("Negative of Log Likelihood")
plt.xlabel("Time")
plt.show()

plt.plot(acc)
plt.show()
print(acc[-1])

# Artificial Neural Network
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

classifier_ann = Sequential()
classifier_ann.add(Dense(units = 15, activation = 'relu', input_dim = 30))
classifier_ann.add(Dense(units = 15, activation = 'relu'))
classifier_ann.add(Dense(units = 1, activation = 'sigmoid'))
classifier_ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
classifier_ann.fit(X, Y, batch_size = 8, epochs = 100)

y_ann = classifier_ann.predict(x_test) 
y_ann = (y_ann > 0.5)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_ann)

acc_ann = (cm[0][0] + cm[1][1])*100/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])
