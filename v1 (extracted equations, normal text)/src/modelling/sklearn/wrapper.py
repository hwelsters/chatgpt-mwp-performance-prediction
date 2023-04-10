from sklearn.model_selection import GridSearchCV

class SklearnHelper(object):
    def __init__(self, clf, seed=0, params={}):
        self.clf = clf
        self.params = params

    def fit(self, x_train, y_train):
        self.fitted = self.clf(**self.params).fit(x_train, y_train)
    
    def predict(self, x):
        return self.fitted.predict(x)
    
    def tune(self, x_train, y_train, params=None):
        
        grid = GridSearchCV(self.clf(), param_grid=params)
        grid.fit(x_train, y_train)

        self.params = grid.best_params_

        print(self.params)
        pass