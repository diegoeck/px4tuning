import numpy as np
import vrft
import sysid
from scipy import signal
import matplotlib.pyplot as plt

N=10000

u=np.zeros(N)
u[2]=1
u[202]=1
u[402]=1
u[602]=1
u[802]=1

a0=np.array([1, -1])
b0=np.array([0, 1])
y = signal.lfilter(b0, a0, u) 

# Td
a=0.9
a0=np.array([1, -4*a+2, (2*a-1)*(2*a-1)])
b0=np.array([0, 4*(1-a), -4*(1-a)*a])


r=np.ones(100)
yd = signal.lfilter(b0, a0, r) 

rho=vrft.vrft_pid_mf(u, y, a0,b0,'loco',250)


plt.plot(yd)