import os
import cv2
import socket
import pickle
import struct
import time
import threading
import shutil


def img2string(capture, encode_param):
   result, bufimg = cv2.imencode('.jpg', capture, encode_param)
   data = pickle.dumps(bufimg, 0)
   size = len(data)
   siapKirim = str(struct.pack(">L", size) + data)
   return siapKirim


def string2img(client, nbit= 4096, tipeImg= cv2.IMREAD_COLOR):
    data = b""
    payload_size = struct.calcsize(">L")

    while len(data) < payload_size:
        data += client.recv(nbit)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client.recv(nbit)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame=pickle.loads(frame_data)
    frame = cv2.imdecode(frame, tipeImg)
    return frame

def string2dict(string):
    kal = ''
    count = 0
    dID = ''
    for h in string:
        if (count < 1) and (str(h) == '_'):
            dID = kal
            kal = ''
            count += 1
        kal = kal + str(h)
    return dID, kal

def isiKamus(qomus, index, isi):
    try:
        if len(qomus[index]):
            pass
    except:
        qomus[index] = []
    qomus[index].append({len(qomus[index])+1 : isi})
    return qomus

def compoundData(strIn, strOut):
    ## namaIn
    #ID_Tanggal_Jam_saldoAwal_Gate-1_Check-In_harga.jpg
    ##fullnameout
    #ID/Nomor_Tanggal_Jam_saldoAwal_Gate-2_Check-Out
    sIn = strIn.split('.jpg')[0].split('_')
    sOut = strOut.split('_')

    #ID, GateCheckIn, TImeOut, TimeIn, SaldoAwal, harga
    string = sIn[0] + '_' + sIn[4] + '_' + sOut[3] + '_'+ sIn[3] + '_' + sOut[4] + '_' + sIn[-1]
    return string

def complithitung(stringIO):
    ##stringIO
    #ID, GateCheckIn, TImeOut, TimeIn, SaldoAwal, harga

    ID, GateCheckIn, TimeOut, TimeIn, SaldoAwal, harga = stringIO.split('_')
    TimeTotal = float(TimeOut) - float(TimeIn)
    banyakJam = TimeTotal/3600
    Biaya = int(banyakJam * int(harga))
    #Biaya = int(banyakJam) * harga

    if SaldoAwal != 'manual':
        SaldoAkhir = int(SaldoAwal) - Biaya
    else:
        SaldoAkhir = 'manual'

    #ID, GateCheckIn, TImeOut, TimeIn, TimeTotal, Biaya, SaldoAwal, SaldoAkhir, harga
    return '_'.join(['_'.join(stringIO.split('_')[0:4]), str(TimeTotal), str(Biaya), stringIO.split('_')[4], str(SaldoAkhir), stringIO.split('_')[-1]])

def tampilCantik(waktuDetik):
    fstr = float(waktuDetik)
    acak = time.ctime(fstr).split(' ')
    formatted = acak[0] + ', ' + acak[2] + ' ' + acak[1] + ' ' + acak[4] + ' (' + acak[3] + ')'
    return formatted
