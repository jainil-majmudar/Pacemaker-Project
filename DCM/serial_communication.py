import serial

ser = serial.Serial()  # open serial port
ser.port = 'COM3'
print(ser.name)   
ser.open()
data = ser.read()
ser.close()
