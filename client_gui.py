#!/usr/bin/python
# coding=UTF-8

from Tkinter import *
import socket, time, threading


HOST, PORT = "139.9.115.114", 8001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
 
received_data = 0
receive_buffer_counter = 0
receive_start_detect = 0
receive_buffer = [0 for i in range(50)]
hex_buffer = [0 for i in range(50)]
receive_byte_previous = 0
max_altitude_meters = 0

error = 0
flight_mode = 0
battery_voltage = 0
temperature = 0
roll_angle = 0
pitch_angle = 0
start = 0
altitude_meters = 0
takeoff_throttle = 0
actual_compass_heading = 0
heading_lock = 0
number_used_sats = 0
fix_type = 0
l_lat_gps = 0
l_lon_gps = 0
adjustable_setting_1 = 0
adjustable_setting_2 = 0
adjustable_setting_3 = 0

def hexshow(data):
    e = 0
    for i in data:
        d = ord(i)
        e = e*256 + d
    return e
 
def get_data():
    global max_altitude_meters, hex_buffer, receive_buffer

    global error, flight_mode, battery_voltage, temperature, roll_angle, pitch_angle, start, altitude_meters, takeoff_throttle   
    global actual_compass_heading, heading_lock, number_used_sats, fix_type, l_lat_gps, l_lon_gps, adjustable_setting_1, adjustable_setting_2, adjustable_setting_3
    for i in range(34):
        hex_buffer[i] = hexshow(receive_buffer[i])
    #print hex_buffer
    #print receive_buffer
 
    check_byte = 0;
    for temp_byte in range(30):
        check_byte ^= hex_buffer[temp_byte]
 
    if check_byte == hex_buffer[31]:
        error = hex_buffer[0]
        flight_mode = hex_buffer[1]
        battery_voltage = (float)(hex_buffer[2])/10.0
        temperature = hex_buffer[3] | ( hex_buffer[4]<<8)
        roll_angle = hex_buffer[5] - 100
        pitch_angle = hex_buffer[6] - 100
        start = hex_buffer[7]
        altitude_meters = (hex_buffer[8] | hex_buffer[9] << 8) - 1000
        if altitude_meters > max_altitude_meters:
            max_altitude_meters = altitude_meters
        takeoff_throttle = hex_buffer[10] | hex_buffer[11] << 8
        actual_compass_heading = hex_buffer[12] | hex_buffer[13] << 8
        heading_lock = hex_buffer[14]
        number_used_sats = hex_buffer[15]
        fix_type = hex_buffer[16]
        l_lat_gps = hex_buffer[17] | hex_buffer[18] << 8 | hex_buffer[19] << 16 | hex_buffer[20] << 24
        l_lon_gps = hex_buffer[21] | hex_buffer[22] << 8 | hex_buffer[23] << 16 | hex_buffer[24] << 24
        adjustable_setting_1 = (float)(hex_buffer[25] | hex_buffer[26] << 8) / 100.0;
        adjustable_setting_2 = (float)(hex_buffer[27] | hex_buffer[28] << 8) / 100.0;
        adjustable_setting_3 = (float)(hex_buffer[29] | hex_buffer[30] << 8) / 100.0;

class receiving_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        global sock, received_data, receive_buffer_counter, receive_start_detect, receive_buffer
        global receive_byte_previous, max_altitude_meters
        while self.running:
            data = sock.recv(50)
            if data:
                if received_data == 0:
                    received_data = 1
                for nextByte in data:
                    if nextByte >= 0:
                        receive_buffer[receive_buffer_counter] = nextByte     
                    if receive_byte_previous == 'J' and receive_buffer[receive_buffer_counter] == 'B':
                        receive_buffer_counter = 0
                        receive_start_detect = receive_start_detect + 1
                        if receive_start_detect >= 2:
                            get_data()
                    else:
                        receive_byte_previous = receive_buffer[receive_buffer_counter]
                        receive_buffer_counter = receive_buffer_counter + 1
                        if (receive_buffer_counter > 48):
                            receive_buffer_counter = 0
            else:
                print "trying reconnect to server"
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((HOST, PORT))
                #receive_buffer_counter = 0
                #receive_start_detect = 0

    def stop(self):
        self.running = False
        if sock != None:
            sock.close()

