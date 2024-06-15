import numpy as np
from numpy import inf

# Problem definition

# Distance matrix
d = np.array([[np.inf, 1, 2.2, 2, 4.1],
                      [1, np.inf, 1.4, 2.2, 4],
                      [2.2, 1.4, np.inf, 2.2, 3.2],
                      [2, 2.2, 2.2, np.inf, 2.2],
                      [4.1, 4, 3.2, 2.2, np.inf]])

max_it = 1000 # max iterations
m = 10 # number of ants
n = len(d) # number of cities
e = 0.5 # evaporation rate
alpha = 0.5 # pheromone factor
beta = 0.5 # heuristic information factor

h =  1/d # η(i,j) = 1/d(i,j), heuristic matrix
h[h == inf] = 0 # if η(i,j) is infinite, assumes 0

# pheromone matrix initialized with random values 
tRandom = np.random.rand(n,n)
t = (tRandom + tRandom.T)/2
np.fill_diagonal(t, 0.1) 
#print(t)

route = np.ones((m,n+1))

for it in range(max_it):

    route[:,0] = 1 # every ant will start at city 1

    for i in range(m-1):

        temp_h = np.array(h) # buffer heuristic matrix

        for j in range(n-1):
            phi = np.zeros(5) # initialize phi array
            sumProb = np.zeros(5) # initialize commulative probability array

            cur_loc = int(route[i,j]-1) # current city

            temp_h[:,cur_loc] = 0

            # Φ calculation
            phiB = np.power(t[cur_loc, :], beta)
            phiA = np.power(temp_h[cur_loc, :], alpha)

            phi = phiB * phiA
            sumPhi = np.sum(phi)

            # Probability of travel
            prob = phi / sumPhi
            sumProb = np.cumsum(prob)

            random = np.random.random_sample() # generate random number [0,1)
            city = np.nonzero(sumProb>random)[0][0]+1   # first true value for sumProb>random vector defined as next city
            route[i, j+1] = city 

        lastCity = list(set([i for i in range(1, n+1)]) - set(route[i,:-2]))[0]

        route[i,-2] = lastCity

    routeOpt = np.array(route)
    costs = np.zeros((m,1))

    for i in range(m):
        s = 0
        for j in range(n):
            s = s + d[int(routeOpt[i,j])-1, int(routeOpt[i, j+1])-1]

        costs[i] = s
    dist_min_loc = np.argmin(costs) 
    dist_min_cost = costs[dist_min_loc]

    bestRoute = route[dist_min_loc,:]
    t = (1-e)*t

    for i in range(m):
        for j in range(n-1):
            dt = 1/costs[i]
            t[int(routeOpt[i,j])-1, int(routeOpt[i, j+1])-1] = t[int(routeOpt[i,j])-1, int(routeOpt[i,j+1])-1]+dt

print('route of all the ants at the end :')
print(routeOpt)
print('best path :',bestRoute)
s = 0
for i in range(n):
    s = s + d[int(bestRoute[i]-1), int(bestRoute[i+1])-1]
print('cost of the best path', s)