import numpy as np
import math
import test
import argparse

_S_ = list()
_T_ = list()
_N_ = list()
_Q_ = list()
_W_ = list()

# n个里面选k个
def C(k, n):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n-k))

def S(n):
    # n >= 0
    if(n <= 1):
        return 0
    if(n == 2):
        return 1
    
    if(_S_[n] != -1):
        return _S_[n]
    else:
        _S_[n] = (n-1)*(S(n-1) + S(n-2))
        return _S_[n]

def T(n, m):
    # n > 0, m > 0, m >= n
    if(n == m):
        if(n == 0):
            _T_[0][0] = 1
            return 1
        _T_[n][n] = S(n)
        return _T_[n][n]
    
    # math.factorial(k) = k!
    if(_T_[n][m] != -1):
        #print(n, m, _T_[n][m])
        return _T_[n][m]
    else:
        sumT = 0
        max_k = min(n, m-n)
        for k in range(max_k):
            sumT = sumT + T(n, n+k) * T(m-n, m-n+k)
        _T_[n][m] = (T(m, m) - sumT) / math.factorial(m-n)

        return _T_[n][m]

# i : 已经碰撞了几次，问题变成总共 m-i 个符号，分为左边 n-i 个符号和右边 m-n 个符号
def N(n, m, i):
    if(_N_[i] != -1):
        return _N_[i]
    else:
        sum = 0
        # max_k : 最多能向左边放入多少个符号
        max_k = min(n-i, m-n)
        for k in range(1 + max_k):
            # C(k, m-n) : 从右边 m-n 个符号中选取 k 个符号有多少种可能
            # T(n-i, n-i+k) : ...
            sum = sum + C(k, m-n) * T(n-i, n-i+k)
        _N_[i] = sum
        return _N_[i]

# 碰撞限制在某 i 项中时，t+1 条数列碰撞次数小于等于 i 次的概率
def Q(n, m, t, i):
    if(_Q_[i] != -1):
        return _Q_[i]
    else:
        sum = 0
        max_i = i
        for z in range(1 + max_i):
            sum = sum + C(z, i) * N(n, m, z)
        _Q_[i] = (sum / (math.factorial(m) / math.factorial(m-n))) ** t
        return _Q_[i]

def W(n, m, t, i):
    if(i == 0):
        if(_W_[0] != -1):
            return _W_[0]
        else:
            _W_[0] = Q(n, m, t, 0)
            return _W_[0]
    
    if(_W_[i] != -1):
        return _W_[i]
    else:
        _W_[i] = Q(n, m, t, i)
        for z in range(i):
            _W_[i] = _W_[i] - C(z, i) * W(n, m, t, z)
        return _W_[i]

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, default=0)
    parser.add_argument('m', type=int, default=0)
    parser.add_argument('t', type=int, default=0)
    args = parser.parse_args()

    n = args.n
    m = args.m
    t = args.t
    
    _S_ = list(-1 for i in range(m+1))
    _T_ = [list(-1 for i in range(m+1)) for j in range(m+1)]
    _N_ = list(-1 for i in range(m+1))
    _Q_ = list(-1 for i in range(m+1))
    _W_ = list(-1 for i in range(m+1))

    print("n =", n)
    print("m =", m)
    print(t+1, "条数列")
    print("\n理论值:")

    # i : 碰撞次数
    for i in range(n+1):
        if (m < n or n <= 0 or m <= 0):
            print("wrong input")
        else:   
            prob = C(i, n) * W(n, m, t, i) 
            print("碰撞次数等于", i, "的概率:", prob)
    
    print("\n仿真结果:")
    test.simulate(n, m, t, i)


        