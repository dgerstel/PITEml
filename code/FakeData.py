#!/usr/bin/python
# -*- coding: utf-8 -*-



import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier

class FakeData():
    def __init__(self):
        pass

	def __call__(self):
		pass

    def generateFakeData(self, sourcepath, fake_data_path, number_of_fake_samples, p_value_list):
        from_sensors = np.loadtxt(sourcepath, delimiter=",")# pobieranie danych z pliku z oryginalnymi 41 danymi
        average_list = [i[0] for i in from_sensors]
        average_par = (np.average(average_list),np.std(average_list))#average parameters
        rms_list = [i[1] for i in from_sensors]
        rms_par = (np.average(rms_list),np.std(rms_list))#RMS parameters
        skewness_list = [i[2] for i in from_sensors]
        skewness_par = (np.average(skewness_list),np.std(skewness_list)) #skewness parameters
        kurtosis_list = [i[3] for i in from_sensors]
        kurtosis_par = (np.average(kurtosis_list),np.std(kurtosis_list)) #kurtosis parameters
        result = []
        for i in range(number_of_fake_samples):
            random_data = [average_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*average_par[1],p_value_list[0][1]*average_par[1]),
						rms_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*rms_par[1],p_value_list[0][1]*rms_par[1]),
						skewness_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*skewness_par[1],p_value_list[0][1]*skewness_par[1]),
						kurtosis_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*kurtosis_par[1],p_value_list[0][1]*kurtosis_par[1]),
						0]
            result.append(random_data)
        np.savetxt(fake_data_path, result, delimiter=",", fmt='%.7f', newline='\n')
        saved_value = np.loadtxt(fake_data_path, delimiter=",")


    def addFakeDataToExistingFile(self, sourcepath, fake_data_path, number_of_fake_samples, p_value_list):
        from_sensors = np.loadtxt(sourcepath, delimiter=",")# pobieranie danych z pliku z oryginalnymi 41 danymi
        average_list = [i[0] for i in from_sensors]
        average_par = (np.average(average_list),np.std(average_list))#average parameters
        rms_list = [i[1] for i in from_sensors]
        rms_par = (np.average(rms_list),np.std(rms_list))#RMS parameters
        skewness_list = [i[2] for i in from_sensors]
        skewness_par = (np.average(skewness_list),np.std(skewness_list)) #skewness parameters
        kurtosis_list = [i[3] for i in from_sensors]
        kurtosis_par = (np.average(kurtosis_list),np.std(kurtosis_list)) #kurtosis parameters
        result = []
        f = open(fake_data_path, 'a')
        for i in range(number_of_fake_samples):
            random_data = [average_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*average_par[1],p_value_list[0][1]*average_par[1]),
						rms_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*rms_par[1],p_value_list[0][1]*rms_par[1]),
						skewness_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*skewness_par[1],p_value_list[0][1]*skewness_par[1]),
						kurtosis_par[0] + random.choice([1,-1])*random.uniform(p_value_list[0][0]*kurtosis_par[1],p_value_list[0][1]*kurtosis_par[1]),
						0]
            msg = '%.7f' % random_data[0] + "," \
                  + '%.7f' % random_data[1] + "," \
                  + '%.7f' % random_data[2] + "," + \
                  '%.7f' % random_data[3] + "," + \
                  '%.7f' % 0 + "\n"

            f.write(msg)
            result.append(random_data)
        # f.write('hi there\n') # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it
        saved_value = np.loadtxt(fake_data_path, delimiter=",")



class KNN():
	def __init__(self,fakedatapath):
		self.from_sensors = np.loadtxt("dane41.dat", delimiter=",")
		self.fake_data = np.loadtxt(fakedatapath, delimiter=",")

	def __call__(self):
		pass

	def TrainAndPredict(self,k,myweights = 'distance', myalgorithm = 'auto'):
		self.neigh = KNeighborsClassifier(n_neighbors=k)
		self.from_sensors = [i[0:-1] for i in self.from_sensors]
		self.fake_data = [i[0:-1] for i in self.fake_data]
		traindata = self.from_sensors[0:30] + self.fake_data[0:30] # Biore 30 serii danych z sensora i 30 serii danych zmyślonych(błędnych)
		targetvalues = [1 for i in range(30)] + [0 for i in range(30)] # tablica o wartosciach 0 i 1
		traindata = [np.ndarray.tolist(i) for i in traindata]
		self.neigh.fit(traindata, targetvalues)
		print "n_neighbors: "+str(k)+"   weights: "+str(myweights)+"   algorithm: "+str(myalgorithm)
		print "Predykcja dla danych z sensora:" + str(self.neigh.predict(self.from_sensors[30:]))
		print "Predykcja dla danych zmyslonych:" + str(self.neigh.predict(self.fake_data[30:])) 
		print "Prawdopodobienstwo poprawnego oszacowania(dla danych zmyslonych): \n" + str(self.neigh.predict_proba(self.fake_data[30:]))
		print "\n"
######################### PROCESS DATA ######################### 


c = FakeData() # tworzy nowy plik z sztucznie wygenerowanymi danymi
c.generateFakeData("dane41.dat", "danefake 1_2-1_5.dat", 50, [[1.2,1.5], [1.2,1.5], [1.2,1.5], [1.2,1.5]]) # losuje 40serii danych. Minimalne wartosci: mean +- 4*std. Maksymalne wartosci: mean +- 5*std
c.generateFakeData("dane41.dat", "danefake 1_5-1_7.dat", 50, [[1.5,1.7], [1.5,1.7], [1.5,1.7], [1.5,1.7]])
c.generateFakeData("dane41.dat", "danefake 1_7-2.dat", 50, [[1.7,2], [1.7,2], [1.7,2], [1.7,2]])
c.generateFakeData("dane41.dat", "danefake 1-2.dat", 50, [[1,2], [1,2], [1,2], [1,2]])
c.generateFakeData("dane41.dat", "danefake 2-3.dat", 50, [[2,3], [2,3], [2,3], [2,3]])
c.generateFakeData("dane41.dat", "danefake 3-4dat", 50, [[3,4], [3,4], [3,4], [3,4]])
c.generateFakeData("dane41.dat", "danefake 4-5.dat", 50, [[4,5], [4,5], [4,5], [4,5]])
#c.addFakeDataToExistingFile("dane41.dat", "danefake.dat", 5, [[1.4,1.5], [1.4,1.5], [1.4,1.5], [1.4,1.5]])# do pliku juz istniejącego dopisuje nowe sztuczne dane, w ten sposob w 1 pliku możemy miec sztuczne dane o roznych parametrach p


for filename in ["danefake 1_2-1_5.dat", "danefake 1_5-1_7.dat", "danefake 1_7-2.dat", "danefake 1-2.dat", "danefake 2-3.dat", "danefake 3-4dat", "danefake 4-5.dat" ]:
	print "############# FILENAME #############"
	print filename
	print "############# FILENAME #############" 	
	for k in range(3,7):
		d = KNN(filename)
		d.TrainAndPredict(k,'distance','auto')






