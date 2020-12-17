# import receiveMatrixProcess
# import receiveSpeedProcess
# import estimateOutputProcess
# import updateRemoveFileProcess
# import init

class param: 
    def __init__(self, frequency, step_time, input_dim, output_dim):
        self.frequency = frequency
        self.step_time = step_time
        self.input_dim = input_dim
        self.output_dim = output_dim
      
   
    def displayParam(self):
        print("frequency : ", self.frequency, ", step_time: ", self.step_time, ", input_dim: ", self.input_dim, ", output_dim: ", self.output_dim)


if __name__ == "__main__":
    a = param(512, 10, 22, 7)
    a.displayParam()
    
    
