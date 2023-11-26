import serial.tools.list_ports
import struct

def check_connection():
    ports = serial.tools.list_ports.comports()
    connected = False

    # Check if 'COM3' port is in the list of available ports
    for port, desc, hwid in sorted(ports):
        if 'COM3' in port:
            connected = True
            break
    return connected

# Define the function to establish a serial connection and send parameters
def send_parameters(data_to_send):
    # Establish a serial connection - update the port and baud rate
    ser = serial.Serial('COM3', 115200)  # Update 'COM3' to your port and 115200 to your baud rate
    
    activity_thresh = data_to_send['ACTIVITY_THRESH'].encode('utf-8')  # Convert the string to bytes
    # Pack the parameters according to the Simulink array order for bytes
    
   
    packet = struct.pack(
    '<BBBBBBffBBffHHBBpBBB',
    0,  # rxdata(1)
    0,  # rxdata(2)
    data_to_send['MODE'],
    data_to_send['LRL'],
    data_to_send['URL'],
    data_to_send['MSR'],

    data_to_send['A_AMPLITUDE'],
    data_to_send['V_AMPLITUDE'],

    data_to_send['A_WIDTH'],
    data_to_send['V_WIDTH'],

    data_to_send['A_SENSITIVITY'],
    data_to_send['V_SENSITIVITY'],

    data_to_send['VRP'],
    data_to_send['ARP'],

    data_to_send['HRL'],
    data_to_send['RATE_SMOOTH'],
    activity_thresh,
    data_to_send['REACT_TIME'],
    data_to_send['RESPONSE_FAC'],
    data_to_send['RECOVERY_TIME'],
    )
   
    ser.write(packet)
    print('Data has been written: ', packet)
    ser.close()  # Close the serial connection after sending

