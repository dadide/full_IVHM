import time
import logging
from logging.handlers import TimedRotatingFileHandler

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


class Param: 
    def __init__(self, frequency, step_time, input_dim, output_dim):
        self.frequency = frequency
        self.step_time = step_time
        self.input_dim = input_dim
        self.output_dim = output_dim
         
    def displayParam(self):
        print("frequency : ", self.frequency, ", step_time: ", self.step_time, ", input_dim: ", self.input_dim, ", output_dim: ", self.output_dim)

def get_time():
	# Func : to get the current time
	time_tup = time.localtime(time.time())
	format_time='%Y_%m_%d-%H_%M_%S'
	cur_time = time.strftime(format_time, time_tup)
	return cur_time

def setUpLogger(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)        
    handler = TimedRotatingFileHandler(log_name + ".log", 
                                    when="m",
                                    interval=2)    #backupCount=2   
    formatter = logging.Formatter("--%(asctime)s--%(levelname)s--%(message)s", \
                                datefmt="%Y-%m-%d %H:%M:%S")                                     
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger