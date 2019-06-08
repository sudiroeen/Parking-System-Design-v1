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
    dKey = string.split('_')[0]
    dValue = string.split(dKey)[-1]
    return dKey, dValue

# def string2dict(string):
#     kal = ''
#     count = 0
#     dID = ''
#     for h in string:
#         if (count < 1) and (str(h) == '_'):
#             dID = kal
#             kal = ''
#             count += 1
#         kal = kal + str(h)
#     return dID, kal

def isiKamus(qomus, index, isi):
    try:
        if len(qomus[index]):
            pass
    except:
        qomus[index] = []
    qomus[index].append({len(qomus[index])+1 : isi})
    return qomus

def duit(dIn, dOut):
    biaya = float(dOut[1] - dIn)/3600.0 * 1000
    saldo_akhir = dOut[0] - biaya
    return biaya, saldo_akhir

