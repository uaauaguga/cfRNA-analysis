from utils import *
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV,StratifiedShuffleSplit,cross_validate,StratifiedKFold
import argparse
import pickle
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.utils import resample

parser = argparse.ArgumentParser(description="Cross Validation")
parser.add_argument("--input","-i",help="Input matrix",required=True)
parser.add_argument("--labels","-l",help="label of the samples",required=True)
parser.add_argument("--pos","-p",help="positive class",required=True)
parser.add_argument("--neg","-n",help="negative class",required=True)
parser.add_argument("--label_field","-lf",help="which field in the covariate table to use as label",default="labels")
parser.add_argument("--features","-f",help="selected features",required=True)
parser.add_argument("--probability","-proba",help="predicted probability",required=True)
parser.add_argument("--roc",help="path of testing roc curve",required=True)
parser.add_argument("--auroc","-auc",help="AUROC",required=True)
args = parser.parse_args()



def autoTune(estimator,X,y,params_grid):
    cv = GridSearchCV(estimator, params_grid,scoring='roc_auc',refit=True,cv=StratifiedKFold(shuffle=True,random_state=777))
    cv.fit(X,y)
    print(cv.best_params_)
    return cv.best_estimator_

print("Load data ...")
labelPath = args.labels
matPath = args.input
mat = pd.read_csv(matPath,sep="\t",index_col=0).fillna(0)
impute = np.repeat(mat.median(axis=1).values.reshape((-1,1)),mat.shape[1],axis=1)
impute = pd.DataFrame(index=mat.index,columns=mat.columns,data=impute)
mat = mat.fillna(impute)

labels = pd.read_csv(labelPath,sep="\t",index_col=0)
label_field = args.label_field
pos_classes = args.pos.strip().split(",")
neg_classes = args.neg.strip().split(",")

sample_ids = set(labels.index).intersection(mat.columns)
labels = labels.loc[sample_ids,:]

pos = labels.apply(lambda x:x.loc[label_field] in pos_classes,axis=1)
neg = labels.apply(lambda x:x.loc[label_field] in neg_classes,axis=1)
discovery = labels["dataset"]=="discovery"
validation = labels["dataset"]=="validation"


pos_ids_train = sorted(list(labels[(pos&discovery)].index))
pos_ids_test = sorted(list(labels[(pos&validation)].index))
neg_ids_train = sorted(list(labels[(neg&discovery)].index))
neg_ids_test = sorted(list(labels[(neg&validation)].index))

sample_ids = pos_ids_train + pos_ids_test + neg_ids_train + neg_ids_test

features = []
with open(args.features) as f:
    for line in f:
        if len(line.strip())>0:
            features.append(line.strip())

X = mat.T.loc[sample_ids,features]

X_train = X.loc[pos_ids_train+neg_ids_train,:].values
y_train = np.array([1]*len(pos_ids_train)+[0]*len(neg_ids_train))
X_test = X.loc[pos_ids_test+neg_ids_test,:].values
y_test = np.array([1]*len(pos_ids_test)+[0]*len(neg_ids_test))

print(pos_ids_test[:4])
print(neg_ids_test[:4])
print(X_test[:4,:])

clf2 = BalancedRandomForestClassifier(n_estimators=100,random_state=777)  #666
grid = {"max_depth":[2,4,8,16,None]}
clf2 = autoTune(clf2,X_train,y_train,grid) 
#y_pred = clf2.predict_proba(X.values)[:,1]
prob = pd.DataFrame(index=sample_ids,columns=["probability","dataset"])
prob.loc[pos_ids_test+neg_ids_test,"probability"]=clf2.predict_proba(X_test)[:,1]
prob.loc[pos_ids_train+neg_ids_train,"probability"]=clf2.predict_proba(X_train)[:,1]
prob.loc[pos_ids_train+neg_ids_train,"dataset"]="train"
prob.loc[pos_ids_test+neg_ids_test,"dataset"]="test"
prob.to_csv(args.probability,sep="\t")
y_pred = prob.loc[pos_ids_test+neg_ids_test,"probability"]
print("ROC-AUC on test set")
print("full-training-set\ttest_set\t{}".format(metrics.roc_auc_score(y_test,y_pred)),sep="\t")
auroc=metrics.roc_auc_score(y_test,y_pred)
with open(args.auroc,"w") as f:
    f.write(str(auroc))
fpr, tpr, thresholds = metrics.roc_curve(y_test,y_pred)
roc_data = {}
roc_data["fpr"] = fpr
roc_data["tpr"] = tpr
roc_data["thresholds"] = thresholds
pd.DataFrame(roc_data).to_csv(args.roc,index=False,sep="\t")

