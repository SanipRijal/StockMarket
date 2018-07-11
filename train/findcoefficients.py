import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing


#importing the dataset
dataset = pd.read_csv('/home/sanip/Development/StockMarket/data/companyData/sample.csv')
X = dataset.reindex(columns=['High', 'Low', 'Open', 'Quantity', 'Turnover'])
X_train= X[1:len(X)+1]
print(X)
#X_scaled = preprocessing.scale(X_train)
y = dataset.reindex(columns=['LTP'])
y_train = list(y[:-1])
#y_scaled = preprocessing.scale(y_train)
len(y_train)

#axis=0 for row
np.append(arr=np.ones([len(X_train), 1]).astype(int), values = X_train, axis=1)
est = sm.OLS(endog=y_train, exog= X_train).fit()
est.summary()

model = sm.ols(formula='LTP~High+Low+Open+Quantity+Turnover', data=dataset)
results_formula = model.fit()
results_formula.params

X = [[345, 343, 344, 6191, 2133740]]
df_new = pd.DataFrame(X, columns=['High', 'Low', 'Open', 'Quantity', 'Turnover'])
fitter_Y = results_formula.predict(exog=df_new)
print(fitter_Y)