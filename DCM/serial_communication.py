import serial.tools.list_ports
import struct
import json
import tkinter.messagebox as messagebox


class SerialCommunication:
    def __init__(self, main_app):
        self.main = main_app
        

    def check_connection(self):
        username = self.main.username
        ports = serial.tools.list_ports.comports()
        connected = False
        try:
            with open("DCM/DataStorage/pacemaker_board_list.json", "r") as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    # Handle the case of an empty JSON file
                    data = {}
        except FileNotFoundError:
            data = {}
        if not data:
            data = {}
    

        # Check for the specific hardware identifier across all available ports
        for prt, desc, hwid in sorted(ports):
            if hwid.startswith("USB VID:PID=1366:1015"):
                self.main.port_list[0] = hwid
                self.main.pacemaker_port = prt
                connected = True
                if username in data:
                    if hwid in data[username]:
                        continue
                    else:
                        data[username] = self.main.port_list
                        messagebox.showwarning("Warning!", "A new pacemaker board has been connected") 
                        with open("DCM/DataStorage/pacemaker_board_list.json", "w") as file:
                            json.dump(data, file)
                else:
                    data[username] = self.main.port_list
                    messagebox.showwarning("Warning!", "A new pacemaker board has been connected")  
                    with open("DCM/DataStorage/pacemaker_board_list.json", "w") as file:
                        json.dump(data, file)

            elif hwid.startswith("USB VID:PID=0483:374B"):
                self.main.heart_port = prt
                self.main.port_list[1] = hwid
                if username in data:
                    if hwid in data[username]:
                        continue
                    else:
                        data[username] = self.main.port_list
                        messagebox.showwarning("Warning!", "A new heart board has been connected")    
                        with open("DCM/DataStorage/pacemaker_board_list.json", "w") as file:
                            json.dump(data, file)
                        break
                else:
                    data[username] = self.main.port_list
                    messagebox.showwarning("Warning!", "A new heart board has been connected")   
                    with open("DCM/DataStorage/pacemaker_board_list.json", "w") as file:
                        json.dump(data, file)
                    break

        return connected

        # Define the function to establish a serial connection and send parameters
    def send_parameters(self, data_to_send,s0,s1):
        activity_thresh_values = {
        'v-low': 0,
        'low': 1,
        'med-low': 2,
        'med': 3,
        'med-high': 4,
        'high': 5,
        'v-high': 6
        }

        activity_thresh_value = activity_thresh_values[data_to_send['ACTIVITY_THRESH']]
    
        packet = []

        s2 = struct.pack('B', data_to_send['MODE'])
        s3 = struct.pack('H', data_to_send['LRL'])
        s4 = struct.pack('H', data_to_send['URL'])
        s5 = struct.pack('H', data_to_send['MSR'])
        s6 = struct.pack('f', data_to_send['A_AMPLITUDE'])
        s7 = struct.pack('f', data_to_send['V_AMPLITUDE'])
        s8 = struct.pack('H', data_to_send['A_WIDTH'])
        s9 = struct.pack('H', data_to_send['V_WIDTH'])
        s10 = struct.pack('f', data_to_send['A_SENSITIVITY'])
        s11 = struct.pack('f', data_to_send['V_SENSITIVITY'])
        s12 = struct.pack('H', data_to_send['VRP'])
        s13 = struct.pack('H', data_to_send['ARP'])
        s14 = struct.pack('B', activity_thresh_value)
        s15 = struct.pack('H', data_to_send['REACT_TIME'])
        s16 = struct.pack('H', data_to_send['RESPONSE_FAC'])
        s17 = struct.pack('H', data_to_send['RECOVERY_TIME'])
        
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
        ser = serial.Serial(self.main.pacemaker_port,115200)

        ser.write(b''.join(packet))
        #print('Data has been written: ', packet)
        #Receiving Params
        modeN = (struct.unpack('B',ser.read(1)))[0]
        lrl = (struct.unpack('H',ser.read(2)))[0]
        url = (struct.unpack('H',ser.read(2)))[0]
        msr= (struct.unpack('H',ser.read(2)))[0]
        a_amplitude = (struct.unpack('f',ser.read(4)))[0]
        v_amplitude = (struct.unpack('f',ser.read(4)))[0]
        a_width = (struct.unpack('H',ser.read(2)))[0]
        v_width = (struct.unpack('H',ser.read(2)))[0]
        a_sensitivity = (struct.unpack('f',ser.read(4)))[0]
        v_sensitivity = (struct.unpack('f',ser.read(4)))[0]
        vrp = (struct.unpack('H',ser.read(2)))[0]
        arp = (struct.unpack('H',ser.read(2)))[0]
        activity_thresh = (struct.unpack('B',ser.read(1)))[0]
        react_time = (struct.unpack('H',ser.read(2)))[0]
        r_factor = (struct.unpack('H',ser.read(2)))[0]
        rec_time = (struct.unpack('H',ser.read(2)))[0]
        a_signal = (struct.unpack('d',ser.read(8)))[0]
        v_signal = (struct.unpack('d',ser.read(8)))[0]
        receivedArray = [modeN,lrl,url,msr,a_amplitude,v_amplitude,a_width,v_width, a_sensitivity, v_sensitivity,vrp,arp,activity_thresh,react_time,r_factor,rec_time]
        egram_data = [a_signal,v_signal]
        print('Received Array: ', receivedArray)
        print('Egram Data: ', egram_data)
        error = 0
        while(error == 0):
            if(data_to_send['MODE'] != round(modeN)):
                error = 1
            elif(data_to_send['LRL'] != round(lrl)):
                error = 1
            elif(data_to_send['URL']  != round(url)):
                error = 1
            elif(data_to_send['MSR']  != round(msr)):
                error = 1
            elif(data_to_send['A_AMPLITUDE']  != round(a_amplitude,1)):
                error = 1
            elif(data_to_send['V_AMPLITUDE']  != round(v_amplitude,1)):
                error = 1
            elif(data_to_send['A_WIDTH'] != round(a_width,1)):
                error = 1
            elif(data_to_send['V_WIDTH'] != round(v_width,1)):
                error = 1
            elif(data_to_send['A_SENSITIVITY'] != round(a_sensitivity)):
                error = 1
            elif(data_to_send['V_SENSITIVITY'] != round(v_sensitivity)):
                error = 1
            elif(data_to_send['VRP'] != round(vrp)):
                error = 1
            elif(data_to_send['ARP'] != round(arp)):
                error = 1
            elif(activity_thresh_value != round(activity_thresh)):
                error = 1
            elif(data_to_send['REACT_TIME'] != round(react_time)):
                error = 1
            elif(data_to_send['RESPONSE_FAC'] != round(r_factor)):
                error = 1
            elif(data_to_send['RECOVERY_TIME'] != round(rec_time)):
                error = 1
            else:
                error = 2
    
        if(error == 1):
            if(s1 != b'\x02'):
                messagebox.showinfo("Note!", "There was a problem communicating with the Pacemaker")
        else:
            messagebox.showinfo("Note!", "The parameters have been confirmed with the Pacemaker")
            # egram_display(pacemaker,mode,modeNum)
        ser.close()  # Close the serial connection after sending

        return egram_data

  
