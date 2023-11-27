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
   
    activity_thresh_values = {
    'v-low': 1,
    'low': 2,
    'med-low': 3,
    'med': 4,
    'med-high': 5,
    'high': 6,
    'v-high': 7
    }

    activity_thresh_value = activity_thresh_values[data_to_send['ACTIVITY_THRESH']]
   
    packet = []

    s0 = b'\x00'
    s1 = b'\x00' 
    s2 = b'\x01'
    s3 = struct.pack('B', data_to_send['LRL'])
    s4 = struct.pack('B', data_to_send['URL'])
    s5 = struct.pack('B', data_to_send['MSR'])
    s6 = struct.pack('f', data_to_send['A_AMPLITUDE'])
    s7 = struct.pack('f', data_to_send['V_AMPLITUDE'])
    s8 = struct.pack('B', data_to_send['A_WIDTH'])
    s9 = struct.pack('B', data_to_send['V_WIDTH'])
    s10 = struct.pack('f', data_to_send['A_SENSITIVITY'])
    s11 = struct.pack('f', data_to_send['A_SENSITIVITY'])
    s12 = struct.pack('H', data_to_send['VRP'])
    s13 = struct.pack('H', data_to_send['ARP'])
    s14 = struct.pack('B', activity_thresh_value)
    s15 = struct.pack('B', data_to_send['REACT_TIME'])
    s16 = struct.pack('B', data_to_send['RESPONSE_FAC'])
    s17 = struct.pack('B', data_to_send['RECOVERY_TIME'])
    
    packet.append(s0)
    packet.append(s1)
    packet.append(s2)
    packet.append(s3)
    packet.append(s4)
    packet.append(s5)
    packet.append(s6)
    packet.append(s7)
    packet.append(s8)
    packet.append(s9)
    packet.append(s10)
    packet.append(s11)
    packet.append(s12)
    packet.append(s13)
    packet.append(s14)
    packet.append(s15)
    packet.append(s16)
    packet.append(s17)
    
    #Establish Serial Connection
    ser = serial.Serial("COM3",115200)

    ser.write(b''.join(packet))
    print('Data has been written: ', packet)
    ser.close()  # Close the serial connection after sending

