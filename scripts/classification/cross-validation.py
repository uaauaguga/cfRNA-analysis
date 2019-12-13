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


parser = argparse.ArgumentParser(description="Feature Selection")
parser.add_argument("--input","-i",help="Input matrix",required=True)
parser.add_argument("--feature","-f",help="selected features",required=True)
parser.add_argument("--pos_ids","-p",help="positive sample ids",required=True)
parser.add_argument("--neg_ids","-n",help="negative sample ids",required=True)
parser.add_argument("--output","-o",help="output of fpr-tpr")
#parser.add_argument("--classifier","-c",choices=["SVM","RF"],help="Method for classification",default="SVM")

args = parser.parse_args()


def loo_ROC(X,y,outpath):
    pre_y = np.zeros(y.shape)
    loo = LeaveOneOut()
    for train_index,test_index in tqdm(loo.split(X)):
        X_train, y_train = X[train_index],y[train_index]
        #clf = SVC(gamma='auto',probability=True)
        clf = RandomForestClassifier()
        #clf = LogisticRegression()
        clf.fit(X_train, y_train)
        pre_y[test_index] = clf.predict_proba(X[test_index])[:, 1]
    fpr, tpr, thresholds = metrics.roc_curve(y, pre_y)
    fpr = fpr.reshape(-1,1)
    tpr = tpr.reshape(-1,1)
    thresholds = thresholds.reshape(-1,1)
    result = np.hstack([fpr,tpr,thresholds])
    result = pd.DataFrame(result,columns=["fpr","tpr","threshold"])
    result.to_csv(outpath,sep="\t",index=False)

mat = pd.read_csv(args.input,sep="\t",index_col=0)
features = pd.read_csv(args.feature,sep="\t",header=None).iloc[:10,0]

pos_ids = open(args.pos_ids).read().split("\n")
neg_ids = open(args.neg_ids).read().split("\n")
pos_ids = list(set(pos_ids).intersection(set(mat.columns)))
neg_ids = list(set(neg_ids).intersection(set(mat.columns)))
sample_ids = pos_ids + neg_ids
#mat = mat.loc[features,sample_ids]
X = mat.T.loc[sample_ids,features].values
X = StandardScaler().fit_transform(X)
y = np.array(len(pos_ids)*[1] + len(neg_ids)*[0])
loo_ROC(X,y,args.output)







