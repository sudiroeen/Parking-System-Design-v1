import socket
import threading
import cv2
import os
import pickle
import struct
import shutil
import json
from source.included import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = '127.0.89.67' 
port = 1234

clients = {}
qomus = {}

try:
	if os.path.isfile('Text/Permanent/kamus.txt'):
		print 'eksekusi'
		with open('Text/Permanent/kamus.txt', 'rb') as jsonBaca:
			qomus = json.load(jsonBaca)
	else:
		print 'else'
		qomus = {}
except:
	print 'except'
	qomus = {}

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
server.listen(10)
print('Server Ready...')
print('Ip Address of the Server::%s'%ip)

def handleMasuk(client, gateName):
	print 'Masuk'

	while True:
		try:
			#ID/Nomor_Tanggal_Jam_saldoAwal_Gate-1_Check-In
			msg = client.recv(2048)

			try:
				with open('Text/Permanent/harga/harga.txt') as h:
					harga = str(h.read()).split('\n')[0]
					if harga == '':
						continue
			except:
				pass
			#"ID": "_Tanggal_Jam_saldoAwal_Gate-1_Check-In_harga"
			ID, ISI = string2dict(msg + '_' + harga)

			kamus = isiKamus(qomus, ID, ISI)

			#"ID": "_Tanggal_Jam_saldoAwal_Gate-1_Check-In_harga"
			with open('Text/Permanent/kamus.txt', 'w') as apkm:
				json.dump(kamus, apkm)

			#ID/Nomor_Tanggal_Jam_saldoAwal_Gate-1_Check-In
			# namaGambar = msg.replace(msg.split('_')[3] + '_', '')

			with open('Text/Permanent/dIn.txt', 'a+') as aIn:
				aIn.write(msg + '\n')
			with open('Text/dTempIn-'+ gateName.split('-')[-1] + '.txt', 'w') as wkm:
				wkm.write(msg)

			img = string2img(client, 4096, cv2.IMREAD_COLOR)

			cv2.imwrite('Foto/'+ msg + '.jpg', img)
		except:
			clients.pop(gateName)
			print (gateName + 'has been logged out')
			continue

def handleKeluar(client, gateName):
	print 'Keluar'
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

	while True:
		try:
			ID = client.recv(1024)
			nama = ''
			try:
				#"ID": "_Tanggal_Jam_saldoAwal_Gate-1_Check-In_harga"
				with open('Text/Permanent/kamus.txt', 'rb') as rkm:
					bcKamus = json.load(rkm)
					isiID = str(bcKamus[ID][len(bcKamus[ID])-1][u'' + str(len(bcKamus[ID]))])
					nama = ID + isiID + '.jpg'
				client.send(nama)
				try:
					jumlahdetik = '_' + nama.split('_')[3]
					print "jumlahdetik: ", jumlahdetik
					harga = '_' + nama.split('.jpg')[0].split('_')[-1]
					print 'harga: ', harga
					namaGambar = nama.replace(jumlahdetik, '').replace(harga, '')
					print "namaGambar: ", namaGambar
					img = cv2.imread('Foto/'+namaGambar)
					strImg = img2string(img, encode_param)
				except:
					print 'Image no longer exist'
					continue
				client.sendall(strImg)
				dOut = client.recv(4096)

				dOutFix = dOut.replace(dOut.split('_')[3] + '_', '')
				with open('Text/Permanent/dOut.txt', 'a+') as aOut:
					aOut.write(dOutFix + '\n')
				with open('Text/dTempOut-' + gateName.split('-')[-1] +'.txt', 'w') as TaOut:
					TaOut.write(dOutFix)
			except:
				client.send('ID anda tidak ditemukan')
				continue
		except:
			clients.pop(gateName)
			print (gateName + 'has been logged out')
			continue

while serverRunning:
	client, address = server.accept()
	gateName = client.recv(1024)
	print('%s connected to the server'%str(gateName))
	
	if(client not in clients):
		clients[gateName] = client
		noGate = int(gateName.split('-')[1])
		if noGate % 2 != 0:
			threading.Thread(target = handleMasuk, args = (client, gateName, )).start()
		elif noGate % 2 ==0:
			threading.Thread(target = handleKeluar, args = (client, gateName, )).start()
