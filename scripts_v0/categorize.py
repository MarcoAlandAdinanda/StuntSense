import numpy as np

class Categorize():
    def __init__(self, param, age, gender, size):
        self.param = param
        self.age = int(age)
        self.gender = gender
        self.size = float(size)
    
    def get_th(self):
        th_list = np.zeros(7)
        if(self.gender == "Laki-laki"):
            if(self.param == "Panjang" and self.age >=0 and self.age <=24):
                print("Penggolongan Panjang Badan Laki-laki (0-24)")
                th_list[0] = (0.0031*((self.age+1)**3)) - (0.1685*((self.age+1)**2)) + (3.7408*(self.age+1)) + 41.996
                th_list[1] = (0.0031*((self.age+1)**3)) - (0.1680*((self.age+1)**2)) + (3.7738*(self.age+1)) + 43.864
                th_list[2] = (0.0032*((self.age+1)**3)) - (0.1678*((self.age+1)**2)) + (3.8046*(self.age+1)) + 45.782
                th_list[3] = (0.0032*((self.age+1)**3)) - (0.1678*((self.age+1)**2)) + (3.8395*(self.age+1)) + 47.651
                th_list[4] = (0.0032*((self.age+1)**3)) - (0.1674*((self.age+1)**2)) + (3.8701*(self.age+1)) + 49.566
                th_list[5] = (0.0029*((self.age+1)**3)) - (0.1582*((self.age+1)**2)) + (3.8297*(self.age+1)) + 51.565
                th_list[6] = (0.0032*((self.age+1)**3)) - (0.1659*((self.age+1)**2)) + (3.9249*(self.age+1)) + 53.358
            elif(self.param == "Tinggi" and self.age >=24 and self.age <= 60):
                print("Penggolongan Tinggi Badan Laki-laki (24-60)")
                th_list[0] = (0.4932*(self.age-24)) + 78.265
                th_list[1] = (0.5361*(self.age-24)) + 81.368
                th_list[2] = (0.5784*(self.age-24)) + 84.491
                th_list[3] = (0.6213*(self.age-24)) + 87.597
                th_list[4] = (0.6634*(self.age-24)) + 90.717
                th_list[5] = (0.7063*(self.age-24)) + 93.826
                th_list[6] = (0.7500*(self.age-24)) + 96.918
        
        elif(self.gender == "Perempuan"):
            if(self.param == "Panjang" and self.age >=0 and self.age <=24):
                print("Penggolongan Panjang Badan Perempuan (0-24)")
                th_list[0] = (0.0026*((self.age+1)**3)) - (0.1390*((self.age+1)**2)) + (3.2942*(self.age+1)) + 41.667
                th_list[1] = (0.0026*((self.age+1)**3)) - (0.1415*((self.age+1)**2)) + (3.3779*(self.age+1)) + 43.453
                th_list[2] = (0.0026*((self.age+1)**3)) - (0.1422*((self.age+1)**2)) + (3.4457*(self.age+1)) + 45.262
                th_list[3] = (0.0027*((self.age+1)**3)) - (0.1430*((self.age+1)**2)) + (3.5099*(self.age+1)) + 47.099
                th_list[4] = (0.0027*((self.age+1)**3)) - (0.1451*((self.age+1)**2)) + (3.5895*(self.age+1)) + 48.898
                th_list[5] = (0.0028*((self.age+1)**3)) - (0.1471*((self.age+1)**2)) + (3.6650*(self.age+1)) + 50.724
                th_list[6] = (0.0028*((self.age+1)**3)) - (0.1481*((self.age+1)**2)) + (3.7327*(self.age+1)) + 52.533  
            elif(self.param == "Tinggi" and self.age >=24 and self.age <= 60):
                print("Penggolongan Tinggi Badan Perempuan (24-60)")
                th_list[0] = (0.5237*(self.age-24)) + 76.477
                th_list[1] = (0.5664*(self.age-24)) + 79.696
                th_list[2] = (0.6087*(self.age-24)) + 82.945
                th_list[3] = (0.6502*(self.age-24)) + 86.181
                th_list[4] = (0.6922*(self.age-24)) + 89.431
                th_list[5] = (0.7340*(self.age-24)) + 92.673
                th_list[6] = (0.7770*(self.age-24)) + 95.896

        return th_list

    def get_status(self, th_list):
        if(self.size<th_list[0]):
            status = "severely_stunted"
        elif(self.size>=th_list[0] and self.size<th_list[1]):
            status = "stunted"
        elif(self.size>=th_list[1] and self.size<=th_list[6]):
            status = "normal"
        elif(self.size>th_list[6]):
            status = "tinggi"

        return status