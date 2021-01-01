
process0_test_flag = 0
if process0_test_flag != 1:
	print('The IVHM is running... Not test code!\n')
else:
	print('Test code is running... Generate data!\n')

import os
import time
import numpy as np
# import processmainFun
import process0Fun_test_speed


def new_get_time():
	# Func : to get the current time
	time_tup = time.localtime(time.time())
	format_time='%Y_%m_%d_%H_%M_%S'		#2020_12_08_13_59_47
	cur_time = time.strftime(format_time, time_tup)
	return cur_time


def process0_fun_test2(speed_result_length, interval, debug_flag):

	speed_result = np.zeros([speed_result_length, 1], np.float32)

	v_index = 0

	while True:
		if v_index == speed_result_length-1:
			v_index = 0
			curr_time = new_get_time()
			

			#-----------------------------------------------
			# add this to create the folder
			# judge if the folder exists
			# '%Y_%m_%d_%H_%M_%S'		
			curr_day = curr_time[5:10]	#2020_12_08_13_59_47
			curr_hour = curr_time[5:13]
			folder_path = './speed/'+curr_day
			# folder_path = './speed/'+curr_day+'/'+curr_hour
			isExist = os.path.exists(folder_path)
			if not isExist:
				os.makedirs(folder_path)
			#-----------------------------------------------

			speed_file_name = folder_path + '/speed_result_' + curr_time + '.csv'
			with open(speed_file_name, 'w') as f:
				np.savetxt(f, speed_result, fmt='%.4f')	 #, delimiter=','


			file_list = os.listdir(folder_path)
			print( 'length:' + str(len(file_list)) )
			if file_list != []:
				for i in range (0, min(3, len(file_list))):
					command = 'sshpass -p 123 scp -C /IVHM/' + folder_path + '/' + file_list[i] + ' ' + ' wy@202.121.180.27:/home/wy/matlab_example/scpTest/speed/'
					print(command)
					exit_code = os.system(command)
					if exit_code == 0:
						rm_exit_code = os.remove('/IVHM/' + folder_path + '/' + file_list[i])
						message = folder_path + '/' + file_list[i] + ' uploaded successfully and removed!!!'
						print(message)
					else:
						message = folder_path + '/' + file_list[i] + ' uploaded Failed Failed Failed!!!'
						print(message)
						break
			else:
				print('No files to upload')

			# #upload('speed_result.csv')
			# command = 'sshpass -p 123 scp -C /IVHM/' + speed_file_name + ' wy@202.121.180.27:/home/wy/matlab_example/scpTest/speed/'
			# print(command)
			# exit_code = os.system(command)

			# if exit_code == 0:
			# 	 rm_exit_code = os.remove('/IVHM/' + speed_file_name)
			# 	 message = curr_time + ' speed_result.csv uploaded successfully and removed!!!rm_exit_code:'
			# 	 print(message+str(rm_exit_code))
			# else:
			# 	message = ' speed_result.csv uploaded Failed Failed Failed!!!'
			# 	# processmainFun.log_write_print(message, debug_flag, process_index=0, message_flag=3)

			
		else :
			v_index = v_index + 1

		speed_result[v_index] = np.random.rand(1, 1)
		print('main' + str(speed_result[v_index]))
		time.sleep(interval)



def process0_fun(speed_result_length, interval, debug_flag):
	# Func: receive data from can(in the real car system)
	# version 1.0 : receive data from real sensor


	speed_result = np.zeros([speed_result_length, 1], np.float32)

	v_index = 0

	while True:

		try:
			if v_index == speed_result_length-1:

				curr_time = new_get_time()
				print(curr_time)

				#-----------------------------------------------
				# add this to create the folder
				# judge if the folder exists
				# '%Y_%m_%d_%H_%M_%S'		
				curr_day = curr_time[5:10]	#2020_12_08_13_59_47
				curr_hour = curr_time[5:13]
				folder_path = './speed/'+curr_day+'/'+curr_hour
				isExist = os.path.exists(folder_path)
				if not isExist:
					os.makedirs(folder_path)
				#-----------------------------------------------
				speed_file_name = folder_path + '/speed_result_' + curr_time + '.csv'

				with open(speed_file_name, 'w') as f:
					np.savetxt(f, speed_result, fmt='%.4f')	 #, delimiter=','


				file_list = os.listdir(folder_path)
				print( 'length:' + str(len(file_list)) )
				if file_list != []:
					for i in range (0, min(3, len(file_list))):
						command = 'sshpass -p 123 scp -C -P 22 /IVHM/' + folder_path + '/' + file_list[i] + ' ' + ' wy@202.121.180.27:/home/wy/matlab_example/scpTest/speed/ '
						print(command)
						exit_code = os.system(command)
						if exit_code == 0:
							rm_exit_code = os.remove('/IVHM/' + folder_path + '/' + file_list[i])
							message = folder_path + '/' + file_list[i] + ' uploaded successfully and removed!!!'
							print(message)
						else:
							message = folder_path + '/' + file_list[i] + ' uploaded Failed Failed Failed!!!'
							print(message)
							break
				else:
					print('No files to upload')

				# #upload('speed_result.csv') with scp
				# command = 'sshpass -p 123 scp -C /IVHM/' + speed_file_name + ' wy@202.121.180.27:/home/wy/matlab_example/scpTest/speed/'
				# exit_code = os.system(command)
				# if exit_code == 0:
				# 	 rm_exit_code = os.remove('/IVHM/' + speed_file_name)
				# 	 message = curr_time + ' speed_result.csv uploaded successfully and removed!!!rm_exit_code:'
				# 	 print(message+str(rm_exit_code))
				# 	 # processmainFun.log_write_print(message, debug_flag, process_index=0, message_flag=3)
				# else:
				# 	 message = curr_time + ' speed_result.csv uploaded Failed Failed Failed!!!'
				# 	 print(message)
				# 	 # processmainFun.log_write_print(message, debug_flag, process_index=0, message_flag=3)

				v_index = 0

			else :
				v_index = v_index + 1

			spd_tmp = np.float32(process0Fun_test_speed.receive_data())
			if abs(spd_tmp + 1) > 0.001:
				speed_result[v_index] = spd_tmp
				print('main' + str(speed_result[v_index]))
				time.sleep(interval)
			else:
				print('main no data in the stack')

		except(KeyboardInterrupt):
			process0Fun_test_speed.p0End()
			print("Finished Successfully")
			break



if __name__ == '__main__':

	# path variables, which are different in PC and Gateway
	root_path = "/IVHM/"
	# root_path = "/home/wy/IVHM_code/newest/"
	theta_path = "MTheta/"  # relative path to the root_path
	resu_path = "result/"  # relative path to the root_path
	txt_path = "txt/"
	input_path = "input/"
	# log_path = "log/"		# defined in the processmainFun.py

	# variables of thread2 :
	server_ip = "202.121.180.27"
	user_name = "wy"
	remote_path = "/home/wy/matlab_example/scpTest/"

	# other variables
	debug_flag = 1


	speed_result_length = 100
	interval = 0.1


	if process0_test_flag == 1:
		process0 = process0_fun_test2(speed_result_length, interval, debug_flag)
	else:
		process0 = process0_fun(speed_result_length, interval, debug_flag)
