#!/usr/bin/env python

import matplotlib.pyplot as plt
import sys
from scipy import signal
import numpy as np
import glob
import os
import math
import argparse


from px4tuning import sysid
from px4tuning import vrft
from px4tuning import importa


def custo(e):
    e=e[2500:-2500]*180/math.pi
    N=e.size
    return math.sqrt(e@e/(N))



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--plot', action='store_true', help="enable plotting")
    parser.add_argument('file', nargs='?', help='file.ulg')

    args = parser.parse_args()

    if args.file:
        arq=args.file
    else:
        list_of_files=glob.glob('*.ulg')
        arq = max(list_of_files, key=os.path.getctime)
    print("Arquivo", arq)
    
    D=importa.open_file(arq)
    
    t0=D.t0
    N=np.size(t0)
    P=N/(t0[-1]-t0[0])*1000000
    print("\nSampling rate:", P, "Hz")
    
    if P<200:
        print("Low sampling rate:")
        print("The following topics should be sampled at least at 200Hz")
        print("'vehicle_attitude','vehicle_attitude_setpoint','actuator_controls_0','vehicle_rates_setpoint'")
        return -1



    
    print("\n=== ROLL RATE")
    
    a=0.98
    b0=np.array([0, 4*(1-a), -4*(1-a)*a])
    a0=np.array([1, -4*a+2, (2*a-1)*(2*a-1)])
    
    yd_r_r = signal.lfilter(b0, a0, D.r_r_r)
    e_r_r=yd_r_r-D.y_r_r
    
    print("Custo: ", custo(e_r_r))
    print("Old PID(s):",D.param.r_r_p,D.param.r_r_i,D.param.r_r_d)
    rho_vrft=vrft.vrft_pid_mf(D.u_r, D.y_r_r, a0, b0, 'loco'  ,P,0.98)
    
    
    
    print("\n=== PITCH RATE")
    
    a=0.98
    b0=np.array([0, 4*(1-a), -4*(1-a)*a])
    a0=np.array([1, -4*a+2, (2*a-1)*(2*a-1)])
    
    yd_r_p = signal.lfilter(b0, a0, D.r_r_p)
    e_r_p=yd_r_p-D.y_r_p
    print("Custo: ", custo(e_r_p))
    print("Old PID(s):",D.param.r_r_p,D.param.r_r_i,D.param.r_r_d)
    rho_vrft=vrft.vrft_pid_mf(D.u_p, D.y_r_p, a0, b0, 'loco'  ,P,0.98)
    
    
    
    
    
    print("\n=== YAW RATE")
    
    a=0.99
    b0=np.array([0, 4*(1-a), -4*(1-a)*a])
    a0=np.array([1, -4*a+2, (2*a-1)*(2*a-1)])
    
    yd_r_y = signal.lfilter(b0, a0, D.r_r_y)
    e_r_y=yd_r_y-D.y_r_y
    
    print("Custo: ",custo(e_r_y))
    print("Old PID(s):",D.param.r_r_p,D.param.r_r_i,D.param.r_r_d)
    rho_vrft=vrft.vrft_pid_mf(D.u_y, D.y_r_y, a0, b0, 'loco'  ,P,0.99)
    
    
    
    
    
    print("\n=== ROLL ANGLE")
    
    a=0.99
    b0=np.array([0, 1-a])
    a0=np.array([1, -a])
    
    yd_a_r = signal.lfilter(b0, a0, D.r_a_r)
    e_a_r=yd_a_r-D.y_a_r
    print("Custo: ", custo(e_a_r))
    print("Old PID(s):",D.param.a_r_p)
    rho_vrft=vrft.vrft_pid_mf(D.r_r_r, D.y_a_r, a0, b0, 'p'    ,P,1)
    
    
    
    
    
    print("\n=== PITCH ANGLE")
    
    a=0.99
    b0=np.array([0, 1-a])
    a0=np.array([1, -a])
    
    yd_a_p = signal.lfilter(b0, a0, D.r_a_p)
    e_a_p=yd_a_p-D.y_a_p
    print("Custo: ", custo(e_a_p))
    print("Old PID(s):",D.param.a_p_p)
    rho_vrft=vrft.vrft_pid_mf(D.r_r_p, D.y_a_p, a0, b0, 'p'    ,P,1)



    print("\n=== YAW ANGLE")
    
    a=0.99
    b0=np.array([0, 1-a])
    a0=np.array([1, -a])
    
    yd_a_y = signal.lfilter(b0, a0, D.r_a_y)
    e_a_p=yd_a_y-D.y_a_y
    print("Custo: ", custo(e_a_p))
    print("Old PID(s):",D.param.a_y_p)
    rho_vrft=vrft.vrft_pid_mf(D.r_r_y, D.y_a_y, a0, b0, 'p'    ,P,1)

    
    if args.plot:
    
        # Plota os graficos
        
        K=180/math.pi
        t0=t0*1e-6
        
        
        p1=plt.figure(1)
        plt.plot(t0,D.u_r, label='roll')
        plt.plot(t0,D.u_p, label='pitch')
        plt.plot(t0,D.u_y, label='yaw')
        plt.plot(t0,D.u_z, label='z')
        plt.ylabel('u')
        plt.legend()
        
        p2=plt.figure(2)
        plt.plot(t0,D.r_r_r*K, label='r')
        plt.plot(t0,yd_r_r*K, label='yd')
        plt.plot(t0,D.y_r_r*K, label='y')
        plt.ylabel('Roll rate')
        plt.legend()
        
        p3=plt.figure(3)
        plt.plot(t0,D.r_r_p*K, label='r')
        plt.plot(t0,yd_r_p*K, label='yd')
        plt.plot(t0,D.y_r_p*K, label='y')
        plt.ylabel('Pitch rate')
        plt.legend()
        
        p4=plt.figure(4)
        plt.plot(t0,D.r_r_y*K, label='r')
        plt.plot(t0,yd_r_y*K, label='yd')
        plt.plot(t0,D.y_r_y*K, label='y')
        plt.ylabel('Yaw speed')
        plt.legend()
        
        p5=plt.figure(5)
        plt.plot(t0,D.r_a_r*K, label='r')
        plt.plot(t0,yd_a_r*K, label='yd')
        plt.plot(t0,D.y_a_r*K, label='y')
        plt.ylabel('Roll angle')
        plt.legend()
        
        p6=plt.figure(6)
        plt.plot(t0,D.r_a_p*K, label='r')
        plt.plot(t0,yd_a_p*K, label='yd')
        plt.plot(t0,D.y_a_p*K, label='y')
        plt.ylabel('Pitch angle')
        plt.legend()
        
        plt.show()
    

if __name__ == "__main__":
    main()
