%hello Sasha! постигаем githab
import RPi.GPIO as GPIO
#from gpio import GPIO
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import string
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.IN)


D=[26,19,13,6,5,11,9,10]

def Let_it_light(pins):
    for k in range (8):
        GPIO.output(pins[k], 1) 

def Let_it_dark(pins):
    for k in range (8):
        GPIO.output(pins[k], 0)
     
def decToBinList(number):
    c=bin(number)[2:] 
    c=c[::-1] 
    s=[0, 0, 0, 0, 0, 0, 0, 0 ] 
    for k in range (len(c)):
        s[k]=int(c[k])        
    s.reverse()
    return s

def lightNumber(pins,List_of_number):
    Let_it_dark(pins)
    for i in range (7,-1,-1): 
        if List_of_number[i]==1:
            GPIO.output(pins[i], List_of_number[i]) 
def num2dac(pins,j): #8
    a=decToBinList(j)
    lightNumber(pins,a)
def adc():
    c=0
    b=255
    j=int((c+b)/2)
    while True:
        num2dac(D,j)
        time.sleep(0.01)
        if b-c==2 or j==0 : 
            Voltage=int(((j*3.3)/256)*100)/100
            print("Digital value: ", j , ", Analog Value: ", Voltage, "V")
            return j
            break
        elif GPIO.input(4)==1:
            c=j
            j=int((c+b)/2)    
        elif GPIO.input(4)==0: 
            b=j
            j=int((c+b)/2) 
try:
    while adc()>0:
        GPIO.output(17,0)
        print ("uuu")
        time.sleep(1)

    t_st = time.time()
    listV = [] 
    listT = [] 
    measure = []
    GPIO.output(17,1)
    while adc() < 256:
        listT.append(time.time()-t_st)
        measure.append(adc())
        listV.append((adc()*3.3)/256)
        time.sleep(0.01)
        if adc()>=252:
            break
    GPIO.output(17,0)
    while adc() > 0:
        listT.append(time.time()-t_st)
        measure.append(adc())
        listV.append((adc()*3.3)/256)
        time.sleep(0.01)
    plt.plot(listV, 'r-')
    plt.show()
    np.savetxt('data.txt', listV, fmt='%d') #7

    dT=0
    for i in range (len(listT)-1):
        dT=dT+abs(listT[i+1]-listT[i]
    dT=dT/(len(listT)-1)
    dV=0
    for i in range (len(listV)-1):
        dV=dV+abs(listV[i+1]-listV[i]
    dV=dV/(len(listV)-1)
    X =  [dT, dV]
    np.savetxt('settings.txt', X, fmt='%f') 

    plt.plot(listT,listV, 'r-')#10
    plt.title('График зависимости напряжения на конденсаторе от времени')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.show()
finally:
        for i in range (7,-1,-1):
            GPIO.output(D[i], 0)
