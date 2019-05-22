import numpy as np
import vrft
import sysid
from scipy import signal
import matplotlib.pyplot as plt

N=10000

u=np.zeros(N)
u[2]=1
u[2002]=1
u[4002]=1
u[6002]=1
u[8002]=1

a0=np.array([1, -1.7, 0.72])
b0=np.array([0, 0.04, 0])
c0=np.array([1, -0.3, 0.5])
y = signal.lfilter(b0, a0, u) 
e=np.random.randn(N)/10000*0
v = signal.lfilter(c0, a0, e) 
y=y+e

print("ARX")
[theta]=sysid.arx(2, 1, u, y, 1)
print(theta)

print("ARMAX")
[theta]=sysid.armax(2, 1, 0, u, y, 1,1000)
print(theta)

print("VRFT")
a=0.9
a0=np.array([1, -a])
b0=np.array([0, 1-a])
rho_vrft=vrft.vrft_pid(u, y,a0,b0,'pid',250)

print("OCI ARX")
rho_oci_arx=vrft.oci_arx(u, y, 0.9)

print("OCI ARMAX")
rho_oci_armax=vrft.oci_armax(u, y, 0.9)


