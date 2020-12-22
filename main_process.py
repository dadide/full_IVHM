# import receiveMatrixProcess
# import receiveSpeedProcess
import estimateOutputProcess
from writeUploadRemoveFileClass import UploadRemoveFile, WriteFile
import time
import config
import numpy as np
from multiprocessing import Process, Queue

def receiveMatrixFun(p, queue_matrix):
    # generate data we need to test

    count = 1

    while True:
        try:
            mat = np.arange(p.freque*p.step_time*p.nIn_a, dtype=np.float64).reshape(p.freque*p.step_time, p.nIn_a)  #,dtype=np.float64
            mat_str = mat.tostring()
            queue_matrix.put(mat_str)
            # queue_matrix.put(mat)

            message = 'count is ' + str(count) + ', queue_matrix size : ' + str(queue_matrix.qsize())
            print(message)

            # print(count)
            count = count + 1
            if count > 10:
                break
            
            time.sleep(p.step_time/5)
        except(KeyboardInterrupt):
            break


def receiveSpeedFun(p, queue_speed):
    # generate data we need to test

    count = 1

    while True:
        try:
            mat = np.arange(p.spdfre*p.step_time, dtype=np.float64).reshape(p.spdfre*p.step_time, 1)  #,dtype=np.float64
            mat_str = mat.tostring()
            queue_speed.put(mat_str)

            message = 'count is ' + str(count) + ', queue_speed size : ' + str(queue_speed.qsize())
            print(message)

            # print(count)
            count = count + 1
            if count > 10:
                break
            
            time.sleep(p.step_time/5)
        except(KeyboardInterrupt):
            break

def estimateOutputFun(p, queue_matrix, queue_speed):

    step_num = 3
    ResultWriter = WriteFile('./result/', step_num)
    InputWriter = WriteFile('./input/', step_num)
    SpeedWriter = WriteFile('./speed/', step_num)

    [theta_a3d, theta_b3d] = estimateOutputProcess.loadTheta(p)
    last_r_d = np.zeros([p.r + p.d, p.nIn_a])
    
    #logger = config.setUpLogger("estimate")

    while True:
        try:
            if queue_matrix.empty() or queue_speed.empty():
                time.sleep(1)
            else:
                [batch_input, batch_speed] = estimateOutputProcess.getDataFromQueue(queue_matrix, queue_speed, p)
                calcu_flag = estimateOutputProcess.getCalculateFlag(batch_speed)
                if calcu_flag == 1:
                    stacked_batch_input = np.vstack((last_r_d, batch_input))
                    last_r_d = batch_input[-(p.r + p.d):, :]

                    t1 = time.time()
                    [phi_a, phi_b, y_batch_true_b, ks, ke] = estimateOutputProcess.constructData(p, stacked_batch_input)
                    model_index = estimateOutputProcess.chooseModel(phi_b, theta_b3d, y_batch_true_b, ks, ke)
                    y_batch_pred_a = estimateOutputProcess.estimateOutput(phi_a, theta_a3d, model_index, ks, ke)
                    t2 = time.time()

                    ResultWriter.save2File(y_batch_pred_a)                                              
                    InputWriter.save2File(batch_input)
                    SpeedWriter.save2File(batch_speed) 
                    t3 = time.time()
                    message = 'estimate consumes:{:0.2f}, write consumes:{:0.2f}'.format(t2-t1, t3-t2)
                    #logger.INFO(message)
                    print(message)
                else:
                    InputWriter.save2File(batch_input)
                    SpeedWriter.save2File(batch_speed) 
                    message = 'This step does not need calculate'
                    #logger.INFO(message)
                    print(message)                
        except(KeyboardInterrupt):
            break


def uploadRmFileFun():
    UpRm = UploadRemoveFile(config.admin_ip, config.password, config.source_fold, config.destination_fold)
    while True:
        try:
            UpRm.findUploadRemoveFile('input/')
            time.sleep(1)
            UpRm.findUploadRemoveFile('result/')
            time.sleep(1)
            UpRm.findUploadRemoveFile('log/')
            time.sleep(1)            
        except(KeyboardInterrupt):
            break

if __name__ == "__main__":

    p = config.Param(512, 10, 10, 22, 70, 16, 6, 50, 0, 'Mtheta/')
    # freque, spdfre, step_time, nIn_a, nOu_a, nIn_b, nOu_b, r, d, theta_path

    queue_matrix = Queue()
    queue_speed = Queue()   

    process1 = Process(target=receiveMatrixFun, kwargs={"p":p, "queue_matrix":queue_matrix})
    process2 = Process(target=receiveSpeedFun, kwargs={"p":p, "queue_speed":queue_speed})
    process3 = Process(target=estimateOutputFun, kwargs={"p":p, "queue_matrix":queue_matrix, "queue_speed":queue_speed})
    process4 = Process(target=uploadRmFileFun, kwargs={})

    process1.start()
    process2.start()   
    process3.start()
    process4.start()

    try:
        pass
        process1.join()
        process2.join()
        process3.join()
        process4.join()
    except(KeyboardInterrupt):
        process1.terminate()
        process1.join()
        process2.terminate()
        process2.join()
        process3.terminate()
        process3.join()
        process4.terminate()
        process4.join()

        # receiveMatrixFun.p0End()
        # receiveSpeedFun.p0End()
        print("Finished successfully!")
        
