from modelling.sklearn.wrapper import SklearnHelper

from sklearn.tree import ExtraTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import OneClassSVM
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multioutput import ClassifierChain
from sklearn.multioutput import MultiOutputClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import RidgeClassifierCV
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import GaussianNB
from sklearn.semi_supervised import LabelPropagation
from sklearn.semi_supervised import LabelSpreading
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import NearestCentroid
from sklearn.svm import NuSVC
from sklearn.linear_model import Perceptron
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import SVC

from xgboost import XGBClassifier
import pandas

from modelling.evaluation.cross_validation import cross_validate
from sklearn.preprocessing import StandardScaler


def get_classifier_results(x_data: pandas.DataFrame, y_data: pandas.Series, n_splits: int = 5, random_state: int = 42, shuffle: bool = True):

    def cross_validate_model(classifier):
        return cross_validate(classifier, x_data, y_data, n_splits, random_state, shuffle)

    results_dict = {}

    x_data = pandas.DataFrame(StandardScaler().fit_transform(x_data))

    random_forest = SklearnHelper(RandomForestClassifier)
    gradient_boost = SklearnHelper(GradientBoostingClassifier)
    xg_boost = SklearnHelper(XGBClassifier)
    extra_trees = SklearnHelper(ExtraTreeClassifier)
    decision_tree = SklearnHelper(DecisionTreeClassifier)
    mlp_classifier = SklearnHelper(MLPClassifier)

    random_forest.tune(x_data, y_data, params={
            'n_jobs': [-1],
            'n_estimators': [100, 500, 1000],
            'max_depth': [6, 10, 50],
            'min_samples_leaf': [2, 5, 10],
            'max_features': ['sqrt', 'log2', None],
            'class_weight': ['balanced_subsample', 'balanced'],
            'threshold': [0.4]

            # 'n_jobs': [-1],
            # 'n_estimators': [500],
            # 'warm_start': [True],
            # 'max_depth': [6],
            # 'min_samples_leaf': [2],
            # 'max_features': ['sqrt'],
            # 'verbose': [0], 
            # 'class_weight': ['balanced_subsample'],
            # 'threshold': [0.4]
        }
    )
    gradient_boost.tune(x_data, y_data, params={
            'n_estimators': [100, 500, 1000],
            'max_depth': [3, 10, 50],
            'learning_rate': [0.01, 0.1, 0.3],
            'min_samples_leaf': [2, 5, 10],
            'max_features': ['sqrt'],
            'subsample': [1, 10]

            # 'n_estimators': [500],
            # 'max_depth': [5],
            # 'min_samples_leaf': [2],
            # 'verbose': [0],
            # 'threshold': [0.4]
        }
    )
    xg_boost.tune(x_data, y_data, params={
            'n_jobs': [-1],
            'n_estimators': [100, 500, 1000],
            'max_depth': [3, 10, 50],
            'learning_rate': [0.01, 0.1, 0.3],
            'scale_pos_weight': [(y_data ^ 1).sum() / y_data.sum()]

            # 'n_jobs': [-1],
            # 'n_estimators': [500],
            # 'max_depth': [2],
            # 'scale_pos_weight': [(1 - y_data).sum() / y_data.sum()],
            # 'threshold': [0.4]
        }
    )
    extra_trees.tune(x_data, y_data, params={
            'max_depth': [3, 10, 50],
            'min_samples_leaf': [2, 5, 10],
            'max_features': ['sqrt', 'log2'],
            'class_weight': ['balanced_subsample', 'balanced']

            # 'n_jobs': [-1],
            # 'n_estimators': [500],
            # 'max_depth': [8],
            # 'min_samples_leaf': [2]
            # 'verbose': [0]
            # ,'class_weight': ['balanced'],
            # 'threshold': [0.4]
        }
    )
    decision_tree.tune(x_data, y_data, params={
        'criterion': ['gini', 'entropy', 'log_loss'],
        'splitter': ['best', 'random'],
        'max_depth': [3, 10, 50],
        'max_leaf_nodes': [1, 10, 50, None]
        }
    )

    results_dict.update(
        RandomForestClassifier=cross_validate_model(random_forest))
    results_dict.update(GradientBoostingClassifier=cross_validate_model(
        gradient_boost))
    results_dict.update(XGBClassifier=cross_validate_model(
        xg_boost))
    results_dict.update(ExtraTreeClassifier=cross_validate_model(
        extra_trees))
    results_dict.update(DecisionTreeClassifier=cross_validate_model(
        decision_tree))
    results_dict.update(MLPClassifier=cross_validate_model(
        mlp_classifier))

    return results_dict
