# import receiveMatrixProcess
# import receiveSpeedProcess
# import estimateOutputProcess
<<<<<<< HEAD
from uploadRemoveFileProcess import UploadRemoveFile
import time
import config
=======
# import updateRemoveFileProcess
import time
from config import Param
>>>>>>> 9c18bf4393d6a4b5a0a26f9074dca16fc99d0a2f
from multiprocessing import Process, Queue


def receiveMatrixFun():
    pass

def estimateOutputFun():
<<<<<<< HEAD
    while True:
        try:
            print('sleep 1 sec!')
            time.sleep(1)
            
        except(KeyboardInterrupt):
            break


def uploadRmFileFun(UpRm):
    
    while True:
        try:
            UpRm.findUploadRemoveFile('input/')
            time.sleep(1)
            # UpRm.findUploadRemoveFile('result/')
        except(KeyboardInterrupt):
            break

if __name__ == "__main__":
    
    a = config.Param(512, 10, 22, 7)
    a.displayParam()

    UpRm = UploadRemoveFile(config.admin_ip, config.password, config.source_fold, config.destination_fold)

    process1 = Process(target=estimateOutputFun, kwargs={})
    process2 = Process(target=uploadRmFileFun, kwargs={'UpRm':UpRm})
    
=======
    pass

def uploadRmFileFun():
    pass

if __name__ == "__main__":
    a = Param(512, 10, 22, 7)
    a.displayParam()

    process1 = Process(target = estimateOutputFun, kwargs={})
    process2 = Process(target = uploadRmFileFun, kwargs={})

>>>>>>> 9c18bf4393d6a4b5a0a26f9074dca16fc99d0a2f
    process1.start()
    process2.start()

    try:
<<<<<<< HEAD
        process1.join()
        process2.join()
    except(KeyboardInterrupt):
        process1.terminate()
        process1.join()
        process2.terminate()
        process2.join()

    # try:
    #     receiveMatrixFun()
    # except(KeyboardInterrupt):
    #     # receiveMatrixFun.p0End()
    #     print("Finished successfully!")
=======
        receiveMatrixFun()
    except(KeyboardInterrupt):
        # receiveMatrixFun.p0End()
        print("Finished successfully!")
>>>>>>> 9c18bf4393d6a4b5a0a26f9074dca16fc99d0a2f
        
