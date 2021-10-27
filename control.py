import time
import numpy as np

def defineVariablesControlCam(como):
    if como == "qr":
        varCam = [
        #constCam
        {
            "D": 0.15,
            "L": 0.11,
            "R": 0.085,
            "centroDeseado": 640/2,
            "tamDeseado": 150,
        },
        #varCam
        {
            #"wV": np.array([0.1, 0.00005]),
            "wV": np.array([0.05, 0.0005]),
            #"wW": np.array([0.53, .05, 0.0001]),
            "wW": np.array([0.1, .0005, 0.0001]),
            "e": np.array([0.001, 0.001]),
            "eOld": np.array([0.001, 0.001]),
            "tAnt": time.time(),
            "eAcum": 0,
        }
        ]
    elif como == "grn":
        varCam = [
        #constCam
        {
            "D": 0.15,
            "L": 0.11,
            "R": 0.085,
            "centroDeseado": 640/2,
            "tamDeseado": 80,
        },
        #varCam
        {
            #"wV": np.array([0.083, 0.000003]),
            "wV": np.array([0.02, 0.00003]),
            #"wW": np.array([0., .0, 0.000]),
            #"wW": np.array([0.3, .0007, 0.0001]),
            "wW": np.array([0.09, .00007, 0.00001]),
            "e": np.array([0.001, 0.001]),
            "eOld": np.array([0.001, 0.001]),
            "tAnt": time.time(),
            "eAcum": 0,
        }
    ]
    return varCam
        


def controlCamara(qrInfo, constCam, varCam):
    centro, tam = qrInfo
    #centro = qrInfo.left + qrInfo.width/2
    errorV = constCam["tamDeseado"]-tam
    errorW = constCam["centroDeseado"] - centro
    varCam["e"] = np.array([errorV, errorW])
    varCam["eAcum"]= varCam["eAcum"]+errorW
    errorD = np.divide(varCam["e"]-varCam["eOld"], time.time()-varCam["tAnt"])
    #salida de red
    v = errorV * varCam["wV"][0] + errorD[0]*varCam["wV"][1]
    w = errorW * varCam["wW"][0] + errorD[1]*varCam["wW"][1] +varCam["eAcum"]*varCam["wW"][2]
    if abs(errorV) < 4:
        v=0
    #velocidad ruedas
    vr = (2*v + w*constCam["L"])/(2*constCam["R"])
    vl = (2*v - w*constCam["L"])/(2*constCam["R"])
    return [vr, vl, varCam]


def controlSensores(dist):
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
