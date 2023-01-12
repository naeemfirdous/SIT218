import random
import hashlib
import socket
import numpy as np
import pandas as pd
import pickle
import gzip
import hmac
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad


IDedge='IDedge1234'
random.seed(30)
hlist=[]
L1=[]
L3=[]
L4=[]
while True:            #Extracting the saved file
    GEDGE = open('Edge_Device_initialization_parameter.txt', 'rb')
    List=open('Edge_Device_initialization_parameter_withouthashing.txt', 'rb')
    while True:
        try:
            hashlist = pickle.load(GEDGE)
        except EOFError:
            break
        print(hashlist)
        try:
            list = pickle.load(List)
        except EOFError:
            break
        print(list)
    break
#Extracting the values from the list
IDgwH=hashlist[0]
IDedgeH=hashlist[1]
rH=hashlist[2]
EinitH=hashlist[3]
IDgw=list[0]
IDedge=list[1]


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Host = socket.gethostbyname(socket.gethostname())
    Port = 5050
    s.connect((Host, Port))
    print(f'Connected to{Host}')
    while True:
        send_M1 = pickle.dumps(IDedgeH) #encoding and sending hash of IDedge
        s.send(send_M1)
        receive_message2 = s.recv(4096) #received reponse from gatway
        message2 = pickle.loads(receive_message2) #decoding received message
        if IDgwH==message2:
            print("Gateway id matched") #ID matching
            cr = pd.read_csv('amplitude1.txt') #importing amplitude.txt
            r = list[2] #assigning the value of r and Einit from the extracted saved list
            Einit = list[3]
            X1=[chr(ord(a) ^ ord(b)) for a, b in zip(str(r), str(Einit))]
            X2 = "".join(X1) #XORing the string of r and Einit
            H=hashlib.md5(X2.encode('utf-8')) #calculating hash
            H1= H.hexdigest()
            Cr1=cr.iloc[0,0] #value of Cr extracted from 1st row of amplitude
            Cr=str(Cr1)
            print(f'value of cr is {Cr}')
            X3 = [chr(ord(a) ^ ord(b)) for a, b in zip(H1, Cr)]
            Ma = "".join(X3)#Calculated Ma by XOR ing  H1 and Cr
            print(Ma)
            msg = '{} {} {}'.format(IDedgeH, Ma, r)
            M3=hmac.new(bytes(list[3], 'latin-1'), msg=bytes(msg, 'latin-1'),
                         digestmod=hashlib.sha256).hexdigest().upper() #Calculatinh hash mac
            print(M3)

            L1.append(IDedgeH)
            L1.append(Ma)
            L1.append(M3)
            message3 = pickle.dumps(L1)#Appended the data to alist and using pickle encoded the message
            s.send(message3) #Sending M3 message
            print('sending M3')
            receive_message4 = s.recv(4096) #Receiving M4
            message4 = pickle.loads(receive_message4)
            Ekey=Cr # Setting Ekey value equal to Cr
            print(Ekey)
            Mb=message4[2] # extracting Mb from the M4 message received
            msg1 = '{} {} {}'.format(Mb, IDgwH, r)
            M4 = hmac.new(bytes(Ekey, 'latin-1'), msg=bytes(msg, 'latin-1'),
                              digestmod=hashlib.sha256).hexdigest().upper()# Calculating the hash mac
            if M4==message4[1]:
                print("value matched")
                ACK1=1 #setting ACK to 1
                ACK=str(ACK1)
                X5 = [chr(ord(a) ^ ord(b)) for a, b in zip(str(r), Ekey)]
                X6 = "".join(X5) # calculating XOR of r and Ekey
                H2 = hashlib.md5(X6.encode('utf-8'))
                H3 = H.hexdigest() # calculated hash of hash
                Ci=[chr(ord(a) ^ ord(b)) for a, b in zip(H3, Mb)]
                Ci = "".join(Ci) # calculated xor of H3 and Mb
                print(Ci)
                print(Cr)
                SN=[chr(ord(a) ^ ord(b)) for a, b in zip(Ci, Cr)]
                SNKey1 = "".join(SN) #calculating xor of Ci and Cr
                mybyte = bytearray(SNKey1, 'utf-8')
                SNkey = mybyte[0:16] #16 byte SNkey
                Einit=SNkey
                Seed1=random.randint(1,100)
                Seed=str(Seed1)#calculated seed
                Ctre=1 #set value to 1
                Key=SNkey #set Key to SNkey
                print(f'value of key is {Key}')
                L3.append(str(Ci))
                L3.append(Seed)
                L3.append(ACK)
                L3string= ','.join(L3)#append value to list and joined the value
                print(L3string)
                message5=L3string.encode('latin-1') #encoded the value we are facing issue with this step
                print(message5)
                iv=Random.new().read(AES.block_size)
                print(iv)
                aes = AES.new(Key, AES.MODE_CFB, iv)
                encd = aes.encrypt(message5)
                s.send(encd) #sending encrypted value
                print("Sending M5")
                L4.append(SNkey)
                L4.append(r)
                L4.append(Ctre)
                with open('mutualauthentication_device.txt', 'wb') as filehandle:
                    pickle.dump(L4, filehandle)
                break
            else:
                break


if __name__ == '__main__':
    main()




