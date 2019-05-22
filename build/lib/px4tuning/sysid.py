import numpy as np
import numpy.linalg as la
from scipy import signal


def arx(na, nb, u, y, nk=0):
    N = np.size(y)
    M = na + nb 

    n_max = np.amax([na, nb + nk])

    phi = np.zeros((N - n_max, M))

    k = 0

    for i in range(0, na):
        phi[:, i] = -y[n_max - i-1:N - i-1]

    for i in range(0, nb):
        phi[:, i+na] = u[n_max - i-nk:N - i-nk]


    y = y[n_max:N]

    R = np.dot(phi.T, phi)
    S = np.dot(phi.T, y)
    theta = la.solve(R, S)

    return [theta]



def armax(na, nb, nc, u, y, nk=0, n=10):
    N = np.size(y)
    M = na + nb
    n_max = np.amax([na, nb + nk, nc])
    phi = np.zeros((N - n_max, M))

    for i in range(0, na):
        phi[:, i] = -y[n_max - i-1:N - i-1]

    for i in range(0, nb):
        phi[:, i+na] = u[n_max - i-nk:N - i-nk]

    y_aux = y[n_max:N]

    R = np.dot(phi.T, phi)
    S = np.dot(phi.T, y_aux)
    theta = la.solve(R, S)
    erro=y-np.append(np.zeros([n_max]), np.dot(phi,theta))
    
    M = na + nb + nc
    phi = np.zeros((N - n_max, M))
    
    for i in range(1, n):
        for i in range(0, na):
            phi[:, i] = -y[n_max - i-1:N - i-1]

        for i in range(0, nb):
            phi[:, i+na] = u[n_max - i-nk:N - i-nk]

        for i in range(0, nc):
            phi[:, i+na+nb] = erro[n_max-i-1:N-i-1]
        
        y_aux = y[n_max:N]
        R = np.dot(phi.T, phi)
        S = np.dot(phi.T, y_aux)
        theta = la.solve(R, S)
        erro=y-np.append(np.zeros([n_max]), np.dot(phi,theta))
    return [theta]

def armax2(na, nb, nc, u, y, nk=0, n=10):
    N = np.size(y)
    n_max = np.amax([na, nb + nk, nc])
    
    for k in range(0,nc+1):
        M = na + nb + k
        phi = np.zeros((N - n_max, M))
        for j in range(1, n):
            for i in range(0, na):
                phi[:, i] = -y[n_max - i-1:N - i-1]
    
            for i in range(0, nb):
                phi[:, i+na] = u[n_max - i-nk:N - i-nk]
    
            for i in range(0, k):
                phi[:, i+na+nb] = erro[n_max-i-1:N-i-1]
            
            y_aux = y[n_max:N]
            R = np.dot(phi.T, phi)
            S = np.dot(phi.T, y_aux)
            thetan = la.solve(R, S)
            
            if (j>1):
                theta=(9*theta+thetan)/10
            else:
                theta=thetan
            
            print(theta)
            erro=y-np.append(np.zeros([n_max]), np.dot(phi,theta))
        
    return [theta]