class Watch(Frame):
    msec = 1000
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._running = False
        self.err_str = StringVar()
        self.flight_mode_str = StringVar()
        self.bat_volt_str = StringVar()
        self.temp_str = StringVar()
        self.roll_str = StringVar()
        self.pitch_str = StringVar()
        self.start_str = StringVar()
        self.alti_str = StringVar()
        self.takeoff_str = StringVar()
        self.compass_str = StringVar()
        self.head_lock_str = StringVar()
        self.num_sat_str = StringVar()
        self.fix_type_str = StringVar()
        self.lat_str = StringVar()
        self.lon_str = StringVar()
        self.adj_1_str = StringVar()
        self.adj_2_str = StringVar()
        self.adj_3_str = StringVar()
        self.makeWidgets()
        self.pack(side = TOP)
    def makeWidgets(self):
        error_label = Label(self, textvariable = self.err_str)
        error_label.configure(width=30, height=1)
        error_label.pack(side = TOP)

        flight_mode_label = Label(self, textvariable = self.flight_mode_str)
        flight_mode_label.configure(width=30, height=1)
        flight_mode_label.pack(side = TOP)

        battery_voltage_label = Label(self, textvariable = self.bat_volt_str)
        battery_voltage_label.configure(width=30, height=1)
        battery_voltage_label.pack(side = TOP)

        temperature_label = Label(self, textvariable = self.temp_str)
        temperature_label.configure(width=30, height=1)
        temperature_label.pack(side = TOP)

        roll_angle_label = Label(self, textvariable = self.roll_str)
        roll_angle_label.configure(width=30, height=1)
        roll_angle_label.pack(side = TOP)

        pitch_angle_label = Label(self, textvariable = self.pitch_str)
        pitch_angle_label.configure(width=30, height=1)
        pitch_angle_label.pack(side = TOP)

        start_label = Label(self, textvariable = self.start_str)
        start_label.configure(width=30, height=1)
        start_label.pack(side = TOP)

        altitude_meters_label = Label(self, textvariable = self.alti_str)
        altitude_meters_label.configure(width=30, height=1)
        altitude_meters_label.pack(side = TOP)

        takeoff_throttle_label = Label(self, textvariable = self.takeoff_str)
        takeoff_throttle_label.configure(width=30, height=1)
        takeoff_throttle_label.pack(side = TOP)

        actual_compass_heading_label = Label(self, textvariable = self.compass_str)
        actual_compass_heading_label.configure(width=30, height=1)
        actual_compass_heading_label.pack(side = TOP)

        heading_lock_label = Label(self, textvariable = self.head_lock_str)
        heading_lock_label.configure(width=30, height=1)
        heading_lock_label.pack(side = TOP)

        number_used_sats_label = Label(self, textvariable = self.num_sat_str)
        number_used_sats_label.configure(width=30, height=1)
        number_used_sats_label.pack(side = TOP)

        fix_type_label = Label(self, textvariable = self.fix_type_str)
        fix_type_label.configure(width=30, height=1)
        fix_type_label.pack(side = TOP)

        l_lat_gps_label = Label(self, textvariable = self.lat_str)
        l_lat_gps_label.configure(width=30, height=1)
        l_lat_gps_label.pack(side = TOP)

        l_lon_gps_label = Label(self, textvariable = self.lon_str)
        l_lon_gps_label.configure(width=30, height=1)
        l_lon_gps_label.pack(side = TOP)

        adjustable_setting_1_label = Label(self, textvariable = self.adj_1_str)
        adjustable_setting_1_label.configure(width=30, height=1)
        adjustable_setting_1_label.pack(side = TOP)

        adjustable_setting_2_label = Label(self, textvariable = self.adj_2_str)
        adjustable_setting_2_label.configure(width=30, height=1)
        adjustable_setting_2_label.pack(side = TOP)

        adjustable_setting_3_label = Label(self, textvariable = self.adj_3_str)
        adjustable_setting_3_label.configure(width=30, height=1)
        adjustable_setting_3_label.pack(side = TOP)

       
        
    def _update(self):
        self._settime()
        self.timer = self.after(self.msec, self._update)
    def _settime(self):
        #string_null = "null"
        global error, flight_mode, battery_voltage, temperature, roll_angle, pitch_angle, start, altitude_meters, takeoff_throttle   
        global actual_compass_heading, heading_lock, number_used_sats, fix_type, l_lat_gps, l_lon_gps, adjustable_setting_1, adjustable_setting_2, adjustable_setting_3
        self.err_str.set(str(error))
        self.flight_mode_str.set(str(flight_mode))
        self.bat_volt_str.set(str(battery_voltage))
        self.temp_str.set(str(temperature))
        self.roll_str.set(str(roll_angle))
        self.pitch_str.set(str(pitch_angle))
        self.start_str.set(str(start))
        self.alti_str.set(str(altitude_meters))
        self.takeoff_str.set(str(takeoff_throttle))
        self.compass_str.set(str(actual_compass_heading))
        self.head_lock_str.set(str(heading_lock))
        self.num_sat_str.set(str(number_used_sats))
        self.fix_type_str.set(str(fix_type))
        self.lat_str.set(str(l_lat_gps))
        self.lon_str.set(str(l_lon_gps))
        self.adj_1_str.set(str(adjustable_setting_1))
        self.adj_2_str.set(str(adjustable_setting_2))
        self.adj_3_str.set(str(adjustable_setting_3))

    def start(self):
        global recv_t
        self._update()
        
