#import winreg
#import itertools
import sys
import glob
import serial

 



class SerialUtility(object):
    
   
    def __init__(self):
        pass
    
    @staticmethod
    def serial_ports():


        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z0-9]*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
            return result


if __name__ == '__main__':
    print(SerialUtility.serial_ports())   
    #def ListComPort():
    
        
        #regPath="HARDWARE\\DEVICEMAP\\SERIALCOMM"
        #COM_List = []
        
        #try:
            
            #regKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regPath)
        #except WindowsError:
            #raise IOError
        
        #for i in itertools.count():
            #try:
                #keyValue = winreg.EnumValue(regKey, i)
              # COM_List.append(keyValue[1]+" "+keyValue[0])
            #except EnvironmentError:
                #break
            
        #return COM_List
        

        
        
    
    
class SerialConnection(object):
    
    
    def __init__(self):
        
        self._baudRate = "57600"
        self._stopBits = "1"
        self._dataBits = "8"
        self._parity = False
    
    @property
    def baudRate(self):
        return self._baudRate
    
    @baudRate.setter
    def baudRate(self, value):
        self._baudRate = value
        
    @property
    def stopBits(self):
        return self._stopBits
    
    @stopBits.setter
    def stopBits(self, value):
        self._stopBits = value
        
    @property
    def dataBits(self):
        return self._dataBits
    
    @dataBits.setter
    def dataBits(self, value):
        self._dataBits = value
        
    @property
    def parity(self):
        return self._parity
    
    @parity.setter
    def parity(self, value):
        self._parity = value
        
    