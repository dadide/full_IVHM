import cantools
#import processmainFun # comment out for testing 
import time
import platform
import numpy as np
from ctypes import *


#-------------------------------------Load dynamic lib-----------------------------------------
#db2 = cantools.database.load_file('./VEHICLE/20151030-zx4_AS22_EP_HSC1-V18.dbc')
db2 = cantools.database.load_file('./XianSensor/Xian_Acc2.dbc')

canDLL = cdll.LoadLibrary('./Ccode/libusbcan.so')
MyDLL = cdll.LoadLibrary('./XianSensor/Xian_Sensor.so')

date = '__date__poped__'




#--------------------------------Config can device function---------------------------------------------------
def input_thread():
   input()

# FOR sensor data receive
class DBC_INFO(Structure):
	_fields_ = [("matrix_column_value", c_int),
				("matrix_row", c_int),
				("filled_column", c_int),
				("matrix_row_value", c_int),
				("timestamp",c_int)#int timestamp;
				]


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
     init_config.AccCode    = 0
     init_config.AccMask    = 0xFFFFFFFF
     init_config.Reserved   = 0
     init_config.Filter     = 1
     init_config.Timing0    = 0x00
     init_config.Timing1    = Brate
     init_config.Mode       = 0
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




def receive_date():
	global date
	return date


def receive_data(matptr, calcul_batch, frequ):

	recei_stime = receive_date()  # the start time of receiving data


# --------------------------------flag setting----------------------------------------
	Addr=0
	TimeFlag = 1
	sRunFlag = 0
	eRunFlag = 0
	spd_flag = 0

	while 1:

		# --------------------------get current time---and---initial speed-------------------------------
#		if TimeFlag or sRunFlag :
#			time.sleep(1)
#			max_vehicle_num_ini = canDLL.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL1) # preview the number of data in cache 
#			print(max_vehicle_num_ini)
#			if max_vehicle_num_ini:
#				obj_vehicle_ini=(ZCAN_CAN_OBJ*max_vehicle_num_ini)() # struct of data, timestamp, ID
#				act_vehicle_num_ini = canDLL.VCI_Receive(USBCAN2,DEVICE_INDEX,CHANNEL1,byref(obj_vehicle_ini),max_vehicle_num_ini, 100)


				# -------------------------------get current time--------------------------------------
#				if TimeFlag == 1:
#					count = 0
#					while count < act_vehicle_num_ini:
#						if (obj_vehicle_ini[count].ID == 0x1a1): # ID of time channel
#							ms_time = db2.decode_message(obj_vehicle_ini[count].ID, obj_vehicle_ini[count].Data)
#							global date
#							date = ''
#							for k, v in ms_time.items():
#								if k == 'Acc_Z':
#									print('Acc_Z')
#									print(v)
#							TimeFlag=0
#							recei_stime=date
#							break
#						count = count + 1
                                # finish obtaing time, timeflag=0

				# --------------------------------get initial speed---------------------------------------
#				if sRunFlag == 1:
#					count = 0
#					while count < ret:
#						if (obj_vehicle_ini[count].ID == 0x353):  # ID of speed channel
#							ms_spd = db2.decode_message(obj_vehicle_ini[count].ID, obj_vehicle_ini[count].Data)
#							for k, v in ms_spd.items():
#								if k == 'VehSpdAvgDrvn_h1HSC1':  # name of speed channel VehSpdAvgDrvn_h1HSC1
#									if v == 'km/h (0x0 - 0x7FFF)':
#										start_spd = 0
#									else:
#										start_spd = float(v)
									# message = ' Start SPEED is '+str(start_spd) + ' !   Count is ' + str(count) + ' . ret is ' + str(ret) # processmainFun.get_time() +
									# processmainFun.log_write_print(message, debug_flag=1, process_index=0, message_flag=3)
#									sRunFlag = 0
#									#eRunFlag = 1
#							break
#						count = count + 1
			        # finish obtaing time, srunFlag=0

		# ------------------------------------get data matrix--------------------------------------------
		max_sensor_num = canDLL.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL1) # preview the number of data in cache 
		if max_sensor_num:
			obj_sensor=(ZCAN_CAN_OBJ*max_sensor_num)() # struct of data, timestamp, ID
			act_sensor_num = canDLL.VCI_Receive(USBCAN2,DEVICE_INDEX,CHANNEL1,byref(obj_sensor),max_sensor_num, 100)
		#ret2 = canDLL.VCI_Receive(VCI_USBCAN2, 0, 1, byref(vci_can_obj_data,Addr*sizeof(VCI_CAN_OBJ)), 2500, 0)
		# print(Addr, min(2500, calcul_batch*frequ*6-Addr), ret_num, ret2)

			time.sleep(0.1)
			Addr=Addr+act_sensor_num
			print(Addr)
			if Addr >= calcul_batch*frequ:

				break
			dbc_info = DBC_INFO(3, 0, 0, calcul_batch*frequ,0)
			MyDLL.DBC_Decode(byref(obj_sensor), Addr, matptr, byref(dbc_info)) #time 0.01s
