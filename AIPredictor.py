import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

dataset = pd.read_excel("Liberty Data Prediction.xlsx", 'Important Data')

X = dataset.drop(['Permit/SqFt','CLabor/SqFt','CMaterials/SqFt','Blabor/SqFt','Bmaterials/SqFt','Electrical/SqFt','Framing/SqFt','Lumber/SqFt','Plumbing/SqFt','RLabor/SqFt','Rmaterials/SqFt','SLabor/SqFt','SMaterials/SqFt','SiLabor/SqFt','SiMaterials/SqFt','TLabor/SqFt','TMaterials/SqFt','Truss/SqFt','Heating/SqFt','Insulation/SqFt','Engineering/SqFt','Excavation/SqFt','Foundation/SqFt','Gravel/SqFt','Painting/SqFt'], axis=1)
YP = dataset['Permit/SqFt']

X_train, X_valid, YP_train, YP_valid = train_test_split(
    X, YP, train_size=0.8, test_size=0.2, random_state=0)

model_LR = LinearRegression()
model_LR.fit(X_train, YP_train)
YP_pred = model_LR.predict(X_valid)
 
print(mean_absolute_percentage_error(YP_valid, YP_pred))

# Printing first 5 records of the dataset
print(X_valid)
print(YP_pred)
