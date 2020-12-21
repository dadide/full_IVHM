# import receiveMatrixProcess
# import receiveSpeedProcess
# import estimateOutputProcess
from uploadRemoveFileProcess import UploadRemoveFile
import time
import config
from multiprocessing import Process, Queue


def receiveMatrixFun():
    pass

def estimateOutputFun():
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
    
    process1.start()
    process2.start()

    try:
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
        
