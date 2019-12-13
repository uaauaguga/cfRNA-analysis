import pandas as pd
import numpy as np
import argparse
from scipy.stats import ranksums
from sklearn.metrics import roc_curve,precision_recall_curve,auc,precision_score,recall_score
from sklearn.svm import SVC,SVR
from sklearn.feature_selection import RFE
from sklearn.model_selection import StratifiedShuffleSplit,ShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Feature Selection")
parser.add_argument("--input","-i",help="Input matrix",required=True)
parser.add_argument("--number","-num",type=int,default=10)
parser.add_argument("--log","-l",help="Selected features in each shuffle",required=True)
parser.add_argument("--feature","-f",help="Finally selected features",required=True)
parser.add_argument("--pos_ids","-p",help="positive sample ids",required=True)
parser.add_argument("--shuffle","-s",help="Number of shuffling in feature selection",type=int,default=10)
parser.add_argument("--neg_ids","-n",help="negative sample ids",required=True)
parser.add_argument("--selector","-se",choices=["ranksum","SVM-RFE"],help="Method for feature selection",default="ranksum")
parser.add_argument("--classifier","-c",choices=["SVM","RF"],help="Method for classification",default="SVM")



args = parser.parse_args()

n_features = args.number
mat_path = args.input
log_path = args.log
feature_path = args.feature
pos_ids = args.pos_ids
neg_ids = args.neg_ids
n_shuffle = args.shuffle
selector = args.selector
classifier = args.classifier

def rankSum(X,y,n):
    pvalue = []
    X0,X1 = X[y==0],X[y==1]
    for i in range(X.shape[1]):
        _,p = ranksums(X0[:,i],X1[:,i])
        pvalue.append(p)
    pvalue = np.array(pvalue)
    return np.argsort(pvalue)[:n]

def SVMRFE(X,y,n):
    estimator = SVR(kernel="linear")
    selector = RFE(estimator,n,step=200)
    selector = selector.fit(X, y)
    print(np.where(selector.ranking_==1)[0])
    return np.where(selector.ranking_==1)[0]
    #return featureINdices

def SVM(X,y):
    return SVC(gamma='auto').fit(X,y)

def logit(X,y):
    return LogisticRegression(solver='lbfgs').fit(X, y)

def RF(X,y):
    return RandomForestClassifier().fit(X,y)

def featureSelection(mat,pos,neg):
    aggregateFeatures = defaultdict(int)
    y = np.array(len(pos)*[1] + len(neg)*[0])
    mat = mat.loc[:,pos+neg]
    features = list(mat.index)
    X = mat.values.T
    X = StandardScaler().fit_transform(X)
    records = []
    if args.selector == "ranksum":
        selectFun = rankSum #SVMRFE #rankSum
    elif args.selector == "SVM-RFE":
        selectFun = SVMRFE
    if args.classifier == "SVM":
        classiFun = SVM
    elif args.classifier == "RF":
        classiFun = RF
    sss = StratifiedShuffleSplit(n_splits=n_shuffle, test_size=0.2)
    for train_index, test_index in tqdm(sss.split(X,y)):
        featureIndices = selectFun(X[train_index,:],y[train_index],n_features)
        X_selected = X[:,featureIndices]
        model = classiFun(X_selected[train_index,:],y[train_index])
        y_pred = model.predict(X_selected[test_index,:])
        y_true = y[test_index]
        recall = recall_score(y_true, y_pred)
        precision = precision_score(y_true,y_pred)
        tp = ((y_true==1)&(y_pred==1)).sum()
        fp = ((y_true==0)&(y_pred==1)).sum()
        tn = ((y_true==0)&(y_pred==0)).sum()
        fn = ((y_true==1)&(y_pred==0)).sum()
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        specificity = tn/(tn+fp)
        for each in np.array(features)[featureIndices]:
            aggregateFeatures[each] += 1
        records.append((precision,recall,specificity,",".join(list(np.array(features)[featureIndices]))))
    finalFeatures = pd.Series(aggregateFeatures).sort_values(ascending=False)
    log = pd.DataFrame.from_records(records)
    log.columns = ["precision","recall","specificity","features"]
    log.to_csv(log_path,index=False,sep="\t")
    finalFeatures.to_csv(feature_path,sep="\t")


def main():
    mat = pd.read_table(mat_path,index_col=0)
    pos = open(pos_ids).read().strip().split("\n")
    neg = open(neg_ids).read().strip().split("\n")
    pos = list(set(pos).intersection(mat.columns))
    neg = list(set(neg).intersection(mat.columns))
    featureSelection(mat,pos,neg) 


if __name__ == "__main__":
    main()





