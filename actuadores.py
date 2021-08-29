import os

def actua(vr, vl, sens, qrInfo):
    os.system("clear")
    print("")
    print("  |{:.2f}| |{:.2f}| |{:.2f}| |{:.2f}|".format(sens[3], sens[2], sens[1], sens[0]))
    print("")
    if qrInfo != False:
        print("")
        print(qrInfo)
        print("")
        print("           |--o--|")
    else:
        print("")
        print("")
        print("")
        print("           |-----|")
    print("           |--A--|")
    print("    |{:2.2f}|-|-----|-|{:2.2f}|".format(vl,vr))
    print("           |-----|")
    print("    |{:2.2f}|-|-----|-|{:2.2f}|".format(vl,vr))
    print("")
    print("    |{:.2f}| |{:.2f}| |{:.2f}|".format(sens[4], sens[5], sens[6]))
    print("")

