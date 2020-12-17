import os

class UploadRemoveFile:
    def __init__(self, password, source_fold, destination_fold, admin_ip):
        self.password = password
        self.source_fold = source_fold
        self.destination_fold = destination_fold
        self.admin_ip = admin_ip

    def uploadFile(self, file_fold, file_name):
        uploadCommand = 'sshpass -p ' + self.password + ' scp -C ' + self.source_fold + file_fold \
                        + file_name + ' ' + self.admin_ip + ':' + self.destination_fold + file_fold
        print(uploadCommand)
        exit_code = os.system(uploadCommand)
        return exit_code

    def removeFile(self, file_fold, file_name):
        removeCommand = 'rm ' + self.source_fold + file_fold + file_name 
        print(removeCommand)
        exit_code = os.system(removeCommand)
        return exit_code

if __name__ == "__main__":
    password = '123'
    source_fold = '/IVHM/'
    destination_fold = '/home/wy/matlab_example/scpTest/'
    admin_ip = 'wy@202.121.180.27'

    file_fold = 'input/'
    file_name = 'abnormal_result.csv'
    inputUpRm = UploadRemoveFile(password, source_fold, destination_fold, admin_ip)
    ec1 = inputUpRm.uploadFile(file_fold, file_name)
    ec2 = inputUpRm.removeFile(file_fold, file_name)
    print(ec1, ec2)
