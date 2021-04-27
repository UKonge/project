# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:33:29 2021

@author: Utkarsh
"""

'''
r = max(get_reps(means,5,h,conf=0.95))
r = int(r)
means = []
for i in range(r):
    month = 1
    td = get_interDemand_time()
    to = np.inf
    to1 = np.inf
    inv = 50
    b = 0
    cost = 0
    M = 50
    L = 30
    N = 112
    order = 0
    order1 = 0
    T = []
    E = []
    costs = []
    D = []
    INV = []
    Os = []
    Tos = []
    while month <= N:
        if min(month,td,to,to1) == month:
            te = month
            month = month+1
            Tos.append((month,order,to))
            I = inv + order + order1
            if I < L and I > 0:
                l = get_leadtime()
                if order == 0:
                    to = te + l
                    order = M-I
                else:
                    to1 = te + l
                    order1 = M-I
                cost = cost+(M-I)*5+60
            if I <= 0:
                l = get_rush_leadtime()
                if order == 0:
                    to = te + l
                    order = M-I
                else:
                    to1 = te + l
                    order1 = M-I
                cost = cost + (M-I)*12+120
            T.append(te)
            E.append('M')
            costs.append(cost+max(inv,0) + 4*b)
            cost = 0
            b = 0
        elif min(month,to,td,to1) == to:
            te = to
            inv = inv + order
            Os.append((order,month,to))
            order = 0
            T.append(te)
            E.append('OD')
            to = np.inf
        elif min(month,to,td,to1) == to1:
            te = to1
            inv = inv + order1
            Os.append((order1,month,to1))
            order1 = 0
            T.append(te)
            E.append('OD')
            to1 = np.inf
        elif min(month,to,td,to1) == td:
            te = td
            td = td + get_interDemand_time()
            d = get_demand()
            D.append(d)
            if inv <= 0:
                b += d
            elif inv-d < 0:
                b += d-inv
            inv = inv - d
            T.append(te)
            E.append('C')
        INV.append(inv)
        
    c = np.array(costs[12:])
    means.append(np.mean(c))

print("For 330 replications, mean monthly cost = ",np.mean(means))
h = get_halfwidth(means)
print("The half width for 330 replications is = ",h)
'''

"""
Continuous review model:
Events here will be:
    1. Recieving of the order
    2. Time of customer demand
"""

from funcs import *
import pandas as pd


orders_T = []
orders_Q = []
tc = get_interDemand_time()
to = np.inf
q = 0
te = tc
b = 0
inv = 50
L = 30
M = 50
ind = 0
I = 0
debug_data = pd.DataFrame(data=None,columns=['Te','Inv','EType','lenT','lenQ','Demand/Q','orderType','delivery_time','I'],index=range(5000))
while tc <= 112:
    if min(tc,to) == tc:
        te = tc
        d = get_demand()
        if inv-d <= 0 and inv > 0:
            b += d-inv
        elif inv <= 0:
            b += d
        inv = inv-d
        I = inv+sum(i for i in orders_Q)
        debug_data.loc[ind,'orderType'] = '-1'
        debug_data.loc[ind,'delivery_time'] = -1
        if I <= L-1 and I > 0:
            x = te+get_leadtime()
            orders_T.append(x)
            orders_Q.append(M-I)
            minpos = orders_T.index(min(orders_T))
            to = orders_T[minpos]
            q = orders_Q[minpos]
            debug_data.loc[ind,'orderType'] = 'N'
            debug_data.loc[ind,'delivery_time'] = x
            # add cost
        elif I <= 0:
            x = te+get_rush_leadtime()
            orders_T.append(x)
            orders_Q.append(M-I)
            minpos = orders_T.index(min(orders_T))
            to = orders_T[minpos]
            q = orders_Q[minpos]
            debug_data.loc[ind,'orderType'] = 'R'
            debug_data.loc[ind,'delivery_time'] = x
            # add cost
        tc = te + get_interDemand_time()
        debug_data.loc[ind,'Te'] = te
        debug_data.loc[ind,'Inv'] = inv
        debug_data.loc[ind,'EType'] = 'C'
        debug_data.loc[ind,'lenT'] = len(orders_T)
        debug_data.loc[ind,'lenQ'] = len(orders_Q)
        debug_data.loc[ind,'Demand/Q'] = d
        debug_data.loc[ind,'I'] = I
        ind += 1
    if min(tc,to) == to:
        te = to
        inv = inv + q
        orders_T.remove(to)
        orders_Q.remove(q)
        debug_data.loc[ind,'Te'] = te
        debug_data.loc[ind,'Inv'] = inv
        debug_data.loc[ind,'EType'] = 'D'
        debug_data.loc[ind,'lenT'] = len(orders_T)
        debug_data.loc[ind,'lenQ'] = len(orders_Q)
        debug_data.loc[ind,'Demand/Q'] = q
        debug_data.loc[ind,'orderType'] = '-1'
        debug_data.loc[ind,'delivery_time'] = -1
        debug_data.loc[ind,'I'] = I
        if len(orders_T) == 0:
            to = np.inf
            q = 0
        else:
            minpos = orders_T.index(min(orders_T))
            to = orders_T[minpos]
            q = orders_Q[minpos]
        ind += 1

debug_data = debug_data.dropna()






