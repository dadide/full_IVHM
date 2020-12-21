import os
import time
import config
import numpy as np


class WriteFile():
    def __init__(self, fold, step_num):
        self.fold = fold
        self.step_num = step_num
        self.file_count = 1
        self.logger = config.setUpLogger("write")
   
    def getFileName(self):
        INDEX_OF_FLAG = -5
        cur_time = config.get_time()
        
        files = os.listdir(self.fold)
        not_full_file = [i for i in files if i[INDEX_OF_FLAG]!='F']
        
        if len(not_full_file) == 0:
            file_name = cur_time + '-' + str(self.file_count) + '-1.csv'
            with open(self.fold + file_name, 'a+') as f:
                f.write(config.header_input_str+'\n')
        elif len(not_full_file) == 1:           
            file_name = not_full_file[0]
        else:
            log_flag = 0
            command = str(not_full_file)
            self.generateLog(command, log_flag)
            file_name = 'somethingwrong.csv'

        return file_name

    def save2File(self, npArray):
        INDEX_OF_FLAG = -5

        is_exist = os.path.exists(self.fold)
        if not is_exist:
            os.makedirs(self.fold)
        
        file_name = self.getFileName()
        with open(self.fold + file_name, 'a+') as f:
            np.savetxt(f, npArray, fmt='%.4f')

        self.file_count = self.file_count + 1
        if file_name[INDEX_OF_FLAG] != str(self.step_num):
            new_file_name = file_name[:INDEX_OF_FLAG] + str(int(file_name[INDEX_OF_FLAG])+1) + file_name[INDEX_OF_FLAG+1:]
        else:
            new_file_name = file_name[:INDEX_OF_FLAG] + 'F' + file_name[INDEX_OF_FLAG+1:]
        os.rename(self.fold + file_name, self.fold + new_file_name)
        
        log_flag = 1
        command = file_name + ' to new filename: ' + new_file_name
        self.generateLog(command, log_flag)

    def generateLog(self, command, log_flag):
        if log_flag == 0:
            message = 'Error!!! Because there are more than one not-full files: ' + command
            self.logger.error(message)
        elif log_flag == 1:
            message = 'Success~~ Change old filename: ' + command
            self.logger.debug(message)


if __name__ == "__main__":
    fold = './input/'
    step_num = 5
    a = WriteFile(fold, step_num)
    for i in range(1,9):
        print(i)
        result = np.zeros([3,10]) + i
        a.save2File(result)






