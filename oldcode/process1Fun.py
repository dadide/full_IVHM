import os
import time
import numba
import processmainFun
import numpy as np
from scipy.io import loadmat


header_str='For_SSL_FL,For_SSL_FR,For_STR_FL,For_STR_FR,For_BJ_X_FL,For_BJ_Y_FL,For_BJ_X_FR,\
For_BJ_Y_FR,Ms_LCA_FL1,Ms_LCA_FL2,Ms_LCA_FL3,Ms_LCA_FR1,Ms_LCA_FR2,Ms_LCA_FR3,Ms_FSSL,\
Ms_RSSL,Ms_TA_RL1,Ms_TA_RL2,Ms_TA_RL3,Ms_TA_RR1,Ms_TA_RR2,Ms_TA_RR3,Ms_UCA_RL,Ms_UCA_RR,\
Ms_LCA_RL1,Ms_LCA_RL2,Ms_LCA_RR1,Ms_LCA_RR2,For_TL_RL,For_TL_RR,For_SSL_RL,For_SSL_RR,\
WFT_Fx_FL,WFT_Fy_FL,WFT_Fz_FL,WFT_Mx_FL,WFT_My_FL,WFT_Mz_FL,WFT_Fx_FR,WFT_Fy_FR,WFT_Fz_FR,WFT_Mx_FR,WFT_My_FR,\
WFT_Mz_FR,WFT_Fx_RL,WFT_Fy_RL,WFT_Fz_RL,WFT_Mx_RL,WFT_My_RL,WFT_Mz_RL,WFT_Fx_RR,WFT_Fy_RR,WFT_Fz_RR,WFT_Mx_RR,WFT_My_RR,WFT_Mz_RR,\
Acc_X_FLLB,Acc_Y_FLLB,Acc_Z_FLLB,Acc_X_FRLB,Acc_Y_FRLB,Acc_Z_FRLB,Acc_X_FS,Acc_Y_FS,Acc_Z_FS,Acc_X_RS,Acc_Y_RS,Acc_Z_RS,Acc_X_DSB,Acc_Z_DSB'

header_input_str = 'Acc_X_Whl_FL,Acc_Y_Whl_FL,Acc_Z_Whl_FL,\
Acc_X_Whl_FR,Acc_Y_Whl_FR,Acc_Z_Whl_FR,\
Acc_X_Whl_RL,Acc_Y_Whl_RL,Acc_Z_Whl_RL,\
Acc_X_Whl_RR,Acc_Y_Whl_RR,Acc_Z_Whl_RR,\
Dis_Dmp_FR,Dis_Dmp_FL,Dis_Dmp_RL,Dis_Dmp_RR,\
Acc_X_FM,Acc_Y_FM,Acc_Z_FM,\
Acc_X_RM,Acc_Y_RM,Acc_Z_RM'

def load_theta(nIn_a, nOu_a, nIn_b, nOu_b, theta_path):
	
	# Func: To get the saved 3d theta matrix
	
	theta_a3d_name = "MTheta_" + str(nIn_a) + 'I' + str(nOu_a) + 'O'	#"MTheta_18I6O.mat"
	theta_b3d_name = "MTheta_" + str(nIn_b) + 'I' + str(nOu_b) + 'O'	#"MTheta_12I2O.mat"

	theta_a3d = loadmat(theta_path + theta_a3d_name)
	theta_b3d = loadmat(theta_path + theta_b3d_name)

	theta_a3d = theta_a3d["MTheta"]									  #得到 theta_a，是一个三维array
	theta_b3d = theta_b3d["MTheta"]   

	return theta_a3d, theta_b3d


def construct_data(r, d, batch_input, input_index_a, input_index_b, output_index_b, nIn_a, nIn_b, debug_flag):

	# Func: To get the Phi , Y from batch_input and corresponding index_slice

	batch_input_a = batch_input[:, input_index_a]
	batch_input_b = batch_input[:, input_index_b]
	y_batch_true_b = batch_input[:, output_index_b]

	# there is no need to demean for input data of a
	# b model's input and output data should be demeaned
	batch_input_b = batch_input_b - batch_input_b.mean(axis=0)
	y_batch_true_b = y_batch_true_b - y_batch_true_b.mean(axis=0)

	message = ' Dimension check----'+str(batch_input_a.shape) + ' '+str(batch_input_b.shape)+ ' '+str(y_batch_true_b.shape)
	processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=2)
	# print(batch_input_a.shape)
	# print(batch_input_b.shape)
	# print(y_batch_true_a.shape)
	# print(y_batch_true_b.shape)

	phi_a, phi_b, ks, ke = construct_phi(r, d, batch_input_a, batch_input_b, nIn_a, nIn_b)

	return phi_a, phi_b, y_batch_true_b, ks, ke


@numba.jit(nopython=True)
def construct_phi(r, d, batch_input_a, batch_input_b, nIn_a, nIn_b):

	# Func: To get the Phi according to r,d,batch_input_a,batch_input_b
	ks = r
	ke = batch_input_a.shape[0]-d-1
	
	phi_a = np.zeros(((ke-ks+1), (d+r+1)*nIn_a))
	phi_b = np.zeros(((ke-ks+1), (d+r+1)*nIn_b))


	# print(batch_input_b.shape, phi_a.shape, phi_b.shape)
	
	for i in range(0, ke-ks+1):
		for j in range(0, d+r+1):
			phi_a[i, (j*nIn_a):((j+1)*nIn_a)] = batch_input_a[ks+d+i-j,:]
			phi_b[i, (j*nIn_b):((j+1)*nIn_b)] = batch_input_b[ks+d+i-j,:]

	return phi_a, phi_b, ks, ke


