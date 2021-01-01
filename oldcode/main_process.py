# after the experiment, some revisions should be done:

# 2020-8-30: before experiment
# multithreading -> multiprocessing
# the running efficiency can be improved

# 2020-9-2:
# upload_size_threshold -> upload_batch_num_thresholds

# 2020-9-9:
# upload the input data as well as predict result

# 2020-9-26:
# 1. demean the b_model's input and output
# 2. do not demean the a_model's input and output
# 3. add header_input_str to the input data
# 4. fix the bug -- the input.csv can not be deleted
# 5. delete the first 30 points from the file----Not Done Yet, and it doesn't important
# 6. get the number of abnormal data in 22 channels every week, save it to .csv and upload it


# 2020-10-17:
# 1. after getting the real threshold:the low bound and up bound is opposite number, so change the mat > abnorm_threshold to abs(mat) > abnorm_threshold
# 2. specify the threshold for every channel according the value provided by Qiuyu

# 2020-10-19 version 1.0:
# 1. put the process0 to main process, so the extra process number is 2

# 2020-10-20
# 1. process0Fun.py : start speed and final speed is read correctly
# 2. process0Fun.py : the logic to get spd_flag is written by myself, please check!

# ----------------------------------------------------------------------------------------
# Todo: remove the unnessary code from the code
# Done: get the GPS_speed from the sensor & add a judge function to decide whether the car is still or running
# Todo: the log file is not even???
# Todo: upgrade the model parameters

process0_test_flag = 0
if process0_test_flag != 1:
	print('The IVHM is running... Not test code!\n')
else:
	print('Test code is running... Generate data!\n')

import os
import time
import numpy as np
import processmainFun
import process0Fun
import process1Fun
import process2Fun
from ctypes import *
from multiprocessing import Process, Queue
import faulthandler;faulthandler.enable()
np.set_printoptions(threshold=np.inf)

r = 50  			# please constant with the training parameters
d = 0
nIn_a = 22  		# the input number of A model
frequ = 512  		# sample frequency
calcul_batch = 5  	# calculate batch time
abnorm_threshold = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 300, 300, 300, 300, 50, 50, 50, 50, 50, 50])
weekly_second = 60  # a week has 7*24*60*60 s, here is a smaller value to test if it works well


def process0_fun_test(que_mat, que_time, nIn_a, calcul_batch, frequ, debug_flag):
	# version 1.0 : generate data we need to test

	count = 1

	# -------- 2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------
	abnormal_result = np.zeros([1, nIn_a], np.int64)
	weekly_counter = weekly_second/calcul_batch		# a week's time needs weekly_count iteration
	# --------2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------

	while True:
		processmainFun.log_write_print(' * * * * * * Thread0_test: generate NO.%d data* * * * * * ' % count, debug_flag, process_index = 0, message_flag = 3)

		st = time.time()

		# generate data
		mat = np.arange(frequ*calcul_batch*nIn_a,dtype=np.float64).reshape(frequ*calcul_batch,nIn_a)

		# ---------2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------
		# ---------2020.10.17 after getting the real threshold:the low bound and up bound is opposite number, so change the mat > abnorm_threshold to abs(mat) > abnorm_threshold----
		abnormal_result = abnormal_result + np.sum( (abs(mat) > abnorm_threshold), axis=0)
		weekly_counter = weekly_counter - 1
		if weekly_counter == 0:
			weekly_counter = weekly_second/calcul_batch
			# write the numpy array to a csv file
			with open('abnormal_result.csv', 'a') as f:
				np.savetxt(f, abnormal_result, fmt='%d', delimiter=',')

			# upload the csv repeat
			command = ' sshpass -p 123 scp -C /IVHM/abnormal_result.csv wy@202.121.180.27:/home/wy/matlab_example/scpTest/'
			exit_code = os.system(command)
			if exit_code == 0:
				message = ' Abnormal_result.csv uploaded successfully!\n'
				processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
			else:
				message = ' Abnormal_result.csv uploaded Failed Failed Failed!!!\n'
				processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
		# ---------2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------
		mat_str = mat.tostring()
		que_mat.put(mat_str)

		cur_time = processmainFun.get_time()
		que_time.put(cur_time)
		et = time.time()

		# print message
		message = ' que_mat size : ' + str(que_mat.qsize()) + ' ;que_time size : ' + str(que_time.qsize()) + ' ;put time : ' + str(et-st)
		processmainFun.log_write_print(message, debug_flag, process_index=0, message_flag=3)

		count = count + 1
		if count > 13:
			break

		time.sleep(10)

	processmainFun.log_write_print(' ++++++++Thread0_test Finished!++++++++\n', debug_flag, process_index = 0, message_flag = 3)


