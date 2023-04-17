# Import libraries
import numpy as np
import math


class Error:
    def angleDifference(self, a1, a2):
        sign = 1 if a1 > a2 else -1
        angle = a1 - a2
        K = -sign * math.pi * 2
        return K + angle if (abs(K + angle) < abs(angle)) else angle
        

    def pointDistance(self, truth, predict):
        diff = np.subtract(truth, predict) # Points difference x2 - x1, y2 - y1
        # print(truth[0:2], ' - ', predict[0:2], ' = ' , diff[0:2])
        # print ('square() = ',  np.square(diff[0:2]))
        # print ('sum() = ',  np.sum(np.square(diff[0:2]), axis=1, keepdims=True))
        # print('mean() = ', np.sum(np.square(diff[0:2]), axis=1, keepdims=True).mean())
        return np.sum(np.square(diff), axis=1, keepdims=True) #  Components sum (x^2 + y^2) 
    
    def MSE(self, truth, predict):
        return self.pointDistance(truth, predict).mean() # Square supressed by missing distance sqrt
    
    def RMSE(self, truth, predict):
        return np.sqrt(self.MSE(truth, predict))