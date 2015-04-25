# UPYBBOT - micropython balaancing robot
# jeffm   - 23.4.2015

import pyb
import graphics
from ssd1306 import SSD1306

lcd = SSD1306(pinout={'sda': 'X10',
                          'scl': 'X9'},
                           height=64,
                           external_vcc=False)
lcd.poweron()
lcd.init_display()
 
from mpu6050 import MPU6050
imu = MPU6050(2,False)

# Complementary Filter A = rt/(rt + dt) where rt is response time, dt = period
fangle = 0.0
def compf(accel,gyro,looptime,A):
    global fangle
    fangle = A * (fangle + gyro * looptime/1000000) + (1-A) * accel
    return fangle

#  graphic display of accel angle & filtered angle
#   - primarily used in development but also for initial setup
def align(n=60):
    lcd.clear()
    lcd.text("Acc",0,56,1)
    lcd.text("CompF",64,56,1)
    graphics.drawCircle(lcd,32,26,26,1)
    graphics.drawCircle(lcd,96,26,26,1)
    start = pyb.micros()
    for i in  range(n):
        angle  = imu.pitch()
        cangle = compf(angle, imu.get_gy(), pyb.elapsed_micros(start),0.91) 
        start = pyb.micros()
        graphics.line(lcd,32,26,angle,24,1)
        graphics.line(lcd,96,26,cangle,24,1)
        lcd.display()
        graphics.line(lcd,32,26,angle,24,0)
        graphics.line(lcd,96,26,cangle,24,0)
    lcd.clear()
    lcd.text("Start balancing!.",0,24,1)
    lcd.text('zero:{:5.2f}'.format(cangle),0,32,1)
    lcd.display()

# set up stepper motors
from nemastepper import Stepper
motor1 = Stepper('Y1','Y2','Y3')
motor2 = Stepper('X1','X2','X3')

from pyb import Timer

def issr(t):
    global motor1, motor2
    motor1.do_step()
    motor2.do_step()
    
tim = Timer(8,freq=10000)

MAX_VEL = 2000 # 2000 usteps/sec = 500steps/sec = 2.5rps = 150rpm
MAX_ANGLE = 7  # degrees of tilt for speed control

def constrain(val,minv,maxv):
    if val<minv:
        return minv
    elif val>maxv:
        return maxv
    else:
        return val

#stability PD controiller - input is target angle, output is acceleration
K =  7
Kp = 4.0
Kd = 0.4
def stability(target,current,rate):
    global K,Kp,Kd
    error = target - current
    output = Kp * error - Kd*rate
    return int(K*output)

#speed P controiller - input is target speed, output is inclination angle
KpS = 0.008
def speedcontrol(target,current):
    global KpS
    error = target - current
    output = KpS * error 
    return constrain(output,-MAX_ANGLE,+MAX_ANGLE)


import radio
rr = radio.Radio(['Y4','Y5','Y6','Y7'])

#main balance loop runs every 5ms
zero_angle = 0.0
def balance():
    global zero_angle
    gangle = zero_angle
    start = pyb.micros()
    controlspeed = 0
    fspeed = 0
    while abs(gangle) < 45:  # give up if inclination angle >=45 degrees
        angle  = imu.pitch()
        rate   = imu.get_gy()
        gangle = compf(angle, rate, pyb.elapsed_micros(start),0.99)         
        start = pyb.micros()
        # speed control
        actualspeed = (motor1.get_speed()+motor2.get_speed())/2
        fspeed = 0.95 * fspeed + 0.05 * actualspeed
        cmd =rr.state()        
        if cmd[2]:                                      # forward
            tangle  = speedcontrol(800,int(fspeed))
        elif cmd[3]:                                    # reverse
            tangle  = speedcontrol(-800,int(fspeed))
        else:                                           # stand still
            tangle  = speedcontrol(0,int(fspeed))
        # stability control
        controlspeed += stability(zero_angle+tangle,gangle,rate)           
        controlspeed = constrain(controlspeed,-MAX_VEL,MAX_VEL)
        # aet motor speed
        if cmd[0]:                                      # turn clockwise
            motor1.set_speed(-controlspeed-300)
            motor2.set_speed(-controlspeed+300)
        elif cmd[1]:                                    # turn anti-clockwise
            motor1.set_speed(-controlspeed+300)
            motor2.set_speed(-controlspeed-300)
        else:                                           # no turn
            motor1.set_speed(-controlspeed)
            motor2.set_speed(-controlspeed)
          
        pyb.udelay(5000-pyb.elapsed_micros(start))
    # stop and turn off motors
    motor1.set_speed(0)
    motor2.set_speed(0)
    motor1.set_off()
    motor2.set_off()

# main program
align()
tim.callback(issr) #start interrupt routine
balance()
tim.callback(None) #stop interrupt routine
         
   
        






              
