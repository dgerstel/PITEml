#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def fuzzyRating(sensor_parameters_list ,qualityFunc, weight_list=[1,1,1,1], unit_list=[1,1,1,1]):
   #  sensor_parameters_list-
    # nalezy podac parametry sensora, w postaci listy, tj:
    # [mu, sig, k, s]
    # weight_lists
    # lista wag, które określają jak mocno odległości w odpowiednich wymiarach wpływają na ocene

    # Tutaj wpisalem parametry "benchmarkowego" sensora
    # nie mam go jeszcze wiec wziłem 1 linijke z dobrych danych

    # dane zawierają po kolei: średnią, RMS, skośność, kurtozę

    average_benchmark = 0.16652
    rms_benchmark = 2.717048
    skewness_benchmark = -0.019911
    kurtosis_benchmark = 0.576181

   #nastepnie trzeba w jakis sposob porowdac jednostki, bo jezeli jakas wartosc benchmarkowa wynosi 0.1 a inna 100
   # to odleglosc w tych 2 przestrzeniach o 1 nie moze byc traktowana jako
   # taka sama odleglosc od idealnego sensora
   # domyslnie pojedynczą jednostką w każdej przestrzeni jest wartość benchmarkowa w tejże przestrezeni

    average_unit = average_benchmark * unit_list[0]
    rms_unit = rms_benchmark * unit_list[1]
    skewness_unit = skewness_benchmark * unit_list[2]
    kurtosis_unit = kurtosis_benchmark * unit_list[3]

   # teraz wyliczamy dystans r, jednak wykorzystujemy liste wag
   # któa określa który wymiar jest ważniejszy
    average_distance = (sensor_parameters_list[0] - average_benchmark )/average_unit
    rms_distance = (sensor_parameters_list[1] - rms_benchmark )/rms_unit
    skewness_distance = (sensor_parameters_list[2] - skewness_benchmark )/skewness_unit
    kurtosis_distance = (sensor_parameters_list[3] - kurtosis_benchmark )/kurtosis_unit

   # teraz mozemy wyznaczyc odleglosc r ktora nazwalem distance
    distance = (weight_list[0] * average_distance**2 +
                weight_list[1] * rms_distance**2 +
                weight_list[2] * skewness_distance**2 +
                weight_list[3] * kurtosis_distance**2)**0.5

   # oczywiscie mogibysmy miec 1 liste wspolczynnikow wagowych, a nie
   # weight_list i unit_list, ale w ten sposób możemy rozseparować
   # częsć któa określa specyfikę przestrzeni: unit_list
   # oraz częsc odpowiadajacą za nasze preferencję, które się mogą zmieniać w
   # zależności od tego co potrzebujemy: weight_list

    return qualityFunc(distance)


def one_divideby_r(r):
    return 1/r

def exp_norm(r, A=100.0, alpha=1.0):
    """
    Quality function -- normalised exp
    returns (0,A], so it doesn't have singularity at r=0,
    but returns A there.

    =======
    params:
    r - distance in the feautre space
    A - ideal sensor score
    alpha - attenuation coefficient (or sensitivity to the distance r);
            should be optimised so (nearly) all good sensors score quality >= 50 %
    """ 
    return A * np.exp(-alpha * r)

sensor_data = [0.023619,2.879776,-0.065719,0.868431]

k=fuzzyRating(sensor_data,one_divideby_r)
print(k)

k=fuzzyRating(sensor_data,exp_norm)
print(k)

# TESTING
perfect_sensor = [0.16652, 2.717048, -0.019911, 0.576181]
almost_perfect_sensor = [0.16, 2.71, -0.019, 0.576]

#k=fuzzyRating(perfect_sensor, one_divideby_r)  # 1/0 !
#print(k)

k=fuzzyRating(perfect_sensor, exp_norm)
print "Perfect sensor; Q = A*exp(-alph*r): ", k, ' %'

k=fuzzyRating(almost_perfect_sensor, one_divideby_r)
print "Almost perfect sensor; Q = 1/r", k

k=fuzzyRating(almost_perfect_sensor, exp_norm)
print "Almost perfect sensor; Q = A*exp(-alph*r): ", k, ' %'
