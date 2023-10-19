import numpy as np
import matplotlib.pylab as plt 

# Initialize the given matrix
A = np.zeros((6, 6), dtype=np.int32)
A [0, (1, 2)] = 1
A [1, (2, 3)] = 1
A [2, 0] = 1
A [3, (1, 4)] = 1
A [4, (1, 3, 5)] = 1
A [5, 4] = 1

M = A / np.sum(A, 0)
# Check whether matrix in given requirement
# print(A, "\n\n", M)

def calPageRank(M, alpha):
    r = np.ones(M.shape[0]) / M.shape[0]
    s = r.copy()
    pre_r = alpha * np.dot(M, r) + (1 - alpha) * s
    count = 0

    while np.max(pre_r - r) > 1e-6:
        r = pre_r
        pre_r = alpha * np.dot(M, r) + (1 - alpha) * s
        count += 1
    print(" alpha value:", alpha, "\n", count, "(iterate times)", "\n", pre_r, "\n")
    # return (pre_r, count)

# The following is the requirement output of the task
calPageRank(M, .85)
calPageRank(M, 1)

# Verify the page rank calculating
print("The first column of the eigenvector after normalized:")
eigenVector = np.linalg.eig(M)[1][:,0]
print(eigenVector/sum(eigenVector))