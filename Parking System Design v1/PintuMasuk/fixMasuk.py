from source.xirkaReader import *
from source.included import *
import socket
import threading
import cv2
import os
import pickle
import struct
import shutil
import json
import sys


LOAD_FILE_ID = '00A40000023004'
LOAD_FILE_SALDO = '00A40000023001'

READ_FILE_ID = '00B0000008'
READ_FILE_SALDO = '00B0000008'


class PintuMasuk:
	def setup(self, kamera, gateName, fileSimpan, ipServer, portServer, rIPServer, rportServer, rIP, rPort):
		self.reader = xirkaReader(rIP, rPort)
		self.reader.setServerIP(rIPServer, rportServer)

		self.klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.klient.connect((ipServer, portServer))
		self.klient.send(gate)

		self.cam = cv2.VideoCapture(kamera)

		self.fileSimpan = fileSimpan

		self.gateName = gateName
		self.nGate = str(int(self.gate.split('-')[-1]))

		self.counter = 0
		setOfFiles = os.listdir('TempFoto/')
		print [j.split('_')[3] for j in setOfFiles if j.split('_')[0].split('A')[0] is self.nGate]
		try:
			if self.gate not in [j.split('_')[3] for j in setOfFiles if j.split('_')[0].split('A')[0] is self.nGate]:
				self.counter = 0
			if len(setOfFiles) != 0:
				self.counter = max([int(i.split('_')[0].split((self.nGate + 'A'))[1]) for i in setOfFiles if len(i.split('_')[0].split((self.nGate + 'A'))) == 2 ])
		except:
			self.counter = 0		


	def klientRunning(self):
		self.reader.eventUsercardRemoved(self.card_removed_handler)
		self.reader.eventUsercardInserted(self.card_inserted_handler)
		self.reader.eventKeypadNewInput(self.keypad_input_handler)

		while True:
			ret, frame = self.cam.read()
			if not os.path.isfile(self.fileSimpan):
				continue
			else:
				#ID/Nomor_Tanggal_Jam_saldoAwal/manual_
				with open(self.fileSimpan, 'rb').read() as msg:
					#ID_Tanggal_Jam_saldoAwal_Gate-1_Check-In
					msg = msg + self.gateName + '_Check-In'

					#ID/Nomor_Tanggal_Jam_saldoAwal/manual_Gate-1_Check-In
					self.klient.send(msg)

					#ID/Nomor_Tanggal_Jam_saldoAwal/manual_Gate-1_Check-In
					namaGambar = msg.replace(msg.split('_')[3] + '_', '')
					cv2.imwrite('TempFoto/' + namaGambar +'.jpg', frame)

				encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
				msgImg = img2string(frame, encode_param)
				self.klient.sendall(msgImg)
				os.remove(self.fileSimpan)

	def card_removed_handler(self):
		self.reader.lcdSetText('Card has been', 'removed')
		print 'card has been removed'

	def card_inserted_handler(self, data):
		print 'card has been inserted'
		try:
			lFileID = self.reader.userSendAPDU(LOAD_FILE_ID)
			rFileID = self.reader.userSendAPDU(READ_FILE_ID)
			nim = rFileID[:-4]
			ID = nim.decode("hex")
			print 'ID:', ID

			#'00D0000008' + 8 bit saldo

			lFileSaldo = self.reader.userSendAPDU(LOAD_FILE_SALDO) #Untuk baca saldo
			rFileSaldo = self.reader.userSendAPDU(READ_FILE_SALDO)
			dSaldoAwal = rFileSaldo[:-4]
			SaldoAwal = int(dSaldoAwal,16)
			
			if (ID == '') or (dSaldoAwal == ''):
				self.reader.lcdSetText("unreadable card")
				return
			self.reader.lcdSetText('Accepted', '')
			timeIn = str(self.reader.rtcGetDatetime())
			self.reader.lcdSetText(ID, timeIn)
			time.sleep(1)
			self.reader.lcdSetText('Remove Card','')
			
			#ID_Tanggal_Jam_SaldoAwal_
			dataIn = ID + "_" + timeIn.replace(' ', '_') + '_' +  str(SaldoAwal) + '_'

			with open(self.fileSimpan, 'w+') as simpanToFile:
				simpanToFile.write(dataIn)

		except:
			print '[*] Kartu Anda terbalik'
			self.reader.lcdSetText('Kartu Anda', 'terbalik')

	def keypad_input_handler(self, data):
		self.counter += 1
		print 'Keypad input:', self.counter 
		self.reader.lcdSetText('Accepted', '')

		timeIn = str(self.reader.rtcGetDatetime())
		self.reader.lcdSetText(str(self.counter),timeIn)

		#Nomor_Tanggal_Jam_saldoAwal(manual)_
		dataIn = str(self.nGate + 'A' + str(self.counter)) + "_" + timeIn.replace(' ', '_') + '_manual_'

		with open(self.fileSimpan, 'w+') as simpanToFile:
			simpanToFile.write(dataIn)


gateName = 'Gate-1'
ipCamera =  0
ipServer, portServer = '127.0.89.67', 1234 
rIP, rPort = '192.168.2.35', 1000 
rIPServer, rportServer = '192.168.2.5', 8010
fileSimpan = 'TempText/masuk.txt'

masuk = PintuMasuk()
masuk.setup(ipCamera, gateName, fileSimpan, ipServer, portServer, rIPServer, rportServer, rIP, rPort)
masuk.klientRunning()