#

	# -------------------------------------get final speed--------------------------------------------
#	dwRel=canDLL.VCI_ClearBuffer(USBCAN2,DEVICE_INDEX,CHANNEL1) # clear buffer 
#	while 1:	
#		if eRunFlag == 1:
		
#			max_vehicle_num_fin = canDLL.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL1) # preview the number of data in cache 
#			obj_vehicle_fin=(ZCAN_CAN_OBJ*ret_num)() # struct of data, timestamp, ID
#			act_vehicle_num_fin = canDLL.VCI_Receive(USBCAN2,DEVICE_INDEX,CHANNEL1,byref(obj_vehicle_fin),max_vehicle_num_fin, 0)  
#			if act_vehicle_num_fin > 0:
#				count = 0
#				while count < act_vehicle_num_fin:
#					if (obj_vehicle_fin[count].ID == 0x353): # index of speed channel
#						ms_spd = db2.decode_message(obj_vehicle_fin[count].ID, obj_vehicle_fin[count].Data)
#						for k, v in ms_spd.items():
#							if k == 'VehSpdAvgDrvn_h1HSC1':  # name of speed channel VehSpdAvgDrvn_h1HSC1
#								if v == 'km/h (0x0 - 0x7FFF)':
#									final_spd = 0
#									break
#								else:
#									final_spd = float(v)
#									break
#							# message = ' Final SPEED is ' + str(final_spd) + ' !   Count is ' + str(count) + ' . ret3 is ' + str(ret3) # processmainFun.get_time() +
#							# processmainFun.log_write_print(message, debug_flag=1, process_index=0, message_flag=3)
#						eRunFlag=0
#						break
#					count=count+1
#		if eRunFlag == 0:
#			break
# ------------------------------------------------determine speed flag based on start_spd and final_spd-------------------------
#	if start_spd + final_spd > 5:
#		spd_flag = 1

	# print('Loooooooook : recei_stime  and  spd_flag: ', recei_stime, spd_flag)
#	return (recei_stime, spd_flag)

def p0End():
	canDLL.VCI_CloseDevice(USBCAN2,DEVICE_INDEX,CHANNEL0)
	canDLL.VCI_CloseDevice(USBCAN2,DEVICE_INDEX,CHANNEL1)

# --------------------------------------------------just for testing---------------------------------------------------------
if __name__ == '__main__':

# ----------------------------   run can device config-------------------------------------------


	# ----------------------------can device parameter setting--------------------------------------------------- 
	ZCAN_DEVICE_TYPE  = c_uint32
	ZCAN_DEVICE_INDEX = c_uint32
	ZCAN_Reserved     = c_uint32
	ZCAN_CHANNEL      = c_uint32
	LEN               = c_uint32

	USBCAN2       =   ZCAN_DEVICE_TYPE(4)
	DEVICE_INDEX  =   ZCAN_DEVICE_INDEX(0)
	Reserved      =   ZCAN_Reserved(0)

# specify which channel to receive data 0--> channel 0      1--> channel 1
	CHANNEL0       =   ZCAN_CHANNEL(0) # for receiving acceleration 
	CHANNEL1       =   ZCAN_CHANNEL(1) # for receiving time and speed 

	Brate0=0x14 # bode rate for channel 0 
	Brate1=0x14 # bode rate for channel 1
# close can if they open unexpectally 
	bRel0=canDLL.VCI_CloseDevice(USBCAN2,DEVICE_INDEX, CHANNEL0) # close can 1
	bRel1=canDLL.VCI_CloseDevice(USBCAN2,DEVICE_INDEX, CHANNEL1)  # close can 2

# open device
	open_flag=canDLL.VCI_OpenDevice(USBCAN2,DEVICE_INDEX,Reserved) # open device 
	
	if open_flag ==0:
	 	print("Opendevice fail!")
	else:
     		print("Opendevice success!")

# start can 
	canstart0 = can_start(USBCAN2,DEVICE_INDEX,CHANNEL0,Brate0) # start can 0
	canstart1 = can_start(USBCAN2,DEVICE_INDEX,CHANNEL1,Brate1) # start can 1

# define buffer 
#vci_can_obj_time = (VCI_CAN_OBJ * 2500)()  # Buffer
#vci_can_obj_data = (VCI_CAN_OBJ * 100000)()  # Buffer

# -------------------------------mock ------------------------------------------
	frequ = 512  		# sample frequency
	calcul_batch = 2  	# calculate batch time
	nIn_a = 3  		# the input number of A model

	mat = np.zeros([frequ*calcul_batch, nIn_a], np.float64)
	# get the pointer of a smat
	tmp = np.asarray(mat)
	dataptr = tmp.ctypes.data_as(POINTER(c_double))
	try:
		receive_data(dataptr, calcul_batch, frequ)
		for _data in dataptr:
			print(_data)
	except(KeyboardInterrupt):
		p0End()
		print("Finished Successfully")
