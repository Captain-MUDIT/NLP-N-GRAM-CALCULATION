import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import classification_report

df=pd.read_csv("updated_dating.csv")
print(df) 

# splitted the data to train and test in 80-20 ratio
train,test=np.split(df.sample(frac=1),[int(0.8*len(df))])


def scale_dataset(dataframe):
  x= dataframe[dataframe.columns[:-1]].values 
  y= dataframe[dataframe.columns[-1]].values

  data= np.hstack((x,np.reshape(y,(-1,1))))

  return data,x,y

train,x_train,y_train= scale_dataset(train)
test,x_test,y_test = scale_dataset(test)

# training model on provided data
svm_model = SVC()
svm_model = svm_model.fit(x_train , y_train)


y_pred = svm_model.predict(x_test)
print(classification_report(y_test,y_pred))


# This section is same as above implemented just to plot the graph 
df1=pd.read_csv("updated.csv")
print(df1)

train,test=np.split(df1.sample(frac=1),[int(0.8*len(df1))])

train,x_train,y_train= scale_dataset(train)
test,x_test,y_test = scale_dataset(test)

svm_model1 = SVC()
svm_model1 = svm_model1.fit(x_train , y_train)

svm_model1 = SVC()
svm_model1 = svm_model1.fit(x_train , y_train)


# The code below is used  to plot the graph 
from sklearn.inspection import DecisionBoundaryDisplay

X = df1[df1.columns[:-1]].values
y = df1[df1.columns[-1]].values

disp = DecisionBoundaryDisplay.from_estimator(
    svm_model1, X, response_method="predict",
    xlabel= "attractiveness", ylabel= "fun",
    alpha=0.5,
)

b1=disp.ax_.scatter(X[:, 0], X[:, 1], c= y ,edgecolor="k")

plt.legend(
    [b1],
    [
        "0",
        "1",
      ],
    loc="upper left",
    title="DECISION"
)

plt.show()