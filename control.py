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
            "distanciaDesesada": 130,
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
    errorV = constCam["distanciaDesesada"]-qrInfo.height
    errorW = constCam["centroDesesado"] - centro
    varCam["e"] = np.array([errorV, errorW])
    errorD = np.divide(varCam["e"]-varCam["eOld"], time.time()-varCam["tAnt"])
    #salida de red
    v = errorV * varCam["wV"][0] + errorD[0]*varCam["wV"][1]
    w = errorW * varCam["wW"][0] + errorD[1]*varCam["wW"][1]
    #actualiza pesos
    #revisión de pesos y velocidad
    acelMax = [1,5]
    velMax = [3, 5]
    porcDesc = [1.05, 1.05]
    if abs(v-varCam["vAnt"][0]) > acelMax[0]:
        varCam["wV"][0] /= porcDesc[0]
        varCam["wV"][1] /= porcDesc[0]
        if(v > 0 and varCam["vAnt"][0] > 0) or (v < 0 and varCam["vAnt"][0] < 0):
            v = varCam["vAnt"][0]*porcDesc[0]
        else:
            v=0
    else:
        varCam["wV"][0] = varCam["wV"][0]+constCam["etaV"][0]*v*errorV
        varCam["wV"][1] = varCam["wV"][1]+constCam["etaV"][1]*v*errorD[0]
    if v > velMax[0]:
        v = velMax[0]
    elif v < -velMax[0]:
        v = -velMax[0]
    if abs(w-varCam["vAnt"][1]) > acelMax[1]:
        varCam["wW"][0] /= porcDesc[1]
        varCam["wW"][1] /= porcDesc[1]
        if(w > 0 and varCam["vAnt"][1] > 0) or (w < 0 and varCam["vAnt"][1] < 0):
            w = varCam["vAnt"][1]*porcDesc[1]
        else:
            w=0
    else:
        varCam["wW"][0] = varCam["wW"][0]+constCam["etaW"][0]*w*errorV
        varCam["wW"][1] = varCam["wW"][1]+constCam["etaW"][1]*w*errorD[1]
    if w > velMax[1]:
        w = velMax[1]
    elif w < -velMax[1]:
        w = -velMax[1]
    #guardo parametros
    varCam["eOld"] = varCam["e"]
    varCam["vAnt"] = [v, w]
    #velocidad ruedas
    vr = (2*v + w*constCam["L"])/(2*constCam["R"])
    vl = (2*v - w*constCam["L"])/(2*constCam["R"])
    return [vr, vl, varCam]


def controlSensores(dist):
    Kp_R = [10, -2, -5, -3, 10, 2, 2, -3]
    Kp_L = [-3, -5, -2, 10, -3, 2, 2, 10]
    varSen = 0
    vr = 0
    vl = 0
    for i in range(len(dist)):
        if dist[i] > 0.85:
            varSen = 0.85
        elif dist[i] > varSen:
            varSen = dist[i]
        vr += dist[i]*Kp_R[i]
        vl += dist[i]*Kp_L[i]
    varSen = 1-(varSen-0)/(0.85-0)
    return [vr, vl, varSen]