def process0_fun(que_mat, que_time, nIn_a, calcul_batch, frequ, debug_flag):
	# Func: receive data from can(in the real car system)
	# version 1.0 : receive data from real sensor

	count = 1
	mat = np.zeros([frequ*calcul_batch, nIn_a], np.float64)

	# -------- 2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------
	abnormal_result = np.zeros([1, nIn_a], np.int64)
	weekly_counter = weekly_second/calcul_batch		# a week's time needs weekly_count iteration
	# -------- 2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------


	# get the pointer of a smat
	tmp = np.asarray(mat)
	dataptr = tmp.ctypes.data_as(POINTER(c_double))

	while True:
		processmainFun.log_write_print(' * * * * * * Thread0: receive NO.%d data* * * * * * ' % count, debug_flag,
								process_index=0, message_flag=3)

		cur_time, calcul_flag = process0Fun.receive_data(dataptr, calcul_batch, frequ)
		calcul_flag = 1		# 2020.10.17 if the calcul_flag = 0, do not push this batch data into queue
		# if debug_flag == 1:
		# 	if np.where(mat != 0)[0].shape[0] == 0:
		# 		print('mat is a zeros matrix!!!')
		# 	else:
		# 		print('mat is not a zeros matrix, please continue~')

		st = time.time()

		# ---------2020.10.17 if the calcul_flag = 0, which means speed==0 and we do not need to calculate this batch data----
		if calcul_flag == 1:	# 2020.10.17 add this judge
			# ---------2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------
			abnormal_result = abnormal_result + np.sum( (mat > abnorm_threshold), axis=0)
			weekly_counter = weekly_counter - 1
			if weekly_counter == 0:
				weekly_counter = weekly_second/calcul_batch
				# write the numpy array to a csv file
				with open('abnormal_result.csv', 'a') as f:
					np.savetxt(f, abnormal_result, fmt='%d', delimiter=',')

				# upload the csv repeat
				command = 'sshpass -p 123 scp -C /IVHM/abnormal_result.csv wy@202.121.180.27:/home/wy/matlab_example/scpTest/'
				exit_code = os.system(command)
				if exit_code == 0:
					message = ' Abnormal_result.csv uploaded successfully!'
					processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
				else:
					message = ' Abnormal_result.csv uploaded Failed Failed Failed!!!'
					processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
			# ---------2020.9.29 add the function to get the number of abnormal data in 22 channels every week---------

			mat_str = mat.tostring()
			que_mat.put(mat_str)
			que_time.put(cur_time)
			et = time.time()
			message = ' Now que_mat size : ' + str(que_mat.qsize()) + ' ;que_time size : ' + str(que_time.qsize()) + ' ;put time : ' + str(et-st)
			processmainFun.log_write_print(message, debug_flag, process_index=0, message_flag=3)

			count = count + 1
		else:
			message = ' SKIP SKIP SKIP this batch!!! This batch data does not need to calculate because the GPS speed is 0'
			processmainFun.log_write_print(message, debug_flag, process_index=0, message_flag=3)


