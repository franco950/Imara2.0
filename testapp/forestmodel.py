import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

csv_file_path='mainpage\creditcard.csv'
df=pd.read_csv(csv_file_path)
df.drop_duplicates(inplace = True)
np.random.seed(0)

def features():
    return df.columns[:-1]

df['is_train']=np.random.uniform(0,1,len(df))<=.75
train=df[df['is_train']==True]
test=df[df['is_train']==False]
# Save the dataframe as a csv file
#test.to_csv("sample.csv", index=False)


def sample():
    return test[:5]


y = train['Class']
classifier=RandomForestClassifier(n_jobs=2,random_state=0)
classifier.fit(train[features],y)
joblib.dump(classifier, 'trained_model.joblib')

#prediction=classifier.predict(sample[features])