import time
#start=time.time()
import numpy as np
import pandas as pd
import joblib
from testapp import models
import json
import random

loaded_model = joblib.load('trained_model.joblib')
df=pd.read_csv('testdata.csv')

def prediction(data):
    return loaded_model.predict(data)

df=df[df.columns[:-1]]
transactiondf=df.copy()
transactions=transactiondf[transactiondf['Class']==1]
transactions=transactions[transactions.columns[:-1]]
fraud=transactions.copy()
def locations():
    list=['Kiambu01','Kiambu02','Online01','Thika01','Thika02','Online02']
    choice=random.sample(list,1)
    for item in choice:
        return item
def gendata(num):
    first=fraud.iloc[num]
    each=first.values.tolist()
    finall=json.dumps(each)[1:-1]
    new_entry = models.transaction.objects.create( location=locations(),transaction_data=finall)
    return new_entry.save()

def always(number):
    results = {}
    x = 1
    while x < number:
        results[x] = gendata(x)
        x += 1
    return results