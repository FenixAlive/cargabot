# cargabot

Requiere las siguientes dependencias de Python para la camara:
opencv
numpy
pyzbar

#para correr la camara pixman hacer un preload
LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libv4l/v4l1compat.so python3 modular/camara.py
