import cantools
import time
import platform
import numpy as np
from ctypes import *


#--------------------------------Config can device function---------------------------------------------------
def input_thread():
   input()

def p0End():
	canDLL.VCI_CloseDevice(USBCAN2,DEVICE_INDEX,CHANNEL0)
	canDLL.VCI_CloseDevice(USBCAN2,DEVICE_INDEX,CHANNEL1)

class ZCAN_CAN_INIT_CONFIG(Structure):
	_fields_ = [("AccCode",c_int),
				("AccMask",c_int),
				("Reserved",c_int),
				("Filter",c_ubyte),
				("Timing0",c_ubyte),
				("Timing1",c_ubyte),
				("Mode",c_ubyte)]

class ZCAN_CAN_OBJ(Structure):
	_fields_ = [("ID",c_uint32),
				("TimeStamp",c_uint32),
				("TimeFlag",c_uint8),
				("SendType",c_byte),
				("RemoteFlag",c_byte),
				("ExternFlag",c_byte),
				("DataLen",c_byte),
				("Data",c_ubyte*8),
				("Reserved",c_ubyte*3)]


def can_start(DEVCIE_TYPE,DEVICE_INDEX,CHANNEL,Brate):
	 init_config  = ZCAN_CAN_INIT_CONFIG()
	 init_config.AccCode	= 0
	 init_config.AccMask	= 0xFFFFFFFF
	 init_config.Reserved   = 0
	 init_config.Filter	 = 1
	 init_config.Timing0	= 0x00
	 init_config.Timing1	= Brate
	 init_config.Mode	   = 0
	 # Initialize the  Can channel 
	 Init_flag=canDLL.VCI_InitCAN(DEVCIE_TYPE,DEVICE_INDEX,CHANNEL,byref(init_config))
	 if Init_flag ==0:
		 print("InitCAN fail!")
	 else:
		 print("InitCAN success!")
	  #Start  Can channel	
	 start_flag=canDLL.VCI_StartCAN(DEVCIE_TYPE,DEVICE_INDEX,CHANNEL)
	 if start_flag ==0:
		 print("StartCAN fail!")
	 else:
		 print("StartCAN success!")
	 return start_flag


#-------------------------------------Load dynamic lib-----------------------------------------
db2 = cantools.database.load_file('./Ccode/180615-lh1-EP22MCE_CAN6-V10.Dbc')

canDLL = cdll.LoadLibrary('./Ccode/libusbcan.so')


date = '__date__poped__'

# ----------------------------can device parameter setting--------------------------------------------------- 
ZCAN_DEVICE_TYPE = c_uint32
ZCAN_DEVICE_INDEX = c_uint32
ZCAN_Reserved = c_uint32
ZCAN_CHANNEL = c_uint32
LEN = c_uint32

USBCAN2 = ZCAN_DEVICE_TYPE(4)
DEVICE_INDEX = ZCAN_DEVICE_INDEX(0)
Reserved = ZCAN_Reserved(0)

# specify which channel to receive data 0--> channel 0	  1--> channel 1
CHANNEL0 = ZCAN_CHANNEL(0)  # for receiving acceleration
CHANNEL1 = ZCAN_CHANNEL(1)  # for receiving time and speed

Brate0 = 0x14  # bode rate for channel 0        1000
Brate1 = 0x1C  # bode rate for channel 1       500
# close can if they open unexpectally
bRel0 = canDLL.VCI_CloseDevice(USBCAN2, DEVICE_INDEX, CHANNEL0)  # close can 1
bRel1 = canDLL.VCI_CloseDevice(USBCAN2, DEVICE_INDEX, CHANNEL1)  # close can 2

# open device
open_flag = canDLL.VCI_OpenDevice(USBCAN2, DEVICE_INDEX, Reserved)  # open device

if open_flag == 0:
	print("Opendevice fail!")
else:
	print("Opendevice success!")

