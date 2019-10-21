class SA_FeatureSelection_WrapperMethod_BySelectionSize(SimulatedAnnealing):
    def __init__(self, X_train, y_train, X_test, y_test, subsetSize, wrapperModel, iteration, subIteration, T0, alpha, silent=True):
        self.iteration = iteration
        self.subIteration = subIteration
        self.T0 = T0
        self.alpha = alpha
        self.subsetSize = subsetSize
        self.silent = silent
        self.wrapperModel = wrapperModel
        features = [i + 1 for i in range(0, X_train.shape[1])]
        self.features = features
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.featureSize = len(features)
        self.selected_features = None
        self.max_accuracy = None
        self.best_equal_combinations_set = set()
        super().__init__(iteration, subIteration, T0, alpha, minimization=False,
                         silent=silent)

    def optimize(self):
        super().optimize()
        self.selected_features = sorted(self.bestSolution[:self.subsetSize])
        self.max_accuracy = self.bestObj

    def initial_solution(self):
        sol = np.random.permutation(self.features).tolist()
        return sol

    def objective_function(self, sol):
        permutation = sol
        selected_features = permutation[:self.subsetSize]
        X_train, y_train, X_test, y_test = self.feature_selected(self.X_train, self.y_train, self.X_test,
                                                                    self.y_test, selected_features)
        obj = self.accuracy_calc(X_train, y_train, X_test, y_test, self.wrapperModel)
        return obj

    def get_neighbor(self, sol):
        r = np.random.randint(0, len(sol), 2)
        while r[0] == r[1]:
            r = np.random.randint(0, len(sol), 2)
        g0 = sol[r[0]]
        g1 = sol[r[1]]
        sol[r[0]] = g1
        sol[r[1]] = g0
        return sol

    def feature_selected(self, X_train, y_train, X_test, y_test, selected):
	features = [i + 1 for i in range(0, X_train.shape[1])]
	mask = [i - 1 for i in features if i in selected]
	X_train = X_train[:, mask]
	y_train = y_train
	X_test = X_test[:, mask]
	y_test = y_test
	return X_train, y_train, X_test, y_test

