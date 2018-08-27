import pyulog
import numpy as np
import math


def open_file(arq):

    class dados:
        class param:
            pass
    # Carrega Mensagens
    msg=['vehicle_attitude','vehicle_attitude_setpoint','actuator_controls_0','vehicle_rates_setpoint'];

    ulog = pyulog.ULog(arq, msg)
    
    dados.param.r_r_p=ulog.initial_parameters['MC_ROLLRATE_P']
    dados.param.r_r_i=ulog.initial_parameters['MC_ROLLRATE_I']
    dados.param.r_r_d=ulog.initial_parameters['MC_ROLLRATE_D']

    dados.param.r_p_p=ulog.initial_parameters['MC_PITCHRATE_P']
    dados.param.r_p_i=ulog.initial_parameters['MC_PITCHRATE_I']
    dados.param.r_p_d=ulog.initial_parameters['MC_PITCHRATE_D']

    dados.param.r_y_p=ulog.initial_parameters['MC_YAWRATE_P']
    dados.param.r_y_i=ulog.initial_parameters['MC_YAWRATE_I']
    dados.param.r_y_d=ulog.initial_parameters['MC_YAWRATE_D']

    dados.param.a_r_p=ulog.initial_parameters['MC_ROLL_P']
    dados.param.a_p_p=ulog.initial_parameters['MC_PITCH_P']
    dados.param.a_y_p=ulog.initial_parameters['MC_YAW_P']


    for d in ulog.data_list:

        if d.name=='vehicle_rates_setpoint':
            t0=d.data['timestamp']
            dados.r_r_r=d.data['roll']
            dados.r_r_p=d.data['pitch']
            dados.r_r_y=d.data['yaw']


        if d.name=='vehicle_attitude':
            t1=d.data['timestamp']
            y_r_r=d.data['rollspeed']
            y_r_p=d.data['pitchspeed']
            y_r_y=d.data['yawspeed']
            q0=d.data['q[0]']
            q1=d.data['q[1]']
            q2=d.data['q[2]']
            q3=d.data['q[3]']

        if d.name=='actuator_controls_0':
            t2=d.data['timestamp']
            u_r=d.data['control[0]']
            u_p=d.data['control[1]']
            u_y=d.data['control[2]']
            u_z=d.data['control[3]']
        
        if d.name=='vehicle_attitude_setpoint':
            t3=d.data['timestamp']
            q0d=d.data['q_d[0]']
            q1d=d.data['q_d[1]']
            q2d=d.data['q_d[2]']
            q3d=d.data['q_d[3]']
  
    N=np.size(q0)
    y_a_p=np.zeros(N)
    y_a_r=np.zeros(N)
    y_a_y=np.zeros(N)
    
    for i in range(0, N):
        y_a_p[i] = -math.asin(2*q1[i]*q3[i]-2*q2[i]*q0[i])
        tt0 = +2.0 * (q0[i] * q1[i] + q2[i] * q3[i])
        tt1 = +1.0 - 2.0 * (q1[i] * q1[i] + q2[i] * q2[i])
        y_a_r[i] = math.atan2(tt0, tt1)
        y_a_y[i] = math.atan2(tt0, tt1)


    N=np.size(q0d)
    r_a_p=np.zeros(N)
    r_a_r=np.zeros(N)
    r_a_y=np.zeros(N)
    for i in range(0, N):
        r_a_p[i] = -math.asin(2*q1d[i]*q3d[i]-2*q2d[i]*q0d[i])
        tt0 = +2.0 * (q0d[i] * q1d[i] + q2d[i] * q3d[i])
        tt1 = +1.0 - 2.0 * (q1d[i] * q1d[i] + q2d[i] * q2d[i])
        r_a_r[i] = math.atan2(tt0, tt1)
        r_a_y[i] = math.atan2(tt0, tt1)



    # Interpola os dados para todos terem a mesma base de tempo
    dados.y_r_r=np.interp(t0, t1, y_r_r)
    dados.y_r_p=np.interp(t0, t1, y_r_p)
    dados.y_r_y=np.interp(t0, t1, y_r_y)

    dados.u_r=np.interp(t0, t2, u_r)
    dados.u_p=np.interp(t0, t2, u_p)
    dados.u_y=np.interp(t0, t2, u_y)
    dados.u_z=np.interp(t0, t2, u_z)


    dados.y_a_r=np.interp(t0, t1, y_a_r)
    dados.y_a_p=np.interp(t0, t1, y_a_p)
    dados.y_a_y=np.interp(t0, t1, y_a_y)

    dados.r_a_r=np.interp(t0, t3, r_a_r)
    dados.r_a_p=np.interp(t0, t3, r_a_p)
    dados.r_a_y=np.interp(t0, t3, r_a_y)

    dados.t0=t0

    return dados
    
