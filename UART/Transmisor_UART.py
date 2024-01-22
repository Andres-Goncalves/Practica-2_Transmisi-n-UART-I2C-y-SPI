from machine import Pin, SPI, UART
from sdcard import SDCard
from utime import sleep_ms
from uos import VfsFat, mount
from os import listdir

#led
led = Pin("LED", Pin.OUT)
lt = False

def led_t():
    global lt
    if lt:
        led.value(0)
        lt = False
    else:
        led.value(1)
        lt = True

#SPI
cs = Pin(13)
spi = SPI(1,
          baudrate=1000000,
          polarity=0,
          phase=0,
          sck = Pin(10),
          mosi = Pin(11),
          miso = Pin(12))
#SD
sd = SDCard(spi, cs)
vol = VfsFat(sd)
mount(vol, "/sd")

#UART
uart = UART(0, baudrate=100000, tx=Pin(0), rx=Pin(1))

datos = []
cont = 0

#Recopilar datos
for ruta in listdir("/sd"):
    if cont >= 14:
        break
    if ruta[:5] == "Datos":
        archivo = open("/sd/"+ruta, "r")
        aux = archivo.read()
        archivo.close()
        
        cruces = 0
        
        for linea in aux.split("\n"):
            if linea == "":
                continue
            cruces += int(linea[:2])
        
        datos.insert(0,cruces)
        cont += 1

#eviar datos
for dato in datos:
    uart.write(str(dato))
    print("Valor enviado: " + str(dato))
    sleep_ms(100)
    led_t()
    
uart.write("Terminar conexion")
led.value(0)

print("Terminar conexion")
print(datos)