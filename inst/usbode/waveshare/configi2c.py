# /*****************************************************************************
# * | File        :	  config.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface,for Raspberry pi
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-17
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import time
from smbus import SMBus
import ctypes
from gpiozero import *
import spidev

# 2015-06-30
# i2c_detect.py
# Public Domain

import pigpio

pi = pigpio.pi() # connect to local Pi

try:
    for device in range(128):

        h = pi.i2c_open(1, device)
        try:
            pi.i2c_read_byte(h)
            print(hex(device))
        except: # exception if i2c_read_byte fails
            pass
        pi.i2c_close(h)

    pi.stop # disconnect from Pi

except Exception as e:
    print(f"initialized gpio, but received error {e}")

# Pin definition
RST_PIN         = 25
DC_PIN          = 24

#GPIO define
KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

Device_SPI = 0
Device_I2C = 1

# /*****************************************************************************
# * | File        :	  config.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface,for Raspberry pi
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-06-17
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import time
from smbus import SMBus
import ctypes
from gpiozero import *
import spidev
import pigpio
#need to init pigpio daemon
pi = pigpio.pi()

# Pin definition
RST_PIN         = 25
DC_PIN          = 24

#GPIO define
KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

Device_SPI = 0
Device_I2C = 1


class RaspberryPi:
    def __init__(self,rst = 27,dc = 25,bl = 18,bl_freq=1000,i2c=None):
        self.INPUT = False
        self.OUTPUT = True
        
        if(Device_SPI == 1):
            self.Device = Device_SPI
            self.spi = spi
        else :
            self.Device = Device_I2C
            self.address = 0x3c
            self.bus = SMBus(1)
        
        self.GPIO_RST_PIN = self.gpio_mode(RST_PIN,self.OUTPUT)
        self.GPIO_DC_PIN = self.gpio_mode(DC_PIN,self.OUTPUT)

        self.GPIO_KEY_UP_PIN     = self.gpio_mode(KEY_UP_PIN,self.INPUT,True,None)
        self.GPIO_KEY_DOWN_PIN   = self.gpio_mode(KEY_DOWN_PIN,self.INPUT,True,None)
        self.GPIO_KEY_LEFT_PIN   = self.gpio_mode(KEY_LEFT_PIN,self.INPUT,True,None)
        self.GPIO_KEY_RIGHT_PIN  = self.gpio_mode(KEY_RIGHT_PIN,self.INPUT,True,None)
        self.GPIO_KEY_PRESS_PIN  = self.gpio_mode(KEY_PRESS_PIN,self.INPUT,True,None)

        self.GPIO_KEY1_PIN       = self.gpio_mode(KEY1_PIN,self.INPUT,True,None)
        self.GPIO_KEY2_PIN       = self.gpio_mode(KEY2_PIN,self.INPUT,True,None)
        self.GPIO_KEY3_PIN       = self.gpio_mode(KEY3_PIN,self.INPUT,True,None)



    def delay_ms(self,delaytime):
        time.sleep(delaytime / 1000.0)

    def gpio_mode(self,Pin,Mode,pull_up = None,active_state = True):
        if Mode:
            return DigitalOutputDevice(Pin,active_high = True,initial_value =False)
        else:
            return DigitalInputDevice(Pin,pull_up=pull_up,active_state=active_state)


    def gpio_pwm(self,Pin):
        return PWMOutputDevice(Pin,frequency = 10000)

    def set_pwm_Duty_cycle(self,Pin,value):
        Pin.value = value

    def digital_write(self, Pin, value):
        if value:
            Pin.on()
        else:
            Pin.off()

    def digital_read(self, Pin):
        return Pin.value

    def spi_writebyte(self,data):
        self.spi.writebytes([data[0]])

    def i2c_writebyte(self,reg, value):
        self.bus.write_byte_data(self.address, reg, value)
    
    def module_init(self): 
        self.digital_write(self.GPIO_RST_PIN,False)
        if(self.Device == Device_SPI):
            self.spi.max_speed_hz = 1000000
            self.spi.mode = 0b11  
        # CS_PIN.off()
        self.digital_write(self.GPIO_DC_PIN,False)
        return 0

    def module_exit(self):
        if(self.Device == Device_SPI):
            self.spi.close()
        else :
            self.bus.close()
        self.digital_write(self.GPIO_RST_PIN,False)
        self.digital_write(self.GPIO_DC_PIN,False)




class RaspberryPi:
    def __init__(self,rst = 27,dc = 25,bl = 18,bl_freq=1000,i2c=None):
        self.INPUT = False
        self.OUTPUT = True
        
        if(Device_SPI == 1):
            self.Device = Device_SPI
            self.spi = spi
        else :
            self.Device = Device_I2C
            self.address = 0x3c
            self.bus = SMBus(1)
        
        self.GPIO_RST_PIN = self.gpio_mode(RST_PIN,self.OUTPUT)
        self.GPIO_DC_PIN = self.gpio_mode(DC_PIN,self.OUTPUT)

        self.GPIO_KEY_UP_PIN     = self.gpio_mode(KEY_UP_PIN,self.INPUT,True,None)
        self.GPIO_KEY_DOWN_PIN   = self.gpio_mode(KEY_DOWN_PIN,self.INPUT,True,None)
        self.GPIO_KEY_LEFT_PIN   = self.gpio_mode(KEY_LEFT_PIN,self.INPUT,True,None)
        self.GPIO_KEY_RIGHT_PIN  = self.gpio_mode(KEY_RIGHT_PIN,self.INPUT,True,None)
        self.GPIO_KEY_PRESS_PIN  = self.gpio_mode(KEY_PRESS_PIN,self.INPUT,True,None)

        self.GPIO_KEY1_PIN       = self.gpio_mode(KEY1_PIN,self.INPUT,True,None)
        self.GPIO_KEY2_PIN       = self.gpio_mode(KEY2_PIN,self.INPUT,True,None)
        self.GPIO_KEY3_PIN       = self.gpio_mode(KEY3_PIN,self.INPUT,True,None)



    def delay_ms(self,delaytime):
        time.sleep(delaytime / 1000.0)

    def gpio_mode(self,Pin,Mode,pull_up = None,active_state = True):
        if Mode:
            return DigitalOutputDevice(Pin,active_high = True,initial_value =False)
        else:
            return DigitalInputDevice(Pin,pull_up=pull_up,active_state=active_state)


    def gpio_pwm(self,Pin):
        return PWMOutputDevice(Pin,frequency = 10000)

    def set_pwm_Duty_cycle(self,Pin,value):
        Pin.value = value

    def digital_write(self, Pin, value):
        if value:
            Pin.on()
        else:
            Pin.off()

    def digital_read(self, Pin):
        return Pin.value

    def spi_writebyte(self,data):
        self.spi.writebytes([data[0]])

    def i2c_writebyte(self,reg, value):
        self.bus.write_byte_data(self.address, reg, value)
    
    def module_init(self): 
        self.digital_write(self.GPIO_RST_PIN,False)
        if(self.Device == Device_SPI):
            self.spi.max_speed_hz = 1000000
            self.spi.mode = 0b11  
        # CS_PIN.off()
        self.digital_write(self.GPIO_DC_PIN,False)
        return 0

    def module_exit(self):
        if(self.Device == Device_SPI):
            self.spi.close()
        else :
            self.bus.close()
        self.digital_write(self.GPIO_RST_PIN,False)
        self.digital_write(self.GPIO_DC_PIN,False)


### END OF FILE ###

