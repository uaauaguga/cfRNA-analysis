import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import argparse
from sklearn import metrics

parser = argparse.ArgumentParser(description="Integrating probability of different variations' prediction by logistic regression")
parser.add_argument("--indir","-i",help="Input dir")
parser.add_argument("--variations","-v",help="Variations for integration",default="expression,splicing,APA,editing")
parser.add_argument("--output","-o",help="label of the s",required=True)
args = parser.parse_args()


indir = args.indir
variations = args.variations.strip().split(",")

def getVariations(cancer):
    global indir
    global variations 
    res = {}
    for variation in variations:
        path_t = "{}/{}-{}/prob.txt".format(indir,variation,cancer)
        prob = pd.read_csv(path_t,sep="\t",index_col=0)
        res[variation] = prob["probability"].copy()
    return pd.DataFrame(res),prob["dataset"]

def evaluate(cancer):
    score,dataset = getVariations(cancer)
    train_ids = dataset[dataset=="train"].index
    test_ids = dataset[dataset=="test"].index
    y_train = [int("NC" not in sample_id) for sample_id in train_ids]
    y_test = [int("NC" not in sample_id) for sample_id in test_ids]
    X_train = score.loc[train_ids]
    X_test = score.loc[test_ids]
    clf = LogisticRegression().fit(X_train,y_train)
    y_pred = clf.predict_proba(X_test)[:,1]
    auc_merge_lr = metrics.roc_auc_score(y_test,y_pred)
    return auc_merge_lr

records = []
for cancer in ['CRC','STAD','HCC', 'LUAD','pan-cancer']:
    print("Process {} ...".format(cancer))
    records.append([cancer]+[evaluate(cancer)])
    print("Done .")
df = pd.DataFrame.from_records(records)
df = df.set_index(0)
df.columns = ["Logistic Regression"]
df.index.name = "Cancers"
df.to_csv(args.output,sep="\t")



