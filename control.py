# width ideal 250
import time

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
    errorD = np.divide(varCam["e"]-varCam["eOld"], time.time()-varCam["tant"])
    #salida de red
    v = errorV * varCam["wV"][0] + errorD[0]*varCam["wV"][1]
    w = errorW * varCam["wW"][0] + errorD[1]*varCam["wW"][1]
    #actualiza pesos

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
