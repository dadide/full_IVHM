# import receiveMatrixProcess
# import receiveSpeedProcess
# import estimateOutputProcess
from writeUploadRemoveFileClass import UploadRemoveFile, WriteFile
import time
import config
import numpy as np
from multiprocessing import Process, Queue


def receiveMatrixFun():
    pass

def receiveSpeedFun():
    pass

def estimateOutputFun(queue_matrix, queue_speed):
   
    p = config.Param(512, 10, 10, 22, 7, 16, 6, 50, 0, 'Mtheta/')
    # freque, spdfre, step_time, nIn_a, nOu_a, nIn_b, nOu_b, r, d, theta_path

    ResultWriter = WriteFile('./result/', 3)
    InputWriter = WriteFile('./input/', 3)
    SpeedWriter = WriteFile('./speed/', 3)

    [theta_a3d, theta_b3d] = estimateOutputProcess.load_theta(p)
    last_r_d = np.zeros([p.r + p.d, p.nIn_a])
   
    while True:
        try:
            if queue_matrix.empty() or queue_speed.empty():
                time.sleep(1)
            else:
                mat_str = queue_matrix.get()
                vec_str = queue_speed.get()

                batch_input = np.fromstring(mat_str, dtype=np.float64).reshape(p.step_time * p.freque, p.nIn_a)
                batch_speed = np.fromstring(vec_str, dtype=np.float64).reshape(p.step_time * p.spdfre, 1)
                
                stacked_batch_input = np.vstack((last_r_d, batch_input))
                last_r_d = batch_input[-(p.r + p.d):, :]

                t1 = time.time()
                [phi_a, phi_b, y_batch_true_b, ks, ke] = estimateOutputProcess.construct_data(p, stacked_batch_input)
                model_index = estimateOutputProcess.choose_model(phi_b, theta_b3d, y_batch_true_b, ks, ke)
                y_batch_pred_a = estimateOutputProcess.predict_output(phi_a, theta_a3d, model_index, ks, ke)
                t2 = time.time()

                InputWriter.save2File(batch_input)
                SpeedWriter.save2File(batch_speed) 
                ResultWriter.save2File(y_batch_pred_a)                                              
                t3 = time.time()
                print('estimate consumes:%.2f, write consumes:%.2f', t2-t1, t3-t2)

        except(KeyboardInterrupt):
            break


def uploadRmFileFun():
    UpRm = UploadRemoveFile(config.admin_ip, config.password, config.source_fold, config.destination_fold)
    while True:
        try:
            UpRm.findUploadRemoveFile('input/')
            time.sleep(1)
            # UpRm.findUploadRemoveFile('result/')
            # time.sleep(1)
            UpRm.findUploadRemoveFile('log/')
            time.sleep(1)            
        except(KeyboardInterrupt):
            break

if __name__ == "__main__":
    
    # a.displayParam()    
    process1 = Process(target=receiveMatrixFun, kwargs={})
    process2 = Process(target=receiveSpeedFun, kwargs={})
    process3 = Process(target=estimateOutputFun, kwargs={})
    process4 = Process(target=uploadRmFileFun, kwargs={})

    # process1.start()
    # process2.start()   
    # process3.start()
    process4.start()

    try:
        # process1.join()
        # process2.join()
        # process3.join()
        process4.join()
    except(KeyboardInterrupt):
        # process1.terminate()
        # process1.join()
        # process2.terminate()
        # process2.join()
        # process3.terminate()
        # process3.join()
        process4.terminate()
        process4.join()

        # receiveMatrixFun.p0End()
        # receiveSpeedFun.p0End()
        # print("Finished successfully!")
        
