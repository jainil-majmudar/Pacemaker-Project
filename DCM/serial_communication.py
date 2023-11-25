import serial.tools.list_ports

def check_connection():
    ports = serial.tools.list_ports.comports()
    connected = False

    # Check if 'COM3' port is in the list of available ports
    for port, desc, hwid in sorted(ports):
        if 'COM3' in port:
            connected = True
            break

    return connected