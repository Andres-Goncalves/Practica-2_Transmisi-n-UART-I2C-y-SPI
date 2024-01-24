from spi_slave import SPI_Slave
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep_ms
from time import localtime

#LED
led = Pin("LED",Pin.OUT)
lt = False

def led_t():
    global lt
    if lt:
        led.value(0)
        lt = False
    else:
        led.value(1)
        lt = True
#--------------------------
        
#Leer dato
def Leer_SPI():
    read = slave.rx_words()
    write = slave.tx_words()
    write[0] = read[0]
    
    try:
        dato = read[0].to_bytes(4, "big").decode("utf-8")
    except:
        return "saltar"
    
    slave.put_words()
    
    led_t()
    return dato
#--------------------------------------------------------

#Inicializar pantalla
WIDTH=128
HEIGHT=64
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT,i2c)
#--------------------------------------------------------

#SPI
slave = SPI_Slave(csel=5, mosi=26, sck=27, miso=4, spi_words=1, F_PIO=10_000_000)
slave.put_words()

#sync
inicio = Pin(13,Pin.OUT)
inicio.value(1)
sleep_ms(10)
inicio.value(0)

#Receptor datos
fin = False
datos = []

while True:
    if slave.received():
        dato = Leer_SPI()
        if dato == "@Fin":
            led.value(0)
            break
        else:
            datos.append(int(dato))
            
print("Terminar conexion")
#--------------------------------------------

#Graficar
X = 48
fecha = localtime()
oled.fill(0)
oled.text("{dia:02d}/{mes:02d}/{año:04d} {hora:02d}:{minuto:02d}".format(año = fecha[0],mes = fecha[1],dia = fecha[2],hora = fecha[3],minuto = fecha[4]),0,0)
oled.text("SPI",48,8)
oled.line(24,16,24,63,1)
oled.line(24,16,127,16,1)

maximo = max(datos)
    
oled.text("{medio:02d}".format(medio=int(maximo/2)),0,36)
oled.text("{max:02d}".format(max=int(maximo)),0,16)
    
if not maximo == 0:
    ratio = 100/maximo
else:
    ratio = 0
    
for k in range(len(datos)):

    X = 128-(k+1)*8
    Y = int(64-48*datos[k]*ratio/100) 
    
    oled.rect(X+2,Y,6,64-Y,1,True)
    
oled.show()

while True:
    fecha = localtime()
    oled.rect(0,0,128,16,0,True)
    oled.text("{dia:02d}/{mes:02d}/{año:04d} {hora:02d}:{minuto:02d}".format(año = fecha[0],mes = fecha[1],dia = fecha[2],hora = fecha[3],minuto = fecha[4]),0,0)
    oled.text("SPI",X,8)
    oled.text("SPI",X+64,8)
    oled.text("SPI",X+128,8)
    oled.text("SPI",X-64,8)
    oled.text("SPI",X-128,8)
    oled.show()
    X -= 1
    if X == -32:
        X = 160
    sleep_ms(40)