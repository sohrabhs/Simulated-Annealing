import numpy as np

class SimulatedAnnealing():
    def __init__(self, iteration=100, subIteration=10, T0=10, alpha=0.99, minimization=True, silent=True):
        self.minimization = minimization
        self.silent = silent
        self.iteration = iteration
        self.subIteration = subIteration
        self.T0 = T0
        self.T = self.T0
        self.alpha = alpha
        self.objs = [0] * self.iteration
        self.bestSolution = None
        self.bestObj = None

    def sortedFirstBySecond(self, first, second, reverse=False):
        index = np.array(sorted(range(len(second)), key=lambda k: second[k], reverse=reverse))
        second = np.array(sorted(second, reverse=reverse))
        first = np.array(first)
        first = first[index]
        first = first.tolist()
        second = second.tolist()
        return first, second

    def optimize(self):
        self.sol = self.initial_solution()
        self.sol_obj = self.objective_function(self.sol)
        self.bestObj = self.sol_obj
        self.bestSolution = self.sol
        for it in range(self.iteration):
            for subit in range(self.subIteration):
                newSol = self.get_neighbor(self.sol)
                newObj = self.objective_function(newSol)

                if self.minimization:
                    if newObj <= self.sol_obj:
                        self.sol = newSol
                        self.sol_obj = newObj
                    else:
                        delta = (newObj - self.sol_obj) / self.sol_obj
                        p = np.exp(-delta / self.T)
                        if np.random.rand() <= p:
                            self.sol = newSol
                            self.sol_obj = newObj
                    if self.sol_obj <= self.bestObj:
                        self.bestSolution = self.sol
                        self.bestObj = self.sol_obj
                else:
                    if newObj >= self.sol_obj:
                        self.sol = newSol
                        self.sol_obj = newObj
                    else:
                        delta = (newObj - self.sol_obj) / self.sol_obj
                        p = np.exp(delta / self.T)
                        if np.random.rand() <= p:
                            self.sol = newSol
                            self.sol_obj = newObj
                    if self.sol_obj >= self.bestObj:
                        self.bestSolution = self.sol
                        self.bestObj = self.sol_obj

            self.T *= self.alpha
            if not self.silent:
                print("it " + str(it + 1) + " obj =" + str(self.bestObj))

    def selection_roulette_wheel(self, n):
        obj = np.array(self.obj)
        if self.minimization:
            obj = 1 / obj
            pdf = obj / sum(obj)
        else:
            pdf = obj / sum(obj)
        cdf = np.cumsum(pdf)
        selection = []
        for j in range(0, n):
            np.random.seed(None)
            r = np.random.random(1)
            for i in range(0, len(cdf)):
                if r <= cdf[i]:
                    selection.append(i)
                    break
        return selection

    def initial_solution(self):
        pass

    def objective_function(self, sol):
        pass

    def get_neighbor(self, sol):
        pass


