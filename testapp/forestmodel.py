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
stats=[]
csv_file_path='creditcard.csv'
df=pd.read_csv(csv_file_path)
df.drop_duplicates(inplace = True)
stats.append(df['Class'].value_counts()) 
 
X = df.drop("Class", axis=1) 
y = df['Class'] 
  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
stats.append([X_train.shape, X_test.shape] )
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
 
param_grid = { 
    'n_estimators': [ 50, 100], 
    'max_features': ['sqrt', 'log2', None], 
    'max_depth': [ 6, 9], 
} 
# grid_search = GridSearchCV(RandomForestClassifier(n_jobs=-1, random_state=42), 
#                            param_grid=param_grid) 
# grid_search.fit(X_train, y_train) 
# print(grid_search.best_estimator_) 
random_search = RandomizedSearchCV(RandomForestClassifier(n_jobs=1, random_state=42), 
                                   param_grid) 
random_search.fit(X_train, y_train) 
print(random_search.best_estimator_) 
estimate=random_search.best_estimator_
estimate.to_csv("estimate.csv", index=False)
#print(classification_report(y_pred,y_test)) 
print(stats)
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start

# Print the result
print(f"Execution time: {elapsed_time:.2f} seconds")