def choose_model(phi_b, theta_b3d, y_batch_true_b, ks, ke):

	# Func: To choose model from the possible working conditions
	
	y_batch_pred_b = np.zeros([theta_b3d.shape[0], phi_b.shape[0], theta_b3d.shape[-1]])
	
	for i in range(theta_b3d.shape[-1]):
		# print(phi_b.shape)
		# print( (theta_b3d[:,:,i].T).shape)
		y_batch_pred_b[:,:,i] = np.matmul(phi_b, theta_b3d[:,:,i].T).T

	y_diff = np.square(y_batch_pred_b - y_batch_true_b[ks:ke+1, :])
	
	mse = y_diff.sum(axis = 1)
	
	mse = mse.sum(axis = 1)

	return mse.argmin(axis = 0)


def predict_output(phi_a, theta_a3d, model_index, ks, ke, debug_flag):
	
	# Func: To estimate these interested outputs and write the numpy array to .txt files
	# Todo: Check whether np.set_printoptions works or not?

	theta = theta_a3d[model_index,:,:]

	# print less numbers of mse
	# np.set_printoptions(precision = 2)

	# estimate here!
	y_batch_pred_a = np.dot(phi_a, theta)

	return y_batch_pred_a


def write_output_input(batch_input, y_batch_pred_a, recei_stime, input_path, resu_path, write_count, upload_batch_num_threshold, debug_flag):

	# Func: To write the estimation data the resu_path folder
	# Time: 8-17-15-30
	# Time: 9-2-15-56 change 'upload_size_threshold' to 'upload_batch_num_threshold'
	# Time: 9-9-19-40 write the batch_input to the input folder

	# get the file which we will write
	file_name = get_writable_filename(recei_stime, resu_path, input_path, write_count, debug_flag)

	if file_name != False:
		# open the specified file and append y_batch_pred_a to it
		with open(resu_path + file_name, 'a') as f:
			np.savetxt(f, y_batch_pred_a, fmt='%.3f', delimiter=',')	# write the result to file

		# open the specified file and append batch_input to it
		with open(input_path + file_name, 'a') as f:
			np.savetxt(f, batch_input, fmt='%.3f', delimiter=',')	# write the result to file

		write_count = write_count + 1

		# 1.0 ---- check the size of the file, if size is larger than the upload_size_threshold, change its name to show the txt is prepared for upload
		# if get_filesize(resu_path + file_name) > upload_size_threshold:

		# 2.0 ---- check the file has written how many batches into the file
		batch_num = int(file_name[-5])
		if batch_num == upload_batch_num_threshold - 1:
			new_file_name = file_name[:-5] + 'F' + '.csv'
		else:
			new_file_name = file_name[:-5] + str(batch_num+1) + '.csv'
		# predict_result
		os.rename(resu_path + file_name, resu_path + new_file_name)

		# input_data
		os.rename(input_path + file_name, input_path + new_file_name)

		return write_count
	else:
		return False


def get_writable_filename(recei_stime, resu_path, input_path, write_count, debug_flag):

	# Func: To check if there is unfinished file (whose size is smaller than the threshold)
	# Retu: a string represents the file name which we should write data to 

	file_list = os.listdir(resu_path)

	unfull_file_list = [i for i in file_list if i[-5]!='F']

	if len(unfull_file_list) == 0:
		# there is no unfull_file in resu_path
		# create a new file with the suffix '_U'
		new_file_name = str(write_count) + '_' + recei_stime + '0.csv'

		with open(resu_path + new_file_name, 'w') as f:
			f.write(header_str+'\n')	# write the result to file

		with open(input_path + new_file_name, 'w') as f:
			f.write(header_input_str+'\n')	# write the result to file

		if debug_flag == 1 :
			message = ' NewNewNew---Writing array to : %s' % new_file_name
			processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=2)
		return new_file_name

	elif len(unfull_file_list) == 1:
		# only one file is unfull, append the new result to this file direct
		if debug_flag == 1 :
			message = ' OldOldOld---Writing array to : %s' % unfull_file_list[0]
			processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=2)
		return unfull_file_list[0]

	else:
		# more than one file is unfull
		if debug_flag == 1 :
			message = ' WhyWhyWhy---Two or more UNFULL files???'
			processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=2)
		return False


def get_filesize(filePath):
 
	fsize = os.path.getsize(filePath)
	fsize = fsize / float(1024 * 1024)

	return round(fsize, 2)


def judge_calculation(batch_input, fm_acc_index, vari_dist_threshold, debug_flag):

	fm_acc_batch_input = batch_input[:, fm_acc_index]
	xyz_vari = np.var(fm_acc_batch_input, 0)

	vari_dist = np.sqrt(xyz_vari[0]*xyz_vari[0]+xyz_vari[1]*xyz_vari[1]+xyz_vari[2]*xyz_vari[2])

	if vari_dist > vari_dist_threshold:
		# the vari_dist is big enough
		message = " Vari_dist is %.4f, greater than threshold %.4f. This batch will be calculated." % (vari_dist, vari_dist_threshold)
		processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=2)
		return 1
	else:
		message = " Vari_dist is %.4f, smaller than threshold %.4f. This batch will be ignored." % (vari_dist, vari_dist_threshold)
		processmainFun.log_write_print(message, debug_flag, process_index=1, message_flag=2)
		return 0
