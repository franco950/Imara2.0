import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import classification_report 
from sklearn.model_selection import train_test_split 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV 
import time
start=time.time()
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# csv_file_path='grid_search_results.csv'
# df=pd.read_csv(csv_file_path)
# df_sorted = df.sort_values(by='mean_test_score', ascending=False)
# selected=['mean_fit_time','mean_score_time','execution_time_seconds','params','rank_test_score','mean_test_score']
# print(df_sorted[selected])

# stats={}
csv_file_path='creditcard.csv'
df=pd.read_csv(csv_file_path)
df.drop_duplicates(inplace = True)
#empty=df[df.isnull().any(axis=1)]
X = df.drop("Class", axis=1) 
y = df['Class'] 
f=[]
f.append(df.columns)
print(f)

# #stats['rows with null values']=len(empty)
# #stats['fraud class values']=df['Class'].value_counts()
# # Convert time from seconds to hours
# df['time_hours'] = df['Time'] / 3600  # 1 hour = 3600 seconds

# # Round down to the nearest hour
# df['hour'] = df['time_hours'].astype(int)
# fraud=df[df['Class']==1]
# legit=df[df['Class']==0]

# Count the number of transactions in each hour for fraud and legitimate transactions
# transactions_per_hour_fraud = fraud['hour'].value_counts().sort_index()
# transactions_per_hour_legit = legit['hour'].value_counts().sort_index()

# Create subplots
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# # Plot fraud transactions
# axes[0].bar(transactions_per_hour_fraud.index, transactions_per_hour_fraud, color='red', edgecolor='black')
# axes[0].set_title('Number of Fraud Transactions per Hour')
# axes[0].set_xlabel('Hour')
# axes[0].set_ylabel('Number of Transactions')
# axes[0].tick_params(axis='x', rotation=45)

# # Plot legitimate transactions
# axes[1].bar(transactions_per_hour_legit.index, transactions_per_hour_legit, color='green', edgecolor='black')
# axes[1].set_title('Number of Legitimate Transactions per Hour')
# axes[1].set_xlabel('Hour')
# axes[1].set_ylabel('Number of Transactions')
# axes[1].tick_params(axis='x', rotation=45)

# # Adjust layout to prevent overlapping
# plt.tight_layout()
# plt.show()
# sns.barplot(y=fraud['Amount'], x=df['hour'])
# plt.show()
# print(4)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# stats.append([X_train.shape, X_test.shape] )
# print(stats)
# print(df.info())
# print(df.columns())

# Correlation matrix 

# sns.heatmap(df.corr(), linewidth=.5)
# plt.show()
#new.get_figure().savefig("heatmap_output.png", bbox_inches='tight')
#correlation=df.corr()['Class']
# sns.scatterplot(data=df, x='Amount', y='Class', hue='Class', palette='viridis')

# plt.title('Scatter Plot of Amount vs Class')
# Show the plot (optional)



#sns.barplot(x=correlation.index, y=correlation.values)

# plt.title('Correlation with Class')
# plt.ylabel('Correlation Coefficient')
# plt.xticks(rotation=45, ha='right')  


#labels = ['Legitimate', 'Fraud']

# Plotting the pie chart
#plt.pie(df['Class'].value_counts(), labels=labels, autopct='%1.1f%%')
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply SMOTE for oversampling
#smote = SMOTE(random_state=42)
#X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Display the plot
#plt.show()

# plt.show()

#print(df.describe())
#legitimate=len(df[df.Class==0])
#fraudulent=len(df[df.Class==1])



# Instantiate RandomForestClassifier with specified parameters
#clf = RandomForestClassifier(n_jobs=-1, random_state=42)

# Fit the model
# clf.fit(X_train, y_train)

# # Make predictions
# y_pred = clf.predict(X_test)


# Save the dataframe as a csv file
#test.to_csv("sample.csv", index=False)


#joblib.dump(classifier, 'trained_model.joblib')

# performance evaluation metrics 
 
# param_grid = { 
#     'n_estimators': [ 50, 100], 
#     'max_features': ['sqrt', 'log2', None], 
#     'max_depth': [ 6, 9], 
# } 
# # grid_search = GridSearchCV(RandomForestClassifier(n_jobs=-1, random_state=42), 
# #                            param_grid=param_grid) 
# # grid_search.fit(X_train, y_train) 
# # print(grid_search.best_estimator_) 
# random_search = RandomizedSearchCV(RandomForestClassifier(n_jobs=1, random_state=42), 
#                                    param_grid) 
# random_search.fit(X_train, y_train) 
# print(random_search.best_estimator_) 
# estimate=random_search.best_estimator_
# estimate.to_csv("estimate.csv", index=False)
# #print(classification_report(y_pred,y_test)) 
# print(stats)
# end_time = time.time()

# # Calculate the elapsed time
# elapsed_time = end_time - start

# # Print the result
# print(f"Execution time: {elapsed_time:.2f} seconds")