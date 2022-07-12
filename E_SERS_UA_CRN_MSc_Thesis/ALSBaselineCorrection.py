import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve


def ALSBaselineCorrection(y, lam=1E6, p=0.0001, niter=30):
    m = len(y)
    w = np.ones(m)
    D = csc_matrix(np.diff(np.eye(m), 3))
    for i in range(niter):
        W = spdiags(w, 0, m, m)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z
