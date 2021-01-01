import time
import logging
# import process0Fun
import process1Fun
from logging.handlers import RotatingFileHandler

def get_time():
	# Func : to get the current time
	time_tup = time.localtime(time.time())
	format_time='%Y_%m_%d_%H_%M_%S'
	cur_time = time.strftime(format_time, time_tup)
	return cur_time


def set_logging():
	# Func : setting for log

	log_path = "log/"

	# ----------------------create the log txt----------------------
	log_file = open(log_path + 'log.txt', 'w')	# save running log to log.txt file
	log_file.close()
	log_file0 = open(log_path + 'debug/process0_log.txt', 'w')	# save running log to log.txt file
	log_file0.close()
	log_file1 = open(log_path + 'debug/process1_log.txt', 'w')	# save running log to log.txt file
	log_file1.close()
	log_file2 = open(log_path + 'debug/process2_log.txt', 'w')	# save running log to log.txt file
	log_file2.close()

	# -------------2020.10.17---create the abnormal txt to record the data----------------
	with open('abnormal_result.csv', 'w') as f:
		f.write(process1Fun.header_input_str + '\n')  # write the result to file

	# ----------------------python logging module parameters----------------------
	logger = logging.getLogger('main')
	# logger.setLevel(level=logging.WARNING)
	logger.setLevel(level=logging.INFO)
	formatter = logging.Formatter("--%(asctime)s--%(name)s--%(levelname)s--\t  %(message)s", \
						datefmt="%Y-%m-%d %H:%M:%S")
	handler = RotatingFileHandler(log_path + "log.txt", maxBytes=100 * 1024, backupCount=1)
	# handler = logging.FileHandler(log_path + 'log.txt')
	handler.setLevel(logging.WARNING)
	handler.setFormatter(formatter)
	logger.addHandler(handler)


def log_write_print(message, debug_flag, process_index, message_flag):
	'''
	Func : To log in a wiser and simple way
	Usag : mainFun.log_write_print('hahahahaha', log_path, 0, debug_flag, 2)
		   mainFun.log_write_print(message, log_path, 0, debug_flag, 2)
	'''
	log_path = "log/debug/"

	# log
	logger_name = "main.process" + str(process_index)
	process_logger = logging.getLogger(logger_name)

	if message_flag == 1:
		process_logger.debug(message)
	elif message_flag == 2:
		process_logger.info(message)
	elif message_flag == 3:
		process_logger.warning(message)
	else:
		process_logger.error(message)

	'''
	# under the debug mode, the writing and printing will be executed
	if debug_flag == 1:
		# write
		file_name = log_path + 'process' + str(process_index) + '_log.txt'
		with open(file_name, 'a') as f:
			# f.write("----" + get_time() +"----" + message + "\n" )
			f.write("----" + process0Fun.receive_date() + "----" + message + "\n" )
		# print
		# print("----" + get_time() +"----" + message)
		print("----" + process0Fun.receive_date() +"----" + message)
'''
