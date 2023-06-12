import board
import digitalio
import pwmio
import busio
import adafruit_tcs34725
from adafruit_motor import servo
from time import sleep

i2c = busio.I2C(board.GP27, board.GP26)  # SCL-SDA
colorSensor = adafruit_tcs34725.TCS34725(i2c)

in1 = pwmio.PWMOut(board.GP1, frequency=1000)
in2 = pwmio.PWMOut(board.GP2, frequency=1000)
in3 = pwmio.PWMOut(board.GP3, frequency=1000)
in4 = pwmio.PWMOut(board.GP4, frequency=1000)

pwmServo = pwmio.PWMOut(board.GP9, duty_cycle=2 ** 15, frequency=50)
servo1 = servo.Servo(pwmServo, min_pulse=500, max_pulse=2200)

button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT

def defineColor():
    global red, green, blue, yellow, black, white
    
    color_rgb = colorSensor.color_rgb_bytes
    temp = colorSensor.color_temperature
    lux = colorSensor.lux

    if color_rgb[0] > 70 and temp < 3000:
        red = True
        green = False
        blue = False
        yellow = False
        black = False
        white = False
        print('Red')
    elif color_rgb[1] > 30 and temp > 5000:
        red = False
        green = True
        blue = False
        yellow = False
        black = False
        white = False
        print('Green')
    elif color_rgb[2] > 30  and temp > 12000:
        red = False
        green = False
        blue = True
        yellow = False
        black = False
        white = False
        print('Blue')
    elif color_rgb[2] < 10 and lux > 9000:
        red = False
        green = False
        blue = False
        yellow = True
        black = False
        white = False
        print('Yellow')
    elif color_rgb[2] < 30 and lux < 2000:
        red = False
        green = False
        blue = False
        yellow = False
        black = True
        white = False
        print('Black')
    else:
        red = False
        green = False
        blue = False
        yellow = False
        black = False
        white = True
        print('White')

def speedConvertion(pin, speed):
    if speed < 0:
        speed = -speed
    duty = (65535*speed)/100
    duty = int(duty)
    if duty > 65535:
        duty = 65535
    pin.duty_cycle = duty

def move(leftSpeed, rightSpeed):
    if leftSpeed > 0:
        speedConvertion(in1, 0)
        speedConvertion(in2, leftSpeed)
    elif leftSpeed < 0:
        speedConvertion(in1, leftSpeed)
        speedConvertion(in2, 0)
    else:
        speedConvertion(in1, 0)
        speedConvertion(in2, 0)

    if rightSpeed > 0:
        speedConvertion(in3, 0)
        speedConvertion(in4, rightSpeed)
    elif rightSpeed < 0:
        speedConvertion(in3, rightSpeed)
        speedConvertion(in4, 0)
    else:
        speedConvertion(in3, 0)
        speedConvertion(in4, 0)

def UTurn():    
    move(20, -20)
    sleep(1.2)
    while not blue:
        move(20, -20)
        defineColor()
    move(0, 0)
        
def activateServo(start, stop, step):
    for angle in range(start, stop, step):
        servo1.angle = angle
        sleep(0.01)

def shake():
    for i in range(10):
        move(60, -60)
        sleep(0.1)
        move(-60, 60)
        sleep(0.1)
    move(0, 0)

def emptyTrash():
    UTurn()
    activateServo(80, 170, 1)
    shake()
    activateServo(170, 80, -1)

red = False
green = False
blue = False
yellow = False
black = False
white = False

activateServo(170, 80, -1)

while True:
    defineColor()

    if blue or black:
        move(0, 20)
    elif white or red:
        move(20, 0)
    elif green:
        move(0, 0)
        sleep(0.5)
        emptyTrash()
    elif yellow:
        while button.value == True:
            move(0, 0)
            sleep(0.01)
        UTurn()
    else:
        move(0, 0)


