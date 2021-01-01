import time
import os
import processmainFun


def sort_check_full(file_list):
	# find the file whose name contained the 'F' surffix
	full_file_list = [i for i in file_list if i[-5]=='F']

	# sort the files in ascendant
	# Q1 : error when the list=[] ???
	# A1 : comment the row first
	# full_file_list.sort(key = lambda x : int(x[:-26]))
	return full_file_list


def upload_delete_file(file_name, absolute_resu_path, command_prefix, command_suffix, debug_flag):
	command = command_prefix + file_name + ' ' + command_suffix

	message = ' Command: ' + command
	processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=2)

	exit_code = os.system(command)

	if exit_code == 0:
		os.system('rm ' + absolute_resu_path + file_name)
		return True
	else:
		# message = '!!!!!Fail Fail Fail---Exit_code != 0\n'
		# processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=2)
		return False


def rename_log(log_name, log_path, log_count):
	# rename the spare log
	new_log_name = str(log_count) + '_log.txt'
	os.rename(log_path + log_name, log_path + new_log_name)

	log_count = log_count + 1  # the count will increase when log.txt.1 exist

	return log_count


def upload_log(log_name, log_path, command_prefix_log, command_suffix_log, debug_flag):
	# upload the spare log
	command = command_prefix_log + log_name + ' ' + command_suffix_log
	message = ' Command: ' + command
	processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=2)

	exit_code = os.system(command)
	if exit_code == 0:
		# message = '!!!!!Succ Succ Succ---Exit_code == 0\n'
		# processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=2)
		os.system('rm ' + log_path + log_name)
		return True
	else:
		# message = '!!!!!Fail Fail Fail---Exit_code != 0\n'
		# processmainFun.log_write_print(message, debug_flag, process_index=2, message_flag=2)
		return False
