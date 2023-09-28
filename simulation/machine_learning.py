import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file into a Pandas DataFrame
df = pd.read_csv('interaction_history.csv')

# Display the first few rows of the DataFrame
print(df.head())

# Analyze the data and find correlations
correlations = df.corr()

# Visualize the correlations using a heatmap
plt.figure(figsize=(8, 6))
plt.imshow(correlations, cmap='coolwarm', interpolation='none', aspect='auto')
plt.colorbar()
plt.xticks(range(len(correlations)), correlations.columns, rotation='vertical')
plt.yticks(range(len(correlations)), correlations.columns)
plt.title('Correlation Heatmap')
plt.show()

# Print the correlation values
print('Correlation Matrix:')
print(correlations)

# Example: To find the correlation between 'Trade_Count' and 'Is_Alive'
trade_alive_corr = df['Trade_Count'].corr(df['Is_Alive'])
print(f'Correlation between Trade_Count and Is_Alive: {trade_alive_corr:.2f}')


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load your data into a DataFrame (replace with your data)
data = pd.read_csv('interaction_history.csv')

# Drop the 'agent_id' column and separate features (X) and target (y)
X = data.drop(['Agent_ID', 'Is_Alive'], axis=1)
print(X.head())
y = data['Is_Alive']

# Split the data into training and testing sets (adjust test_size and random_state)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize feature data (optional, but can improve some models)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create and train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:\n', report)

import joblib

joblib.dump(model,'model_filename.pkl')

new_data = pd.read_csv('interaction_history2.csv')
results = new_data['Is_Alive']
new_data = new_data.drop(['Agent_ID','Is_Alive'], axis=1)

print(new_data.head())

scaler = StandardScaler()
new_data = scaler.fit_transform(new_data)

print(new_data)  # Scale new data if needed
prediction = model.predict(new_data)

i = 0
num_right = 0
num_wrong = 0
while i < len(results):

    if prediction[i] == results[i]:
        num_right += 1
        
        i +=1
    else:
        
        num_wrong +=1 
        i+=1

print("Number of correct predictions ===>", num_right)
print("Number of wrong predictions ===>", num_wrong)
print("Right/Wrong Ratio ===>",num_right/num_wrong)