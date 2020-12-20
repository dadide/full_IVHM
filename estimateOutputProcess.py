import os
import numpy as np

class WriteFile():
    def __init__(self, fold, step_num):
        self.fold = fold
        self.file_count = 1
        self.step_num = step_num
    
    def getFileName(self):
        file_name = str(self.file_count)
        self.file_count = self.file_count + 1
        return file_name

    def save2File(self, npArray):
        is_exist = os.path.exists(self.fold)
        if not is_exist:
            os.makedirs(self.fold)

        with open(fold + self.getFileName()) as f:
            np.savetxt(f, npArray, fmt='%.4f')


if __name__ == "__main__":
    fold = './input/'
    step_num = 2
    a = WriteFile(fold, step_num)
    result = np.zeros([3,10], np.float32)+1
    a.save2File(result)





