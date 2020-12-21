import os
import time
import numba
import config
import numpy as np
from scipy.io import loadmat
import uploadRemoveFileProcess


def load_theta(p):
	
	# Func: To get the saved 3d theta matrix
	
	theta_a3d_name = "MTheta_" + str(p.nIn_a) + 'I' + str(p.nOu_a) + 'O'	#"MTheta_18I6O.mat"
	theta_b3d_name = "MTheta_" + str(p.nIn_b) + 'I' + str(p.nOu_b) + 'O'	#"MTheta_12I2O.mat"

	theta_a3d = loadmat(p.theta_path + theta_a3d_name)
	theta_b3d = loadmat(p.theta_path + theta_b3d_name)

	theta_a3d = theta_a3d["MTheta"]									  #得到 theta_a，是一个三维array
	theta_b3d = theta_b3d["MTheta"]   

	return theta_a3d, theta_b3d


def construct_data(p, batch_input):

	# Func: To get the Phi , Y from batch_input and corresponding index_slice

    input_index_a = list(range(0, p.nIn_a))
    input_index_b = list(range(0, p.nIn_b))
    output_index_b = list(range(p.nIn_b, p.nIn_b + p.nOu_b))

	batch_input_a = batch_input[:, input_index_a]
	batch_input_b = batch_input[:, input_index_b]
	y_batch_true_b = batch_input[:, output_index_b]

	batch_input_b = batch_input_b - batch_input_b.mean(axis=0)
	y_batch_true_b = y_batch_true_b - y_batch_true_b.mean(axis=0)

	message = ' Dimension check----'+str(batch_input_a.shape) + ' '+str(batch_input_b.shape)+ ' '+str(y_batch_true_b.shape)
	print(message)
	# print(batch_input_a.shape)
	# print(batch_input_b.shape)
	# print(y_batch_true_a.shape)
	# print(y_batch_true_b.shape)

	phi_a, phi_b, ks, ke = construct_phi(p.r, p.d, batch_input_a, batch_input_b, p.nIn_a, p.nIn_b)

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


def predict_output(phi_a, theta_a3d, model_index, ks, ke):
	
	# Func: To estimate these interested outputs and write the numpy array to .txt files
	# Todo: Check whether np.set_printoptions works or not?

	theta = theta_a3d[model_index,:,:]

	# estimate here!
	y_batch_pred_a = np.dot(phi_a, theta)

	return y_batch_pred_a





