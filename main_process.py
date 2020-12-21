# import receiveMatrixProcess
# import receiveSpeedProcess
# import estimateOutputProcess
# import updateRemoveFileProcess
import time
from config import Param
from multiprocessing import Process, Queue


def receiveMatrixFun():
    pass

def estimateOutputFun():
    pass

def uploadRmFileFun():
    pass

if __name__ == "__main__":
    a = Param(512, 10, 22, 7)
    a.displayParam()

    process1 = Process(target = estimateOutputFun, kwargs={})
    process2 = Process(target = uploadRmFileFun, kwargs={})

    process1.start()
    process2.start()

    try:
        receiveMatrixFun()
    except(KeyboardInterrupt):
        # receiveMatrixFun.p0End()
        print("Finished successfully!")
        
