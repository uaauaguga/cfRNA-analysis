import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from tqdm import tqdm
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import LeaveOneOut
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score


parser = argparse.ArgumentParser(description="Feature Selection")
parser.add_argument("--input","-i",help="Input matrix",required=True)
parser.add_argument("--feature","-f",help="selected features",required=True)
parser.add_argument("--pos_ids_train","-ptr",help="train positive sample ids",required=True)
parser.add_argument("--neg_ids_train","-ntr",help="train negative sample ids",required=True)
parser.add_argument("--pos_ids_test","-pte",help="test positive sample ids",required=True)
parser.add_argument("--neg_ids_test","-nte",help="test negative sample ids",required=True)
parser.add_argument("--single","-s",help="whether evaluate the performance of single feature",action="store_true",default=False)
parser.add_argument("--output","-o",help="output of fpr-tpr")
parser.add_argument("--classifier","-cls",help="classifer utilized",choices=["RandomForest","SVM","LogisticRegression"],default="RandomForest")
args = parser.parse_args()

mat = pd.read_csv(args.input,sep="\t",index_col=0)
features = pd.read_csv(args.feature,sep="\t",header=None).iloc[:10,0]

pos_ids_train = open(args.pos_ids_train).read().split("\n")
neg_ids_train = open(args.neg_ids_train).read().split("\n")
pos_ids_test = open(args.pos_ids_test).read().split("\n")
neg_ids_test = open(args.neg_ids_test).read().split("\n")

#print("{} positive samples and {} negative samples in discovery set".format(len(pos_ids_train),len(neg_ids_train)))
pos_ids_train = list(set(pos_ids_train).intersection(set(mat.columns)))
neg_ids_train = list(set(neg_ids_train).intersection(set(mat.columns)))
#print("{} positive samples and {} negative samples are presented in the matrix".format(len(pos_ids_train),len(neg_ids_train)))
sample_ids_train = pos_ids_train + neg_ids_train

print("{} positive samples and {} negative samples in validation set".format(len(pos_ids_test),len(neg_ids_test)))
pos_ids_test = list(set(pos_ids_test).intersection(set(mat.columns)))
neg_ids_test = list(set(neg_ids_test).intersection(set(mat.columns)))
#print("{} positive samples and {} negative samples are present in the matrix".format(len(pos_ids_test),len(neg_ids_test)))
sample_ids_test = pos_ids_test + neg_ids_test

sample_ids = sample_ids_train + sample_ids_test

X = mat.T.loc[sample_ids,features].values
X = StandardScaler().fit_transform(X)

X = pd.DataFrame(X,index=sample_ids,columns=features)

X_train = X.loc[sample_ids_train,:].values
X_test = X.loc[sample_ids_test,:].values
y_train = np.array(len(pos_ids_train)*[1] + len(neg_ids_train)*[0])
y_test =  np.array(len(pos_ids_test)*[1] + len(neg_ids_test)*[0])


train_index = np.arange(0,X_train.shape[0])
np.random.shuffle(train_index)
X_train = X_train[train_index,:]
y_train = y_train[train_index]

test_index = np.arange(0,X_test.shape[0])
np.random.shuffle(test_index)
X_test = X_test[test_index,:]
y_test = y_test[test_index]


if args.classifier == "SVM":
    clf = SVC(gamma='auto',probability=True)
elif args.classifier == "RandomForest":
    clf = RandomForestClassifier()
elif args.classifier == "LogisticRegression":
    clf = LogisticRegression()
    
if not args.single:
    clf.fit(X_train, y_train)
    #y_pred = clf.predict(X[test_index])[:, 1]
    y_pred = clf.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred)
    auc_score = roc_auc_score(y_test,y_pred)
    print("AUROC:",auc_score)
    fpr = fpr.reshape(-1,1)
    tpr = tpr.reshape(-1,1)
    thresholds = thresholds.reshape(-1,1)
    result = np.hstack([fpr,tpr,thresholds])
    result = pd.DataFrame(result,columns=["fpr","tpr","threshold"])
    result.to_csv(args.output,sep="\t",index=False)
else:
    records =  []
    for i in np.arange(X_train.shape[1]):
        clf = LogisticRegression(solver="lbfgs")
        print(features[i])
        clf.fit(X_train[:,i].reshape((-1,1)),y_train)
        y_pred = clf.predict_proba(X_test[:,i].reshape((-1,1)))[:, 1]
        auc_score = roc_auc_score(y_test,y_pred)
        print("AUROC:",auc_score)
        records.append((features[i],auc_score))
    res = pd.DataFrame.from_records(records)
    res.columns = ["gene-id","auroc"]
    res = res.set_index("gene-id")
    res.to_csv(args.output,sep="\t")
    print(res)