def process1_fun(que_mat, que_time, nIn_a, r, d, theta_path, input_path, resu_path, debug_flag):
	# Func: estimate the interested output in a batch time
	# version 1.0:
	# Todo: The slicing of input_index_b and output_index_b should be conform to the preprocess.py

	nOu_a = 70	# indicates the number of the real outputs of the system
	nIn_b = 16
	nOu_b = 6

	# upload_size_threshold = 5	# when the result txt reach this size, we will stop writing into the file and prepare to upload in thread2
	upload_batch_num_threshold = 3 # when the result txt has been written 3 batch's result, the file will be unploaded
	calcu_count = 1
	write_count = 1

	# fancy slicing of numpy
	input_index_a = list( range(0, nIn_a) )	#[0:nIn_a]		
	# Todo: keep in line with the preprocess.py
	input_index_b = list( range(0, nIn_b) )	#check!!!
	output_index_b = list( range(nIn_b, nIn_b+nOu_b) )	#check!!!

	# load the prepared theta mat, every theta mat is a three dimension matrix because of choosing multi-models
	[theta_a3d, theta_b3d] = process1Fun.load_theta(nIn_a, nOu_a, nIn_b, nOu_b, theta_path)

	# ------------2020.8.25 Add latest! ------------
	# judge function threshold
	# Todo: keep in line with training procedure
	fm_acc_index = [16, 17, 18]
	vari_dist_threshold = 0.025	

	# to deal with the first batch data
	last_r_d = np.zeros([r+d, nIn_a])
	# ------------2020.8.25 Add latest! ------------

	#save_count = 1

	while True:
		if que_mat.empty():
			time.sleep(1)
			processmainFun.log_write_print(' No prepared mat, sleep 1 sec', debug_flag, process_index=1, message_flag=3)
		else:
			st = time.time()
			recei_stime = que_time.get()
			mat_str = que_mat.get()
			batch_input = np.fromstring(mat_str, dtype=np.float64).reshape(calcul_batch*frequ, nIn_a)

			#-------------------------------------
			#cur_time = process0Fun.receive_date()
			#np.savetxt(str(save_count) + 'mat.csv', batch_input, header=cur_time, delimiter=',')
			#save_count = save_count + 1
			#processmainFun.log_write_print(' Process1save : mat is written', debug_flag, process_index=1, message_flag=2)
			#------------------------------------

			et = time.time()
			message = ' Getting from queue needs time: ' + str(et - st) + '. Mat is prepared and begins to calculate!'
			processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=3)
			message = ' Now que_mat size : ' + str(que_mat.qsize()) + ' ;que_time size : ' + str(que_time.qsize())
			processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=3)

			# the data is achieved successfully!

			# ------------2020.8.25 Add latest! -----------
			# --to solve the problem: the first r and the last d data cann't be predicted--
			stacked_batch_input = np.vstack((last_r_d, batch_input))
			last_r_d = batch_input[-(r + d):, :]
			#------------to judge whether the batch data will be calculated or not----------
			judge_code = 1
			#judge_code = process1Fun.judge_calculation(stacked_batch_input, fm_acc_index, vari_dist_threshold, debug_flag)
			# ------------2020.8.25 Add latest! -----------
			
			if judge_code == 1:
				# this batch's data should be calculated!
				s0_time = time.time()

				[phi_a, phi_b, y_batch_true_b, ks, ke] = process1Fun.construct_data(r, d, stacked_batch_input, input_index_a, \
					input_index_b, output_index_b, nIn_a, nIn_b, debug_flag)
				s1_time = time.time()

				model_index = process1Fun.choose_model(phi_b, theta_b3d, y_batch_true_b, ks, ke)
				s2_time = time.time()

				y_batch_pred_a = process1Fun.predict_output(phi_a, theta_a3d, model_index, ks, ke, debug_flag)
				s3_time = time.time()

				write_result = process1Fun.write_output_input(batch_input, y_batch_pred_a, recei_stime, input_path, resu_path, write_count, upload_batch_num_threshold, debug_flag)
				s4_time = time.time()

				if write_result == False:
					processmainFun.log_write_print(' !!!Writing estimation to .cvs failed!!!', debug_flag, process_index=1, message_flag=3)
				else:
					write_count = write_result

				# -------------------------------write the using time to log---------------------------------------------------
				tip_mess = ' The calculate time of this batch data :'
				message1 = '  Construct_data uses %.2f s!\n' % (s1_time - s0_time)
				message2 = '  Choose_model uses %.2f s! Model_index %d \n' % (s2_time - s1_time, model_index)
				message3 = '  Predict_output uses %.2f s!\n' % (s3_time - s2_time)
				message4 = '  Write_output uses %.2f s!\n' % (s4_time - s3_time)
				message5 = '  No. %d batch data uses %.2f s!\n---------------------------------------------------' % (calcu_count, s4_time - s0_time)
				message = tip_mess + '\n\n' + message1 + '\n' + message2 + '\n' + message3 + '\n' + message4 + '\n' + message5
				processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=3)
				# -------------------------------write the using time to log---------------------------------------------------

				calcu_count = calcu_count + 1


