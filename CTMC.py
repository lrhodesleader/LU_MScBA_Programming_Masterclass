# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:52:10 2022

@author: rhodesle
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def CTMC(horizon, initial_state, generator, dt = 0.01):
    """
    A function to numerically integrate a continuous time Markov chain.

    Parameters
    ----------
    horizon : float
        Length of the time horizon of interest.
    initial_state : numpy.matrix
        The probabilities of being in each state at time zero.
    generator : numpy.matrix
        The gernator matrix for the process.
    dt : float, optional
        The time step used by the numerical integration. The default is 0.01.

    Returns
    -------
    trace : pandas.DataFrame
        A data frame of how the state probabilities evolve over time.

    """
    # number of states 
    n = initial_state.shape[1]
    
    # create discrete-time transition matrix
    transition_matrix = dt*generator + np.eye(n)
    # check step is small enough
    for i in range(n):
        if transition_matrix[i,i] < 0:
            error = "Q["+str(i)+","+str(i)+"] = %.3f" % transition_matrix[i,i]
            raise Exception(error+"\nTime step too big.")
    
    # output for the function
    trace = {i : [initial_state[0,i]] for i in range(initial_state.shape[1])}

    # set the time to 0
    t = 0
    
    while t<=horizon:
        # update state probabilities
        initial_state = np.dot(initial_state,transition_matrix)
        # update time
        t += dt
        
        # store new state in trace
        store_probs(trace, initial_state)
     
    trace = pd.DataFrame(trace)
    
    # add time to the output
    trace['Time'] = [dt*i for i in range(len(trace[0]))]

    return(trace)

def store_probs(store, current_probabilities):
    """
    A function to store the current state probabilities.

    Parameters
    ----------
    store : dictionary
        Where we wan to store the values.
    current_probabilities : numpy.matrix
        The probabilities of being in each state.

    """
    # number of states 
    n = current_probabilities.shape[1]

    # store new state in trace
    for i in range(n):
        store[i].append(current_probabilities[0,0])

# try it out
Q = np.matrix([[-3,1.5,1.5],
               [0,-2,2],
               [1,0.5,-1.5]])
p = np.matrix([1,0,0])

X = CTMC(1,p,Q)
X.plot(x='Time')
plt.show()