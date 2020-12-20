# import receiveMatrixProcess
# import receiveSpeedProcess
# import estimateOutputProcess
# import updateRemoveFileProcess
import time
from multiprocessing import Process. Queue

class param: 
    def __init__(self, frequency, step_time, input_dim, output_dim):
        self.frequency = frequency
        self.step_time = step_time
        self.input_dim = input_dim
        self.output_dim = output_dim
      
   
    def displayParam(self):
        print("frequency : ", self.frequency, ", step_time: ", self.step_time, ", input_dim: ", self.input_dim, ", output_dim: ", self.output_dim)

def receiveMatrixFun():
    pass


def uploadRmFileFun():
    pass

if __name__ == "__main__":
    a = param(512, 10, 22, 7)
    a.displayParam()

    process1 = Process(target = receiveMatrixFun, kwargs={})
    process2 = Process(target = uploadRmFileFun, kwargs={})

    process1.start()
    process2.start()

    try:
        process0 = receiveMatrixFun()
    except(KeyboardInterrupt):
        receiveMatrixFun.p0End()
        print("Finished successfully!")
        
