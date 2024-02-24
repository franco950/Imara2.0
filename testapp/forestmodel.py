import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import classification_report 
from sklearn.model_selection import train_test_split 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV 
import time
import os

import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix, recall_score, f1_score
# loaded_model = joblib.load('trained_model  with smote, Time feature removed.joblib')
# feature_importance = loaded_model.feature_importances_
# print(feature_importance)
# #assert len(X_train.columns) == len(model.feature_importances_)
# feature_names = [ 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
# 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
# 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount'] 
# plt.bar(feature_names,feature_importance)
# plt.xlabel('Feature names')
# plt.ylabel('Feature importance')
# plt.show()
start=time.time()
stats=[]
csv_file_path='creditcard.csv'
df=pd.read_csv(csv_file_path)
df.drop_duplicates(inplace = True)
#dc=df.drop('Class',axis=1)
print(len(df))
# sns.pairplot(df)
# plt.show()
z_scores_all_features = (df - df.mean()) / df.std()
outliers_all_features = (z_scores_all_features.abs() > 50).any(axis=1)
dnew = df[outliers_all_features]
print(len(dnew))
merged_df = pd.merge(df, dnew, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']

# Drop the '_merge' column
df = merged_df.drop('_merge', axis=1)
print(len(df))
# sns.histplot(df, kde=True)
# plt.show()
#print(data_outliers)
# z_scores = pd.Series((df - df.mean()) / df.std())
# outliers = df[df[z_scores.abs() > 3]]
#print(outliers)
stats.append(df['Class'].value_counts()) 
print(stats)
dropped='none'#'Time'#, 'V22','V23','V24'
#df=df.drop('Time',axis=1)
# # df=df.drop('V24',axis=1)
# # df=df.drop('V22', axis=1)
# # df=df.drop('V23', axis=1)
X = df.drop("Class", axis=1) 
y = df['Class'] 
test_size=0.25
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
new=pd.Series(y_train_smote).value_counts()

stats.append(['training and test data size: ',X_train.shape, X_test.shape] )
stats.append(['\n training count after SMOTE: ',new])
stats.append(['\n dropped features: ',dropped])


# plus=X_test
# plus['Class']=y_test
# nw=plus[plus['Class']==1]
# ai=plus[plus['Class']==0]
# nws=nw
# print(nws.head())
# nws=nws.drop('Class',axis=1)
# nws['predicted']=loaded_model.predict(nws)
# nwa=nws[nws['predicted']==0]
# print(nwa.head())
# cot=(nws.corr()['predicted'])
# print(cot)
# #sns.barplot(x=cot.index, y=cot.values)

# plt.scatter(nwa['predicted'], nwa['V14'],s=1, color='r')
# plt.scatter(ai['Class'], ai['V14'],s=1, color='g')
# plt.show()
# plt.clf()


# Save the dataframe as a csv file
#X_test.to_csv("testdata0.25.csv", index=False)

# performance evaluation metrics 
 
# param_grid = { 
#     'n_estimators': [50],  
#     'max_depth': [39]} 

# rf_model = RandomForestClassifier(n_jobs=-1,random_state=42, class_weight='balanced')
# grid_search = GridSearchCV(rf_model,scoring='f1', param_grid=param_grid) 
# grid_search.fit(X_train, y_train) 
# end_time = time.time()
# results_df = pd.DataFrame(grid_search.cv_results_)


# # Calculate the elapsed time
# elapsed_time = end_time - start

# # Print the result
# results_df['test_size']=test_size
# results_df['execution_time_seconds'] = elapsed_time
# # Save the results to a CSV file
# results_df.to_csv('grid_search_results.csv', mode='a', header=not os.path.isfile('grid_search_results.csv'), index=False)


# print(grid_search.best_params_) 
# print(f"Execution time: {elapsed_time:.2f} seconds")

rf_model = RandomForestClassifier(n_jobs=-1,random_state=42)
rf_model.fit(X_train_smote, y_train_smote) 
feature_importance=rf_model.feature_importances_
end_time = time.time()
# # Calculate the elapsed time
max_depths = [estimator.tree_.max_depth for estimator in rf_model.estimators_]
max_depth_used = max(max_depths)

print(f"Highest Maximum Depth Used: {max_depth_used}")
elapsed_time = end_time - start
joblib.dump(rf_model, 'trained_model  with smote,11 outliers removed.joblib')
prediction=rf_model.predict(X_test)
report = classification_report(y_test, prediction)
print(report)
matrix = confusion_matrix(y_test, prediction)
print(matrix)
accuracy=accuracy_score(y_test,prediction)
# # Save the results to a CSV file
conf_matrix_df = pd.DataFrame(matrix, columns=['Predicted 0', 'Predicted 1'], index=['Actual 0', 'Actual 1'])

# Save both classification report and confusion matrix to a single text file
with open('classification_and_confusion with smote, 11 outliers removed.txt', 'w') as report_file:
        
    report_file.write(" Training time:\n")
    report_file.write(f"{elapsed_time} seconds ({elapsed_time/60} minutes)\n\n")

    report_file.write(" Accuracy:\n")
    report_file.write(f"{accuracy}\n\n")

    report_file.write(" depth:\n")
    report_file.write(f"{max_depth_used}\n\n")

    report_file.write(" feature importance:\n")
    report_file.write(f"{feature_importance}\n\n")

    report_file.write(" Statistics:\n")
    report_file.write(f"{stats}\n\n")

    report_file.write(" Classification Report:\n")
    report_file.write(f"{report}\n\n")

    report_file.write(" Confusion Matrix:\n")
    report_file.write(f"{conf_matrix_df.to_string()}\n")