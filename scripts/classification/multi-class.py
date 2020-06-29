import numpy as np
import pandas as pd
import argparse
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV,StratifiedShuffleSplit,cross_validate
from sklearn import metrics
from sklearn.model_selection import train_test_split
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

parser = argparse.ArgumentParser(description="Feature Selection")
parser.add_argument("--input","-i",help="Input matrix",required=True)
parser.add_argument("--features","-f",help="selected features")
parser.add_argument("--scaling","-s",help="sacling",action="store_true",default=False)
parser.add_argument("--performance","-p",help="performance output",required=True)
parser.add_argument("--confusion","-c",help="path of confusion matrix on test set",required=True)
parser.add_argument("--labels","-l",help="label of the samples",required=True)
args = parser.parse_args()

def autoTune(estimator,X,y,params_grid):
    cv = GridSearchCV(estimator, params_grid,scoring='balanced_accuracy',refit=True)
    cv.fit(X,y)
    print(cv.best_params_)
    return cv.best_estimator_


labelPath = args.labels
matPath = args.input

mat = pd.read_csv(matPath,sep="\t",index_col=0)
impute = np.repeat(mat.median(axis=1).values.reshape((-1,1)),mat.shape[1],axis=1)
impute = pd.DataFrame(index=mat.index,columns=mat.columns,data=impute)
mat = mat.fillna(impute)

if args.features is None:
    features = mat.index
else:
    features = pd.read_csv(args.features,sep="\t",header=None).iloc[:,0]


labels = pd.read_csv(labelPath,sep="\t",index_col=0)
label_field = "labels"
labels = labels[~(labels[label_field]=="ESCA")]
labels = labels[~(labels[label_field]=="NC")]

ids_train = labels[labels["dataset"]=="discovery"].index
ids_test =  labels[labels["dataset"]=="validation"].index
label2int = pd.Series({"CRC":0,"STAD":1,"LUAD":2,"HCC":3})

print("{} samples in discovery set".format(len(ids_train)))
sample_ids_train = sorted(list(set(ids_train).intersection(set(mat.columns))))
print("{} samples in the matrix".format(len(sample_ids_train)))
print("{} samples in validation set".format(len(ids_test)))
sample_ids_test = sorted(list(set(ids_test).intersection(set(mat.columns))))
print("{} samples in the matrix".format(len(sample_ids_test)))
sample_ids = sample_ids_train + sample_ids_test

X = mat.T.loc[sample_ids,features].values

if args.scaling:
    X = StandardScaler().fit_transform(X)

X = pd.DataFrame(X,index=sample_ids,columns=features)

X_train = mat.loc[features,sample_ids_train].values.T
y_train = label2int.loc[labels.loc[sample_ids_train,label_field]].values
train_index = np.arange(0,X_train.shape[0])
np.random.shuffle(train_index)
X_train = X_train[train_index,:]
y_train = y_train[train_index]

X_test = mat.loc[features,sample_ids_test].values.T
y_test = label2int.loc[labels.loc[sample_ids_test,label_field]].values
test_index = np.arange(0,X_test.shape[0])
np.random.shuffle(test_index)
X_test = X_test[test_index,:]
y_test = y_test[test_index]
print(sample_ids_train[:10])


def evaluate(X_train,y_train,X_test,y_test):
    clf =  BalancedRandomForestClassifier(n_estimators=500,max_features=None,max_depth=None,random_state=777)
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict_proba(X_test).argsort(axis=1)
    y_pred1 = y_pred[:,-1]
    y_pred2 = y_pred[:,-2]
    return  metrics.confusion_matrix(y_test,y_pred1),metrics.confusion_matrix(y_test,y_pred2)


fields = list(label2int.index) + ["rank"]
records = []

for i in tqdm(range(100)):
    X_train_,y_train_ = resample(X_train,y_train,stratify=y_train)
    c1,c2 = evaluate(X_train_,y_train_,X_test,y_test)
    df1 = pd.DataFrame(data=c1,index=label2int.index,columns=label2int.index)
    df2 = pd.DataFrame(data=c2,index=label2int.index,columns=label2int.index)
    acc1 = df1/df1.sum(axis=1).values.reshape((-1,1))
    acc2 = df2/df2.sum(axis=1).values.reshape((-1,1))
    top1 = list(np.diagonal(acc1.values)) + ["top1"]
    top2 = list(np.diagonal((acc1+acc2).values)) + ["top2"]
    records.append(top1)
    records.append(top2)


c1,c2 = evaluate(X_train,y_train,X_test,y_test)
df1 = pd.DataFrame(data=c1,index=label2int.index,columns=label2int.index)
df2 = pd.DataFrame(data=c2,index=label2int.index,columns=label2int.index)
acc1 = df1/df1.sum(axis=1).values.reshape((-1,1))
acc2 = df2/df2.sum(axis=1).values.reshape((-1,1))
top1 = list(np.diagonal(acc1.values)) + ["top1-all"]
top2 = list(np.diagonal((acc1+acc2).values)) + ["top2-all"]
records.append(top1)
records.append(top2)
print(acc1)

result = pd.DataFrame.from_records(records)
result.columns = fields
result.to_csv(args.performance,index=False,sep="\t")
acc1.to_csv(args.confusion,sep="\t")

