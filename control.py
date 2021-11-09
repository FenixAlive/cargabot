import time
import numpy as np

def define_variables_control_cam(how):
    if how == "qr":
        cam_temp = [
        #const_cam
        {
            "D": 0.15,
            "L": 0.11,
            "R": 0.085,
            "centroDeseado": 640/2,
            "tamDeseado": 130,
        },
        #var_cam
        {
            "wV": np.array([0.17, 0.0005]),
            "wW": np.array([0.37, .003, 0.000]),
            "e": np.array([0.00, 0.00]),
            "eOld": np.array([0.00, 0.00]),
            "tAnt": time.time(),
            "eAcum": 0,
        }
        ]
    elif how == "grn":
        cam_temp = [
        #const_cam
        {
            "D": 0.15,
            "L": 0.11,
            "R": 0.085,
            "centroDeseado": 640/2,
            "tamDeseado": 80,
        },
        #var_cam
        {
            "wV": np.array([0.1, 0.00005]),
            "wW": np.array([0.35, .003, 0.000]),
            "e": np.array([0.00, 0.00]),
            "eOld": np.array([0.00, 0.00]),
            "tAnt": time.time(),
            "eAcum": 0,
        }
    ]
    return cam_temp
        


def control_camera(cam_info, const_cam, var_cam):
    if cam_info != False:
        centro, tam = cam_info
    else:
        return (0, 0, var_cam)
    error_v = const_cam["tamDeseado"]-tam
    error_w = const_cam["centroDeseado"] - centro
    var_cam["e"] = np.array([error_v, error_w])
    var_cam["eAcum"]= var_cam["eAcum"]+error_w
    error_d = np.divide(var_cam["e"]-var_cam["eOld"], time.time()-var_cam["tAnt"])
    #salida de red
    v = error_v * var_cam["wV"][0] + error_d[0]*var_cam["wV"][1]
    w = error_w * var_cam["wW"][0] + error_d[1]*var_cam["wW"][1] +var_cam["eAcum"]*var_cam["wW"][2]
    if abs(error_v) < 2.5:
        v=0
    #velocidad ruedas
    vr = (2*v + w*const_cam["L"])/(2*const_cam["R"])
    vl = (2*v - w*const_cam["L"])/(2*const_cam["R"])
    return [vr, vl, var_cam]


def control_sensors(dist):
    varSenMax = 0.75
    Kp_R = [16, -6, -8, 12, 6, -5]
    Kp_L = [-8, -6, 16, -5, 6, 12]
    varSen = 0
    vr = 0
    vl = 0
    for i in range(len(dist)):
        if dist[i] > varSenMax:
            varSen = varSenMax
        elif dist[i] > varSen:
            varSen = dist[i]
        vr += dist[i]*Kp_R[i]*7.5
        vl += dist[i]*Kp_L[i]*7.5
    varSen = 1-(varSen-0)/(varSenMax-0)
    return [vr, vl, varSen]
