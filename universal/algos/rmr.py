# -*- coding: utf-8 -*-
from universal.algo import Algo
import universal.tools as tools
import numpy as np
from olmar import OLMAR
import pandas as pd

norm = lambda x: np.sqrt((x**2).sum(axis=1))

class RMR(OLMAR):
    """ Robust Median Reversion. Strategy exploiting mean-reversion by robust 
    L1-median estimator. Practically the same as OLMAR.
    
    Reference:
        Dingjiang Huang, Junlong Zhou, Bin Li, Steven C.H. Hoi, Shuigeng Zhou
        Robust Median Reversion Strategy for On-Line Portfolio Selection, 2013.
        http://ijcai.org/papers13/Papers/IJCAI13-296.pdf
    """

    PRICE_TYPE = 'raw'
    REPLACE_MISSING = True
    
    def __init__(self, window=5, eps=10., tau=0.001):
        """ 
        :param window: Lookback window.
        :param eps: Constraint on return for new weights on last price (average of prices).
            x * w >= eps for new weights w.
        :param tau: Precision for finding median. Recommended value is around 0.001. Strongly
                    affects algo speed.
        """
        super(RMR, self).__init__(window, eps)
        self.tau = tau
        
        
    def predict(self, x, history):
        """ find L1 median to historical prices """
        y = history.mean()
        y_last = None
        while y_last is None or norm(y - y_last) / norm(y_last) > self.tau:
            y_last = y
            d = norm(history - y)
            y = history.div(d, axis=0).sum() / (1. / d).sum()
        return y / x
    

if __name__ == '__main__':
    tools.quickrun(RMR())


