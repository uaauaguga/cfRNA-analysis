import numpy as np
from copy import copy
import pandas as pd
from sklearn.utils.validation import check_X_y,check_is_fitted
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels
from imblearn.ensemble import BalancedRandomForestClassifier
from collections import defaultdict
from scipy.stats import ranksums 
from skrebate import SURF

def relief(X,y):
    np.random.seed(0)
    return SURF().fit(X,y).feature_importances_

def ranksum(X,y):
    pvalue = []
    X0,X1 = X[y==0],X[y==1]
    for i in range(X.shape[1]):
        _,p = ranksums(X0[:,i],X1[:,i])
        pvalue.append(p)
    return -np.log(np.array(pvalue))

class BalancedBinaryClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self,max_depth=None,n_features=10,selector=ranksum,trend="both",space_mask=None):
        self.max_depth = max_depth
        self.n_features = n_features
        self.selector = selector
        self.model_ = BalancedRandomForestClassifier(max_depth=max_depth,n_estimators=100,random_state=777)
        self.trend = trend
        self.space_mask = space_mask 
    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.mask = self.trend_mask =  np.zeros(X.shape[1])
        self.classes_ = unique_labels(y)
        if self.classes_.shape[0] != 2:
            raise Exception('Current implementation only support binary classification')
        self.importance = self.selector(X,y)
        flag1 = flag2 = False
        mean_diff = X[y==1,:].mean(axis=0)-X[y==0,:].mean(axis=0)
        if self.trend == "up":
            flag1 = True
            self.trend_mask[mean_diff<=0] = 1
            print("Trend mask: {}/{}".format(int(self.trend_mask.sum()),X.shape[1]))
        if self.space_mask is not None:
            flag2 = True
            self.space_mask =  np.array(self.space_mask).astype(int)
            print("Space mask: {}/{}".format(int(self.space_mask.sum()),X.shape[1]))
        else:
            self.space_mask = np.zeros(X.shape[1])
        if flag1 or flag2:
            self.mask = self.trend_mask + self.space_mask
            self.mask[self.mask>1] = 1 
            print("Remained: {}/{}".format(X.shape[1]-int(self.mask.sum()),X.shape[1]))
            self.importance[self.mask.astype(bool)] = self.importance.min()-1
        if self.trend == "both_balance":
            n_up = int(self.n_features/2)
            n_down = self.n_features - n_up
            up_importance = copy(self.importance)
            down_importance = copy(self.importance)
            up_importance[mean_diff<0] = up_importance.min()-1
            down_importance[mean_diff>0] = down_importance.min()-1
            up_order = np.argsort(up_importance)[::-1]
            down_order = np.argsort(down_importance)[::-1]
            features = np.array(list(up_order[:n_up]) + list(down_order[:n_down]))
            print(features)
        else:
            order = np.argsort(self.importance)[::-1]
            features = order[:self.n_features]
        self.features = features
        self.model_.fit(X[:,self.features],y)
        
    def predict(self, X):
        check_is_fitted(self)
        return self.model_.predict(X[:,self.features])
    
    def predict_proba(self, X):
        check_is_fitted(self)
        return self.model_.predict_proba(X[:,self.features])