# start can
canstart0 = can_start(USBCAN2, DEVICE_INDEX, CHANNEL0, Brate0)  # start can 0
canstart1 = can_start(USBCAN2, DEVICE_INDEX, CHANNEL1, Brate1)  # start can 1


# define buffer
# vci_can_obj_time = (VCI_CAN_OBJ * 2500)()  # Buffer
# vci_can_obj_data = (VCI_CAN_OBJ * 100000)()  # Buffer


def receive_data():

	start_spd = -1

	max_vehicle_num_ini = canDLL.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL1) # preview the number of data in cache 
	
	if max_vehicle_num_ini:
		obj_vehicle_ini=(ZCAN_CAN_OBJ*max_vehicle_num_ini)() # struct of data, timestamp, ID
		act_vehicle_num_ini = canDLL.VCI_Receive(USBCAN2,DEVICE_INDEX,CHANNEL1,byref(obj_vehicle_ini),max_vehicle_num_ini, 100)


		# -------------------------------get current time--------------------------------------
		# count = 0
		# while count < act_vehicle_num_ini:
		# 	if (obj_vehicle_ini[count].ID == 0x1a1): # ID of time channel
		# 		ms_time = db2.decode_message(obj_vehicle_ini[count].ID, obj_vehicle_ini[count].Data)
		# 		global date
		# 		date = ''
		# 		for k, v in ms_time.items():
		# 			if k == 'Acc_Z':
		# 				print('Acc_Z')
		# 				print(v)
		# 				speed = v
		# 		break
		# 	count = count + 1

		count = 0 # for initial speed
		while count < act_vehicle_num_ini:
			if (obj_vehicle_ini[count].ID == 0x353):  # ID of time channel
				ms_spd = db2.decode_message(obj_vehicle_ini[count].ID, obj_vehicle_ini[count].Data)
				for k, v in ms_spd.items():
					if k == 'VehSpdAvgDrvnHSC6':  # name of speed channel VehSpdAvgDrvn_h1HSC1
						if v == 'km/h (0x0 - 0x7FFF)':
							start_spd = 0
							print(start_spd)
						else:
							start_spd = float(v)

				break
			count = count + 1

	return start_spd


# def receive_data():

# # --------------------------------flag setting----------------------------------------
# 	Addr=0
# 	TimeFlag = 1
# 	sRunFlag = 0
# 	eRunFlag = 0
# 	spd_flag = 0

# 	while 1:
# 		try:
# 			speed = -1
# 			# --------------------------get current time---and---initial speed-------------------------------
# 			if TimeFlag or sRunFlag :
# 	#			time.sleep(1)
# 				max_vehicle_num_ini = canDLL.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL1) # preview the number of data in cache 
# 	#			print(max_vehicle_num_ini)
# 				if max_vehicle_num_ini:
# 					obj_vehicle_ini=(ZCAN_CAN_OBJ*max_vehicle_num_ini)() # struct of data, timestamp, ID
# 					act_vehicle_num_ini = canDLL.VCI_Receive(USBCAN2,DEVICE_INDEX,CHANNEL1,byref(obj_vehicle_ini),max_vehicle_num_ini, 100)


# 					# -------------------------------get current time--------------------------------------
# 					if TimeFlag == 1:
# 						count = 0
# 						while count < act_vehicle_num_ini:
# 							if (obj_vehicle_ini[count].ID == 0x1a1): # ID of time channel
# 								ms_time = db2.decode_message(obj_vehicle_ini[count].ID, obj_vehicle_ini[count].Data)
# 								global date
# 								date = ''
# 								for k, v in ms_time.items():
# 									if k == 'Acc_Z':
# 										print('Acc_Z')
# 										print(v)
# 										speed = v
# 	#							TimeFlag=0
# 	#							recei_stime=date
# 								break
# 							count = count + 1
# 			break
# 		except(KeyboardInterrupt):
# 			process0Fun_test_speed.p0End()
# 			print("Finished Successfully")
# 	return speed


