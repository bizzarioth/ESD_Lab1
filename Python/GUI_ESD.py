#---------------------------MAIN-----------------------------
import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
import serial
from serial import tools
from serial.tools import list_ports
import threading
import time
import os
import GUI_uart
import csv

global all_csvdata_list
global time_list

port_id='COM5'
baudrate=4800
#port_id=''
pastvalue=0		#in min, to get past data
csvfile_path = "C:\\Users\MKND\Desktop\Test_csv.csv"
#GET List of all Ports 				
ports = serial.tools.list_ports.comports(include_links=False)
port_list=['COM2']
for port,desc,hwid in ports:
	#print("{}: {} [{}]".format(port, desc, hwid))		//Get a list of all available ports
	port_list.append('{}'.format(port))
	print(port_list)

#-Call this once -------------------------------------#
with open(csvfile_path, mode='r',newline='') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	all_csvdata_list=list(csv_reader)
	#GOT LIST OF ALL CSV DATA--->all_csvdata_list---->[['Temperature', 'Light', 'Time'],[temp,lite,t1]...#
	#print('time')
	time_list=[]
	for i in range(1,len(all_csvdata_list)):
		#print(all_csvdata_list[i][2])
		time_list.append(all_csvdata_list[i][2])

if __name__=="__main__":
	main_gui = tk.Tk()
	main_gui.title("ESD Interface 2.0")

	
	#------TEMP Commands------------------
	def set_port(select):
		global port_id
		port_id=select
		print(port_id)
		#print(port_id)
	def set_baud(select):
		global baudrate
		baudrate=select
		#print(baudrate)
		
		##Temp BUTTON click
	def click_conn_but():
		#include this part 
		#port_id given by strvar.get() and baudrate=intvar.get()
		global port_id
		global baudrate
		port_id=strvar.get()
		baudrate=intvar.get()
		#print(baudrate)
		#print(port_id)
		GUI_uart.connect(port_id,baudrate)

	def click_discon_but():
		GUI_uart.disconnect()

	def click_CSVsearch():
		global all_csvdata_list
		print('hey Search pressed')
		'''	
		with open(csvfile_path, mode='r',newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			all_csvdata_list=list(csv_reader)
		for i in range(len(all_csvdata_list),0,-1):
			print('check')
			#compare str(time_req) with all_data[i][2]
		'''

	def click_testing():
		temperature_msg.config(text="gogo")

	#-------------------------------------#

	#FRAMES-------------------------------
	frame_1 = tk.Frame(main_gui, bd = 3, relief = 'groove')
	frame_2 = tk.Frame(main_gui,bd=4,relief = 'groove')
	frame_3 = tk.Frame(main_gui,bd=2,relief = 'groove')
	frame_2.grid(row=0,column=0,pady=15)
	frame_1.grid(row=1,column=0)
	frame_3.grid(row=2,column=0,pady=15)
	#-------------------------------------#

	#TEXTAREA-----------DISPLAY Serial O/P-------
	serial_disp=tk.scrolledtext.ScrolledText(frame_3,width=40,height=10)
	serial_disp.grid(column=0,row=0)
	serial_disp.insert('insert',"Serial Monitor : \r\n")
	#--------------------------------------------------------#

	#TEST BUTTON-------------------------------------#
	test_but=tk.Button(frame_3,text='TEST',command=click_testing)	#add connect() command| Now can pass port_id n baudrate directly
	test_but.grid()
	#--------------------------------------------------------#

	#LABELS----------------------------------------------------		[font=("Arial Bold", 50)]
	temperature_label=tk.Label(frame_1,text='Current temperature_label	:').grid(row=0,column=0,padx=15)
	light_label=tk.Label(frame_1,text='Current Light Intensity :').grid(row=1,column=0,padx=5)
	port_label=tk.Label(frame_2,text='COM-PORT :').grid(row=0,column=0)
	baud_label=tk.Label(frame_2,text='Baud Rate :').grid(row=0,column=2)

	temperature_past_label=tk.Label(frame_1,text='Old Temperature_label:').grid(row=4,column=0)		#below Spinbox
	light_past_label=tk.Label(frame_1,text='Old Light Intensity :').grid(row=4,column=1)
	
	pastvalue_label=tk.Label(frame_1,text='Show past data of : (mins)').grid(row=3,pady=10)	#below current value
	#--------------------------------------------------------#

	#-------Number of MINutes---------------------------------------#
		#--Listview/Combobox--[OPTION]--#
		#--SPINBOX IMPLEMENTATION---------------------#
	'''pastvalue=tk.IntVar()
				pastvalue_spinbox=tk.Spinbox(frame_1,textvariable=pastvalue,from_=2,to=10,increment=2,width=5)
				pastvalue_spinbox.grid(row=3,column=1,pady=10)
				print(pastvalue)'''
	#---------------------------------------------#
		#--LISTBOX IMPLEMENTATION---------------------#
	tk_list_var=tk.StringVar()
	tk_list_var.set(time_list)
	LB_TEST=tk.Listbox(frame_1,listvariable=tk_list_var,selectmode='SINGLE',height=4,width=8)
	LB_TEST.grid(row=3,column=1,pady=10)
	
	#---------------------------------------------#
	

	#----------------------------------------------------------------#
	#TEXTBOXs-{OUTPUTS}----------------------------------------------#
	temperature_val=38.2
	lighti_val=1234			#light intensity
	temperature_msg=tk.Message(frame_1,text=temperature_val,bd=3,relief='groove',bg='lightgreen')
	light_msg=tk.Message(frame_1,text=lighti_val,relief='groove',bg='yellow')

	temperature_past_msg=	tk.Message(frame_1,bd=3,relief='groove',bg='skyblue')
	light_past_msg=			tk.Message(frame_1 ,relief='groove',bg='purple')
		#placing Msgs
	temperature_msg.grid(row=0,column=1)				#along temperature_label
	light_msg.grid(row=1,column=1)

	temperature_past_msg.grid(row=5,column=0)			#below 	temperature_past_label
	light_past_msg.grid(row=5,column=1)
	#---------------------------------------------------------#

	#SERIAL_SETUP_INPUTS-------------------------------------------
		#---------------#EntryBoxes-----------------------------
	'''PORT_txt=tk.Entry(frame_2,width=10)
				BAUDR_txt=tk.Entry(frame_2,width=10)
				PORT_txt.grid(row=0,column=1)
				BAUDR_txt.grid(row=0,column=3)
				PORT_txt.insert('end','COM5')
					#get port and baudrate
				port_id=PORT_txt.get()
				baudrate=BAUDR_txt.get()'''
		#---------------#DROPDOWNs------------------------------
	'''fake' list_of_ports'''
	#list_of_ports=['COM6','COM3','COM5','COM2','COM7']
	list_of_ports=port_list
	list_of_baudrates=[9600,19200,38400,57600,74880,115200]
	strvar=tk.StringVar()
	strvar.set(list_of_ports[0])
	intvar=tk.IntVar()
	intvar.set(list_of_baudrates[0])
	
	PORT_OPmenu=tk.OptionMenu(frame_2,strvar,*list_of_ports,command=set_port)			
	BAUD_OPmenu=tk.OptionMenu(frame_2,intvar,*list_of_baudrates,command=set_baud)
	PORT_OPmenu.grid(row=0,column=1)
	BAUD_OPmenu.grid(row=0,column=3)
	port_id=strvar.get()	#putting default|redundant but safe
	baudrate=intvar.get()	#putting default|redundant but safe
	#---------------------------------------------------------------------#

	#BUTTONS-----------------------------------------------------------------		
	connect_button=tk.Button(frame_2,text='Connect',command=click_conn_but)	#add connect() command| Now can pass port_id n baudrate directly
	disconnect_button = tk.Button(frame_2,text = "Disconnect", command = click_discon_but)
	search_button=tk.Button(frame_1,text="Show", command=click_CSVsearch)
	
	connect_button.grid(row=1,column=0,columnspan=2)
	disconnect_button.grid(row=1,column=2,columnspan=2)
	search_button.grid(row=3,column=2,pady=10)
	#---------------------------------------------------------------------#

	#help(connect_button.grid)
	#print(PORT_txt.index('end'))	#gives index of last char==> 0 for none
	#mainloop
	#main_gui.geometry('500x500')
	main_gui.mainloop()
