import camara
import sensores
import control
import actuadores

def main():
    if not camara.cam.read()[0]:
        print("fallo al detectar camara")
        return False
    while(1):
        info = camara.foto()
        if info:
            print("QR: ", info)
        #sensores
        #tomar decisiones con los datos (control)
        #actuadores

if __name__ == '__main__':
    main()
