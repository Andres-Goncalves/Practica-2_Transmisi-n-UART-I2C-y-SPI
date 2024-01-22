from machine import Pin, I2C, UART
from ssd1306 import SSD1306_I2C
from utime import sleep_ms
from time import localtime


#led
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

#UART
uart = UART(0, baudrate=100000, tx=Pin(0), rx=Pin(1),timeout=1)

#pantalla
WIDTH=128
HEIGHT=64
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT,i2c)

datos = []

#recibir datos
while True:
    if uart.any():
        data = str(uart.readline(), 'utf-8')
        print("Valor recibido:", data)
        led_t()
        
        if data == "Terminar conexion":
            led.value(0)
            break
        
        datos.append(int(data))
        
print(datos)
X = 48

#graficar
fecha = localtime()
oled.fill(0)
oled.text("{dia:02d}/{mes:02d}/{año:04d} {hora:02d}:{minuto:02d}".format(año = fecha[0],mes = fecha[1],dia = fecha[2],hora = fecha[3],minuto = fecha[4]),0,0)
oled.text("UART",X,8)
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
    oled.text("UART",X,8)
    oled.text("UART",X+64,8)
    oled.text("UART",X+128,8)
    oled.text("UART",X-64,8)
    oled.text("UART",X-128,8)
    oled.show()
    X -= 1
    if X == -32:
        X = 160
    sleep_ms(40)