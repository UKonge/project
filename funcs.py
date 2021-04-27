# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:34:37 2021

@author: Utkarsh
"""
import numpy as np
from scipy.stats import t,norm
#np.random.seed(0)

def get_demand():
    u = np.random.uniform()
    if u <= 0.5:
        return 1
    elif u <= 3/4:
        return 2
    elif u <= 7/8:
        return 3
    else:
        return 4

def get_interDemand_time():
    return np.random.exponential(1/15)

def get_leadtime():
    return np.random.uniform(low=0.25,high=1.25)

def get_rush_leadtime():
    return np.random.uniform(low=0.1,high=0.25)

def get_halfwidth(data,conf=0.95):
    h = t.interval(conf,len(data)-1)[1]
    s = np.var(data,ddof=1)**0.5
    return h*s/len(data)**0.5

def get_reps(data,des_h,curr_h,conf=0.95):
    r1 = len(data)*curr_h**2/des_h**2
    z = norm.ppf((1+conf)/2)
    r2 = z*np.var(data,ddof=1)/des_h**2
    return[r1,r2]

def compare_alters(alt1,alt2,conf):
    assert len(alt1) == len(alt2)
    a = np.array(alt1)
    b = np.array(alt2)
    m = a-b
    xbar = np.mean(m)
    hw = get_halfwidth(m,conf)
    r = [xbar-hw,xbar+hw]
    if xbar-hw <= 0 and xbar+hw >= 0:
        return r,0
    elif xbar-hw > 0:
        return r,1
    elif xbar+hw < 0:
        return r,2
    else:
        print("Unthinkable has happened")
        print(r)
        return r,-1

def simulate_Periodic(reps,M,L):
    means = []
    frs = []
    for i in range(reps):
        month = 1
        td = get_interDemand_time()
        to = np.inf
        to1 = np.inf
        inv = 50
        b = 0
        cost = 0
        N = 112
        order = 0
        order1 = 0
        costs = []
        tot_demand = 0
        unsat_demand = 0 
        fill_rates = []
        while month <= N:
            if min(month,td,to,to1) == month:
                te = month
                month = month+1
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
                costs.append(cost+max(inv,0) + 4*b)
                if month > 12:
                    fill_rates.append(1-unsat_demand/tot_demand)
                unsat_demand = 0
                tot_demand = 0
                cost = 0
                b = 0
            elif min(month,to,td,to1) == to:
                te = to
                inv = inv + order
                order = 0
                to = np.inf
            elif min(month,to,td,to1) == to1:
                te = to1
                inv = inv + order1
                order1 = 0
                to1 = np.inf
            elif min(month,to,td,to1) == td:
                te = td
                td = td + get_interDemand_time()
                d = get_demand()
                tot_demand += d
                if inv <= 0:
                    b += d
                    unsat_demand += d
                elif inv-d < 0:
                    b += d-inv
                    unsat_demand += d-inv
                inv = inv - d
        c = np.array(costs[12:])
        means.append(np.mean(c))
        frs.append(np.mean(fill_rates))
    return means,frs