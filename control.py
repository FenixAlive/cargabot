# width ideal 250
import time
import numpy as np

def defineVariablesControlCam():
    return [
        #constCam
        {
            "D": 0.16,
            "L": 0.23,
            "R": 0.12,
            "etaV": np.array([0.0001, 0.0001]),
            "etaW": np.array([0.0001, 0.0001]),
            "centroDesesado": 640/2,
            "tamDesesado": 200,
        },
        #varCam
        {
            "wV": np.array([0.001, 0.001]),
            "wW": np.array([0.001, 0.001]),
            "e": np.array([0.001, 0.001]),
            "eOld": np.array([0.001, 0.001]),
            "tAnt": time.time(),
            "vAnt": np.array([0,0]) 
        }
    ]


def controlCamara(qrInfo, constCam, varCam):
    centro = qrInfo.left + qrInfo.width/2
    errorV = constCam["tamDesesado"]-qrInfo.height
    errorW = constCam["centroDesesado"] - centro
    varCam["e"] = np.array([errorV, errorW])
    errorD = np.divide(varCam["e"]-varCam["eOld"], time.time()-varCam["tAnt"])
    #salida de red
    v = errorV * varCam["wV"][0] + errorD[0]*varCam["wV"][1]
    w = errorW * varCam["wW"][0] + errorD[1]*varCam["wW"][1]
    #actualiza pesos
    #revisión de pesos y velocidad
   # varCam["wV"][0] = varCam["wV"][0]+constCam["etaV"][0]*v*errorV
    #varCam["wV"][1] = varCam["wV"][1]+constCam["etaV"][1]*v*errorD[0]
    #varCam["wW"][0] = varCam["wW"][0]+constCam["etaW"][0]*w*errorV
    #varCam["wW"][1] = varCam["wW"][1]+constCam["etaW"][1]*w*errorD[1]
    #varCam["eOld"] = varCam["e"]
    #velocidad ruedas
    vr = (2*v + w*constCam["L"])/(2*constCam["R"])
    vl = (2*v - w*constCam["L"])/(2*constCam["R"])
    return [vr, vl, varCam]


def controlSensores(dist):
    Kp_R = [8, -3, -4, 6, 3, -2]
    Kp_L = [-4, -3, 8, -2, 3, 6]
    varSen = 0
    vr = 0
    vl = 0
    for i in range(len(dist)):
        if dist[i] > 0.85:
            varSen = 0.85
        elif dist[i] > varSen:
            varSen = dist[i]
        vr += dist[i]*Kp_R[i]*10
        vl += dist[i]*Kp_L[i]*10
    varSen = 1-(varSen-0)/(0.85-0)
    return [vr, vl, varSen]
