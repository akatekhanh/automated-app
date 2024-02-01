
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso



# Task 1:
# Load the data
data = pd.read_csv('ToyotaCorolla.csv')

# Define the predictors
predictors = data.drop(columns=['Id', 'Model', 'Price'])

# Define the target variable
target = data['Price']


# Task 2:
# Check the descriptive statistics of the predictors
predictors.describe()


# Task 3
# Remove the "Automatic" column
predictors = predictors.drop(columns=['Cylinders'])

# Standardize the predictors
scaler = StandardScaler()
predictors_standardized = pd.DataFrame(scaler.fit_transform(predictors), columns=predictors.columns)


# Task 4:
# Split the dataset into training (65%) and test (35%)
X_train, X_test, y_train, y_test = train_test_split(predictors_standardized, target, test_size=0.35, random_state=446)


# Task 4:
# Develop a linear regression model
model = LinearRegression()

# Fit the model on the training dataset
model.fit(X_train, y_train)

# Predict the target value of the test dataset
y_pred = model.predict(X_test)

# Report the Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)


# Task 5:
# Develop a ridge regression model
# model = Ridge(alpha=1)
# model = Ridge(alpha=10)
# model = Ridge(alpha=100)
# model = Ridge(alpha=1000)
model = Ridge(alpha=10000)

# Fit the model on the training dataset
model.fit(X_train, y_train)

# Predict the target value of the test dataset
y_pred = model.predict(X_test)

# Report the Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Report the coefficients
coefficients = model.coef_
print("Coefficients:", coefficients)


# Task 6
# Develop a LASSO model
# model = Lasso(alpha=1)
# model = Lasso(alpha=10)
# model = Lasso(alpha=100)
# model = Lasso(alpha=1000)
model = Lasso(alpha=10000)


# Fit the model on the training dataset
model.fit(X_train, y_train)

# Predict the target value of the test dataset
y_pred = model.predict(X_test)

# Report the Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Report the coefficients
coefficients = model.coef_
print("Coefficients:", coefficients)
