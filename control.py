# width ideal 250

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


def controlCamara(qrInfo, constCam, varCam):
    pass
