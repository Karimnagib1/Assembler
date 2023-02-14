# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 17:48:14 2022
        
@author: kareem ElZeky
"""
import random

def twosComplement(num):
    s = ''
    try:
        i = num.rindex('1')
        s = num[i:]
        for j in range(i-1,-1,-1):
            if num[j] == '1':
                s = '0' +s
            else:
                s = '1' + s
        return s
    except:
        return num

locs = {}

MRI = {"And": ('0000','1000'), "ADD": ('0001','1001'), "LDA": ('0010','1010'), "STA": ('0011','1011'),
       "BUN": ('0100','1100'),"BSA":('0101','1101'), 'ISZ': ('0110','1110')}
non_MRI = {'CLA': '0111100000000000',
       'CLE': '0111010000000000', 'CMA': '0111001000000000', "CME":'0111000100000000' ,
       "CIR":'0111000010000000' , "CIL": '0111000001000000' ,"INC": '0111000000100000' ,
       "SPA": '0111000000010000' , "SNA": '0111000000001000', "SZA": '0111000000000100' ,
       "SZE": '0111000000000010' ,"HLT": '0111000000000001', "INP":'1111100000000000' ,
       "OUT": '1111010000000000', "SKI": '1111001000000000', "SKO": '1111000100000000',
       "ION": '1111000010000000' , "IOF": '1111000001000000'}

PI = ['ORG', 'END']


def firstPass(file):    
    LC = 0
    labels = {}
    f = open(file, 'r')
    
    for line in f:
        line = line.strip()
        lineWords = line.split(' ')
        l = []
        for i in lineWords:
            if i != '':
                if '\t' in i:
                    i = i.split('\t')
                    for k in i:
                        l.append(k)
                else:
                    l.append(i)

        if l[0][-1] == ',':
            labels[l[0][:-1]] = '0x' + str(LC)
            LC+=1
        elif l[0] == 'ORG':
            LC = int(l[1])
        elif l[0] == 'END':
            break
        else:
            LC+=1
    f.close()
    return labels
            

def secondPass(file, labels):
    LC =0
    f = open(file, 'r')
    x = f'machineCode{random.randint(0,1000)}.txt'
    print('Check file',x)
    r = open(x, 'a')
    counter = 0
    for line in f:
        counter += 1
        line = line.strip()
        lineWords = line.split(' ')
        l = []
        
        for i in lineWords:
            if i != '':
                if '\t' in i:
                    i = i.split('\t')
                    for k in i:
                        l.append(k)
                else:
                    l.append(i)
                    
        if l[0] in PI:
            if l[0] == 'ORG':
                LC = int(l[1])
                
            elif l[0] == 'END':
                break
        elif l[0][:-1] in labels:
            
            loc = bin(int(str(LC),16))[2:]
            while len(loc) < 12:
                loc = '0' + loc
                
            if l[1] == 'HEX':    
                temp = bin(int(l[2],16))[2:]
                
                if temp[0] == 'b':
                    temp = temp[1:]
                    while len(temp) < 16:
                        temp = '0' + temp
                    temp = twosComplement(temp)
                
                else:
                    while len(temp) < 16:
                        temp = '0' + temp

                temp = loc + '\t' +  temp + '\n'
        
            elif l[1] == 'DEC':
                temp = bin(int(l[2]))[2:]

                if temp[0] == 'b':
                    temp = temp[1:]
                    
                    while len(temp) < 16:
                        temp = '0' + temp

                    temp = twosComplement(temp)
                else:
                    while len(temp) < 16:
                        temp = '0' + temp
                temp = loc + '\t' +  temp + '\n'
            
            r.write(temp)
            LC += 1
        elif l[0] in MRI:
            address = bin(int(labels[l[1]],16))[2:]
            while len(address) < 12:
                address = '0' + address
            loc = bin(int(str(LC),16))[2:]
            while len(loc) < 12:
                loc = '0' + loc
            
            
            if l[-1] != 'I':
                temp = loc + '\t'+ MRI[l[0]][0] + address + '\n'
            else:
                temp = loc + '\t'+ MRI[l[0]][1] + address + '\n'
            LC +=1
            r.write(temp)
        elif l[0] in non_MRI:
            loc = bin(int(str(LC),16))[2:]
            while len(loc) < 12:
                loc = '0' + loc 
            r.write(loc+ '\t'+ non_MRI[l[0]] + '\n')
            LC += 1
        else:
            raise Exception('Error in line '+ str(counter))
    r.close()
    f.close()

def assemble(file):
    labels = firstPass(file)
    print(labels)
    secondPass(file,labels)
                               
assemble('test2.txt')
# assemble('test2.txt')