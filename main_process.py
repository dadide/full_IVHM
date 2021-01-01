# import receiveMatrixProcess
# import receiveSpeedProcess
import estimateOutputProcess
from writeUploadRemoveFileClass import UploadRemoveFile, WriteFile
import time
import config
import numpy as np
from multiprocessing import Process, Queue


matrix_test_flag = 1
speed_test_flag = 1

def receiveMatrixFun(p, queue_matrix):

    if matrix_test_flag == 1:
        print('matrix_test_flag == 1')
        config.testFun(p, 1, queue_matrix)      # generate data we need to test
    else:
        print('matrix_test_flag == 0')
        count = 1

        logger = config.setUpLogger("receive")
        AbnormityWriter = WriteFile('abnormity/', config.step_num*10)   #so every 30s*10=5min will generate a abnormal csv 
        
        # get the pointer of a mat
        mat = np.zeros([p.step_time*p.freque, p.nIn_a], np.float64)
        tmp = np.asarray(mat)
        dataptr = tmp.ctypes.data_as(POINTER(c_double))

        abnorm_threshold = np.zeros([1, p.nIn_a]) + 100
        # abnorm_threshold = np.array([100, 100, 100, 100, 100, 100, 100, 100, 100])


        while True:
            receiveMatrixProcess.receive_data(dataptr, p.step_time, p.freque)
            mat_str = mat.tostring()
            queue_matrix.put(mat_str)

            abnormity = np.sum( (abs(mat) > abnorm_threshold), axis=0)
            AbnormityWriter.save2File(abnormity.reshape(1, p.nIn_a)) 

            message = 'Received no.%d step data' % count
            print(message)
            logger.info(message)

            count = count + 1



def receiveSpeedFun(p, queue_speed):

    if speed_test_flag == 1:
        print('speed_test_flag == 1')
        config.testFun(p, 2, queue_speed)       # generate data we need to test
    else:
        print('speed_test_flag == 0')
        count = 1
        
        # get the pointer of a vec
        vec = np.zeros([p.step_time*p.spdfre, 1], np.float64)
        tmp = np.asarray(vec)
        dataptr = tmp.ctypes.data_as(POINTER(c_double))

        while True:
            receiveSpeedProcess.receive_data(dataptr, p.step_time, p.spdfre)
            vec_str = vec.tostring()
            queue_speed.put(vec_str)

            count = count + 1



def estimateOutputFun(p, queue_matrix, queue_speed):

    
    ResultWriter = WriteFile('result/', config.step_num)
    InputWriter = WriteFile('input/', config.step_num)
    SpeedWriter = WriteFile('speed/', config.step_num)

    [theta_a3d, theta_b3d] = estimateOutputProcess.loadTheta(p)
    last_r_d = np.zeros([p.r + p.d, p.nIn_a])
    
    logger = config.setUpLogger("estimate")

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
                    logger.info(message)
                    print(message)
                else:
                    InputWriter.save2File(batch_input)
                    SpeedWriter.save2File(batch_speed) 
                    message = 'This step does not need calculate'
                    logger.info(message)
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
            UpRm.findUploadRemoveFile('abnormity/')
            time.sleep(1)     
        except(KeyboardInterrupt):
            break

if __name__ == "__main__":

    # p = config.Param(512, 10, 10, 22, 70, 16, 6, 50, 0, 'MTheta/')
    p = config.Param(512, 10, 10, 9, 70, 6, 3, 50, 0, 'MTheta/')

    # freque, spdfre, step_time, nIn_a, nOu_a, nIn_b, nOu_b, r, d, theta_path

    queue_matrix = Queue()
    queue_speed = Queue()   

    process1 = Process(target=receiveMatrixFun, kwargs={"p":p, "queue_matrix":queue_matrix})
    process2 = Process(target=receiveSpeedFun, kwargs={"p":p, "queue_speed":queue_speed})
    process3 = Process(target=estimateOutputFun, kwargs={"p":p, "queue_matrix":queue_matrix, "queue_speed":queue_speed})
    # process4 = Process(target=uploadRmFileFun, kwargs={})

    process1.start()
    process2.start()   
    process3.start()
    # process4.start()

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
        # process4.terminate()
        # process4.join()

        # receiveMatrixFun.p0End()
        # receiveSpeedFun.p0End()
        print("Finished successfully!")
        