def exit_func():
    global recv_t
    recv_t.stop()
    recv_t.join()


 
if __name__ == '__main__':
    recv_t = receiving_thread()
    recv_t.start()
    root = Tk()
    root.title("ymfc monitor")
    root.geometry('800x600')
    frame_root = Frame(root)  
    frame_t = Frame(frame_root) 
    frame_m = Frame(frame_root) 
    frame_l = Frame(frame_m)  
    frame_r = Frame(frame_m) 
      
    mw = Watch(frame_r)
    mywatch = Button(frame_t, text = 'start', command = mw.start)
    mywatch.configure(width=30, height=1)
    mywatch.pack(side = TOP)
    
    exit = Button(frame_t, text = 'stop', command = exit_func)
    exit.configure(width=30, height=1)
    exit.pack(side = TOP)

    label_error = Label(frame_l, text="Error:")
    label_error.configure(width=30, height=1)
    label_error.pack(side = TOP)

    label_flight_mode = Label(frame_l, text="Flight mode:")
    label_flight_mode.configure(width=30, height=1)
    label_flight_mode.pack(side = TOP)

    label_battery_voltage = Label(frame_l, text="Battery voltage:" )
    label_battery_voltage.configure(width=30, height=1)
    label_battery_voltage.pack(side = TOP)

    label_temperature = Label(frame_l, text="temperature:")
    label_temperature.configure(width=30, height=1)
    label_temperature.pack(side = TOP)

    label_roll_angle = Label(frame_l, text="roll:")
    label_roll_angle.configure(width=30, height=1)
    label_roll_angle.pack(side = TOP)

    label_pitch_angle = Label(frame_l, text="pitch:")
    label_pitch_angle.configure(width=30, height=1)
    label_pitch_angle.pack(side = TOP)

    label_start = Label(frame_l, text="start:")
    label_start.configure(width=30, height=1)
    label_start.pack(side = TOP)

    label_altitude_meters = Label(frame_l, text="altitude:")
    label_altitude_meters.configure(width=30, height=1)
    label_altitude_meters.pack(side = TOP)

    label_takeoff_throttle = Label(frame_l, text="takeoff:")
    label_takeoff_throttle.configure(width=30, height=1)
    label_takeoff_throttle.pack(side = TOP)

    label_actual_compass_heading = Label(frame_l, text="compass heading:")
    label_actual_compass_heading.configure(width=30, height=1)
    label_actual_compass_heading.pack(side = TOP)

    label_heading_lock = Label(frame_l, text="head lock:")
    label_heading_lock.configure(width=30, height=1)
    label_heading_lock.pack(side = TOP)

    label_number_used_sats = Label(frame_l, text="sats:")
    label_number_used_sats.configure(width=30, height=1)
    label_number_used_sats.pack(side = TOP)

    label_fix_type = Label(frame_l, text="fix type:")
    label_fix_type.configure(width=30, height=1)
    label_fix_type.pack(side = TOP)

    label_l_lat_gps = Label(frame_l, text="Lat:")
    label_l_lat_gps.configure(width=30, height=1)
    label_l_lat_gps.pack(side = TOP)

    label_l_lon_gps = Label(frame_l, text="Lon:")
    label_l_lon_gps.configure(width=30, height=1)
    label_l_lon_gps.pack(side = TOP)

    label_adjustable_setting_1 = Label(frame_l, text="adjustable setting 1:")
    label_adjustable_setting_1.configure(width=30, height=1)
    label_adjustable_setting_1.pack(side = TOP)

    label_adjustable_setting_2 = Label(frame_l, text="adjustable setting 2:")
    label_adjustable_setting_2.configure(width=30, height=1)
    label_adjustable_setting_2.pack(side = TOP)

    label_adjustable_setting_3 = Label(frame_l, text="adjustable setting 3:")
    label_adjustable_setting_3.configure(width=30, height=1)
    label_adjustable_setting_3.pack(side = TOP)

    frame_l.pack(side=LEFT)
    frame_r.pack(side=RIGHT)
    frame_t.pack(side=TOP)
    frame_m.pack(side=TOP)
    frame_root.pack() 
    
    root.mainloop()

   