def process2_fun(root_path, input_path, resu_path, server_ip, user_name, remote_path, debug_flag):
	# Func: upload result .txt files to the server
	# Time: 9-9-19-50 upload the batch_input files in the input folder to the server

	# resu
	absolute_resu_path = root_path + resu_path
	command_prefix = 'sshpass -p 123 scp -C ' + absolute_resu_path
	command_suffix = user_name + '@' + server_ip + ':' + remote_path + resu_path

	# input
	absolute_input_path = root_path + input_path
	command_prefix_input = 'sshpass -p 123 scp -C ' + absolute_input_path
	command_suffix_input = user_name + '@' + server_ip + ':' + remote_path + input_path

	# log
	log_count = 1
	log_path = "log/"
	absolute_log_path = root_path + log_path
	command_prefix_log = 'sshpass -p 123 scp -C ' + absolute_log_path
	command_suffix_log = user_name + '@' + server_ip + ':' + remote_path + log_path

	while True:

		file_list = os.listdir(resu_path)
		full_file_list = process2Fun.sort_check_full(file_list)

		message = ' Prepared files : ' + str(full_file_list)
		processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=2)

		if full_file_list != []:
			# there are prepared full txt files
			for i in full_file_list:
				# upload these full text files				
				st_time = time.time()
				upload_result = process2Fun.upload_delete_file(i, absolute_resu_path, command_prefix, command_suffix, debug_flag)
				upload_result_input = process2Fun.upload_delete_file(i, absolute_input_path, command_prefix_input, command_suffix_input,
															   debug_flag)
				# if upload fail, the only reason may be no Internet
				# result
				if upload_result == True:
					message = ' Result Files are Uploaded and deleted: %s, using %.2f s!' % (i, time.time()-st_time)
					processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
				else:
					message = ' Result Files Uploaded ERROR !!! Path wrong OR waiting for Internet connect... Using %.2f s!' % (time.time()-st_time)
					processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)

				# input
				if upload_result_input == True:
					message = ' Input Files are Uploaded and deleted: %s, using %.2f s!' % (i, time.time() - st_time)
					processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
				else:
					message = ' Input Files Uploaded ERROR !!! Path wrong OR waiting for Internet connect... Using %.2f s!' % (time.time() - st_time)
					processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)

				time.sleep(1)
		else:
			time.sleep(1)

		#  -----------------------upload the log files---------------------------
		log_list = os.listdir(log_path)
		if "log.txt.1" in log_list:
			log_count = process2Fun.rename_log("log.txt.1", log_path, log_count)

		upload_log_list = [ i for i in log_list if i[-4:]=='.txt' and i != 'log.txt']
		for i in upload_log_list:
			upload_log_result = process2Fun.upload_log(i, log_path, command_prefix_log, command_suffix_log, debug_flag)
			if upload_log_result == True:
				message = ' LogLogLog----Uploaded and deleted!'
				processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)
			else:
				message = ' LogLogLog----Path wrong OR waiting for Internet connect...'
				processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=3)


if __name__ == '__main__':

	# path variables, which are different in PC and Gateway
	root_path = "/IVHM/"
	# root_path = "/home/wy/IVHM_code/newest/"
	theta_path = "MTheta/"	#relative path to the root_path
	resu_path = "result/"	#relative path to the root_path
	txt_path = "txt/"
	input_path = "input/"
	# log_path = "log/"		# defined in the processmainFun.py


	# variables of thread2 :
	server_ip = "202.121.180.27"
	user_name = "wy"
	remote_path = "/home/wy/matlab_example/scpTest/"

	# other variables
	debug_flag = 1

	# set the logging
	processmainFun.set_logging()

	# * * * * * * * * multiprocessing are ready to start !  * * * * * * * * *
	q_m = Queue()
	q_t = Queue()


	# * * three extra processing version * * *
	# if process0_test_flag == 1:
	# 	process0 = Process(target=process0_fun_test, kwargs={'que_mat':q_m,'que_time':q_t,"nIn_a":nIn_a,"calcul_batch":calcul_batch,"frequ":frequ,'debug_flag':debug_flag})
	# else:
	# 	process0 = Process(target=process0_fun, kwargs={'que_mat':q_m,'que_time':q_t,"nIn_a":nIn_a,"calcul_batch":calcul_batch,"frequ":frequ,'debug_flag':debug_flag})

	# process1 = Process(target=process1_fun, kwargs={'que_mat':q_m,'que_time':q_t, "nIn_a":nIn_a, "r":r, "d":d, "theta_path":theta_path, "input_path":input_path, "resu_path":resu_path, "debug_flag":debug_flag})
	# process2 = Process(target=process2_fun, kwargs={"root_path":root_path,"input_path":input_path,"resu_path":resu_path,"server_ip":server_ip,"user_name":user_name,\
	# 	"remote_path":remote_path,"debug_flag":debug_flag})
	
	# process0.start()
	# process1.start()
	# process2.start()

	# try:
	# 	pass
	# except(KeyboardInterrupt):
	# 	process0Fun.p0End()
	# 	print("Finished Successfully")
	# * * * * * * * * * * * * *


	# * * two extra processing version * * *
	process1 = Process(target=process1_fun, kwargs={'que_mat':q_m,'que_time':q_t, "nIn_a":nIn_a, "r":r, "d":d, "theta_path":theta_path, "input_path":input_path, "resu_path":resu_path, "debug_flag":debug_flag})
	process2 = Process(target=process2_fun, kwargs={"root_path":root_path,"input_path":input_path,"resu_path":resu_path,"server_ip":server_ip,"user_name":user_name,\
		"remote_path":remote_path,"debug_flag":debug_flag})
	
	process1.start()
	process2.start()
	
	try:
		if process0_test_flag == 1:
			process0 = process0_fun_test(q_m, q_t, nIn_a, calcul_batch, frequ, debug_flag)
		else:
			process0 = process0_fun(q_m, q_t, nIn_a, calcul_batch, frequ, debug_flag)
	except(KeyboardInterrupt):
		process0Fun.p0End()
		print("Finished Successfully")
