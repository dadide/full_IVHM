import os
import time
import config


class UploadRemoveFile:
    def __init__(self, admin_ip, password, source_fold, destination_fold):
        self.admin_ip = admin_ip
        self.password = password
        self.source_fold = source_fold
        self.destination_fold = destination_fold
        self.logger = config.setUpLogger("upRm")

    def findFullFile(self, file_fold):
        INDEX_OF_FLAG = -5
        files = os.listdir(self.source_fold + file_fold)
        full_files = [i for i in files if i[INDEX_OF_FLAG]=='F']    
        if full_files == []:
            log_flag = -1
            emptyCommand = file_fold
            self.generateLog(emptyCommand, log_flag)
        else:
            log_flag = -2
            fullCommand = file_fold + ' are ' + str(full_files)
            self.generateLog(fullCommand, log_flag)
        return full_files

    def uploadFile(self, file_fold, file_name):
        uploadCommand = 'sshpass -p ' + self.password + ' scp -C ' + self.source_fold + file_fold \
                        + file_name + ' ' + self.admin_ip + ':' + self.destination_fold + file_fold
        # print(uploadCommand)
        exit_code = os.system(uploadCommand)
        # exit_code = 1
        if exit_code != 0:
            log_flag = 1
            self.generateLog(uploadCommand, log_flag)
        else:
            log_flag = 0
            self.generateLog(uploadCommand, log_flag)
        return exit_code

    def removeFile(self, file_fold, file_name):
        removeCommand = 'rm ' + self.source_fold + file_fold + file_name 
        # print(removeCommand)
        exit_code = os.system(removeCommand)
        # exit_code = 2
        if exit_code != 0:
            log_flag = 1
            self.generateLog(removeCommand, log_flag)
        else:
            log_flag = 0
            self.generateLog(removeCommand, log_flag)
        # return exit_code

    def findUploadRemoveFile(self, file_fold):
        full_file_list = self.findFullFile(file_fold)
        for i in range(0, len(full_file_list)):
            file_name = full_file_list[i]
            if self.uploadFile(file_fold, file_name) == 0:
                self.removeFile(file_fold, file_name)
            else:
                break

    def generateLog(self, command, log_flag):
        if log_flag == 0:
            message = 'Success~~ ' + command
            self.logger.info(message)
        elif log_flag == 1 :
            message = 'Failed!!! ' + command
            self.logger.warning(message)
        elif log_flag == -1:
            message = 'Please wait, empty in ' + command
            self.logger.warning(message)
        elif log_flag == -2:
            message = 'Files in ' + command
            self.logger.debug(message)



if __name__ == "__main__":
    admin_ip = 'wy@202.121.180.27'
    password = '123'
    # source_fold = '/IVHM/'
    source_fold = './'
    destination_fold = '/home/wy/matlab_example/scpTest/'
    inputUpRm = UploadRemoveFile(admin_ip, password, source_fold, destination_fold)

    file_fold = 'input/' # or 'result/', 'speed/'

    inputUpRm.findUploadRemoveFile(file_fold)

    # flag = 1 
    # if flag == 1:
    #     file_name = 'result.csv'
    #     ec1 = inputUpRm.uploadFile(file_fold, file_name)
    #     ec2 = inputUpRm.removeFile(file_fold, file_name)
    # else:
    #     full_file_list = inputUpRm.findFullFile(file_fold)
    #     print(full_file_list)
    #     for i in range(0, len(full_file_list)):
    #         file_name = full_file_list[i]
    #         inputUpRm.uploadFile(file_fold, file_name)
    #         inputUpRm.removeFile(file_fold, file_name)

