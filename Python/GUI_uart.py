import tkinter as tk
import serial
import threading
import time
import os
import csv

serial_data = ''
filter_data = ''
update_period = 5
serial_object = None
Start_write_flag=1
csvfile_path = "C:\\Users\MKND\Desktop\Test_csv.csv"

def connect(port_entry_name,baud_entry_name):
	"""The function initiates the Connection to the UART device with the Port and Buad fed through the Entry
    boxes in the application.Some Exceptions have been made to prevent the app from crashing,
    such as blank entry fields and value errors, this is due to the state-less-ness of the UART device, the device sends data at regular intervals irrespective of the master's state.The other Parts are self explanatory."""
	#version_but = button_var.get()
	port='COM5'
	baud=115200
	global serial_object
	global Start_write_flag

	port = port_entry_name
	baud = baud_entry_name
	try:
		"""if version_but == 2:
			serial_object = serial.Serial('/dev/tty' + str(port), baud) 	##FOR LINUX
		elif version_but == 1:
			erial_object = serial.Serial('COM5', baud)"""					##FOR WINDOWS
		serial_object = serial.Serial(port, baud)
	except:
		print('SerialPort open Error for:\n\r Baud=',baud_entry_name,' and Port=',port_entry_name)
		return
	else:
		print('Serial_Port successfully opened')
		Start_write_flag=1
	t1 = threading.Thread(target = get_uart_data)
	t1.daemon = True
	t1.start()


def get_uart_data():
	#strip=strips chars at end and strt of str;;	split=converts str to list using delimiters;;	decode=converts bytes obj [b'0x0032'] to str
	#filter_data=  serial_data.strip(b'_/n/r').decode().split('_') 			#give	['temp','lux']
	#Function reads USART data-->pushes to .CSV file
	#					  aand-->sets global filter_data~~['temp','lux','h:m']------> gets used later
	global serial_object
	global filter_data
	global Start_write_flag
	while(1):
		if not serial_object.isOpen():
			print("Port closed")
			return
		try:
			if serial_object.isOpen():
				serial_data = serial_object.readline()
				#print('port read')
				print(serial_data)
			else:
				Start_write_flag=0
				return
			#filter_data = serial_data.strip().decode().replace(' ','').split(',')
			#For data in form->b'_38.2_78787_\r\n'
			#print(serial_data.strip(b'_\n\r').decode().split('_'))
			filter_data=  serial_data.strip(b'_\n\r').decode().split('_')
							#gives	['temp','lux']
			#check data aand publish back#
			
			filter_data.append("{}".format(time.strftime('%I:%M')))
							#gives	filter_data~~['temp','lux','h:m']
			print(filter_data)
			#if filter_data[0]:
			#	serial_object.write(b'!\n')
			#----------#
			#serial_object.write(b'd')
			#if serial_object.isOpen():
			with open(csvfile_path, mode='a',newline='') as csv_file:
				csv_writer = csv.writer(csv_file, delimiter=',')
				#if Start_write_flag:
				if filter_data[0]:
					csv_writer.writerow(filter_data)
			
		except TypeError:
			pass


def send_uart_data(send_dat):
	#send to μC
	###can send data from textbox-->data is always converted into ASCII
	global serial_object
	if not send_dat:
		send_dat="test"
	serial_object.write(b'!')



def update_ui(tb_name1,temp_disp_val,lite_disp_val):
	'''update(txtArea,)
	Appends TextArea, sets Curr. Temp&Light values
	Threaded update function
	gets data and applies on ui. !### Auto refresh ".after()" not usedin this example
	'''
	global filter_data
	global update_period
	global all_csvdata_list
	global time_list
	
	#UPDATE GUI
	while (1):
		if Start_write_flag:	
			if filter_data[0]:
				time_list=[] 				#clear Gui variable
				#print(filter_data)
				tb_name1.insert('end',filter_data)
				tb_name1.insert('end','\n')
				temp_disp_val.config(text=filter_data[0])
				lite_disp_val.config(text=filter_data[1])
				#Populate a List object to get all time values
				#global all_csvdata_list
				with open(csvfile_path, mode='r',newline='') as csv_file:
					csv_reader = csv.reader(csv_file, delimiter=',')
					all_csvdata_list=list(csv_reader)
				#GOT LIST OF ALL CSV DATA--->all_csvdata_list---->[['Temperature', 'Light', 'Time'],[temp,lite,t1]...#
				#print('time')
				for i in range(1,length):
					print(all_csvdata_list[i][2])
					time_list.append(all_csvdata_list[i][2])
				#GOT LIST OF ALL CSV Time.Has 1 offset than all_csvdata_list!!!! ---->[t1,t2...]#
				print(time_list)
				'''Update list in UI'''

				


def disconnect():    
	""" 
	This function is for disconnecting and quitting the application
	Sometimes the application throws a couple of errors while it is being shut down, the fix isn't out yet
	simple GUI.quit() calls
	"""
	global Start_write_flag
	Start_write_flag=0
	try:
		serial_object.close()
	except AttributeError:
		print("Error in Disconnecting -_-")
	else:
		print("Disconnected")
		return
	#gui.quit()


if __name__=="__main__":
	#gui = tk.Tk()
	#gui.title("UART Interface")
	tb_1=tk.Text(gui,bg='cyan',width=5,height=10)
	tb_try=tk.Text(gui,bg='blue',width=10,height=5)
	tb_1.pack()
	tb_1.insert('end',"Holoa \n")
	tb_1.place(x=0,y=0)
	tb_try.place(x=50,y=0)
	tb_name1=tb_1
	tb_name2=tb_try
	#needs to be at end of everything
	#gui.mainloop()