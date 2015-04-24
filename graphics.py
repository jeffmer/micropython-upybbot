# graphics routines - recoded in Python from Adafruit-GFX-Library

'''
Copyright (c) 2013 Adafruit Industries.  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''



import pyb
import math

def drawCircle(lcd,x0,y0,r,color):
    '''
    draw circle with centre (x0,y0) and radius r
    '''
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r
    lcd.pixel(x0  , y0+r, color)
    lcd.pixel(x0  , y0-r, color)
    lcd.pixel(x0+r, y0  , color)
    lcd.pixel(x0-r, y0  , color)
    while (x<y):
        if (f >= 0):
            y -= 1
            ddF_y += 2
            f += ddF_y
        x +=1
        ddF_x += 2
        f += ddF_x
        lcd.pixel(x0 + x, y0 + y, color)
        lcd.pixel(x0 - x, y0 + y, color)
        lcd.pixel(x0 + x, y0 - y, color)
        lcd.pixel(x0 - x, y0 - y, color)
        lcd.pixel(x0 + y, y0 + x, color)
        lcd.pixel(x0 - y, y0 + x, color)
        lcd.pixel(x0 + y, y0 - x, color)
        lcd.pixel(x0 - y, y0 - x, color)

def swap(x,y,yes):
    if yes:
        return (y,x)
    else:
        return (x,y)

# Bresenham's algorithm -  wikpedia
def drawLine(lcd, xa, ya, xb, yb, color):
    '''
    draw line from (xa,ya to xb,yb
    '''
    steep = abs(yb - ya) > abs(xb - xa)
    x0,y0 = swap(xa, ya,steep)
    x1,y1 = swap(xb, yb,steep)
    yes = x0>x1
    x0,x1 = swap(x0, x1, yes)
    y0,y1 = swap(y0, y1, yes)
    dx = x1 - x0
    dy = abs(y1 - y0)
    err = dx // 2
    ystep = -1
    if (y0 < y1):
        ystep = 1
    while (x0<=x1):
        if (steep):
            lcd.pixel(y0, x0, color)
        else:
            lcd.pixel(x0, y0, color)
        err -= dy
        if (err < 0):
            y0 += ystep
            err += dx;
        x0+=1


def line(lcd,x,y,phi,d,color):
    '''
    draw a line of lenght d from (x,y) at angle phi in degrees
    '''
    a = math.radians(phi)
    x1 = int(x + d * math.sin(a))
    y1 = int(y + d * math.cos(a))
    drawLine(lcd,x,y,x1,y1,color)
    
