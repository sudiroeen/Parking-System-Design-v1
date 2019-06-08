from PyQt5 import QtCore, QtGui, QtWidgets
from lib.xirkaReader import *
import datetime
import source.included
import source.updateGui
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

WRITE_TO_FILE_READER = '00D0000008'

class PintuKeluar:
	def setup(self, Dialog, kamera, gate, fileSimpan, ipServer, portServer, rIPServer, rportServer, rIP, rPort):
		self.reader = xirkaReader(rIP, rPort)
		self.reader.setServerIP(rIPServer, rportServer)

		self.gateName = gate
		self.klient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.klient.connect((ipServer, portServer))
		self.klient.send(gate)

		self.cam = cv2.VideoCapture(kamera)

		self.fileSimpan = fileSimpan

		self.gui = source.updateGui.GUIParkirLuar(Dialog, self.reader, self.fileSimpan)
		
	def kosong(self):
		self.gui.lNID.clear()
		self.gui.lNTimeOut.clear()
		self.gui.lNTimeIn.clear()
		self.gui.lNTimeTotal.clear()
		self.gui.lNBiaya.clear()
		self.gui.lNCheckIn.clear()
		self.gui.lNKembalian.clear()
		self.gui.lNSAwal.clear()
		self.gui.lNSAkhir.clear()
		self.gui.lNImgMasuk.clear()
		self.gui.lNImgKeluar.clear()

	def card_removed_handler(self):
		print 'card has been removed'
		self.reader.lcdSetText('Card has been', 'removed')
	

	def card_inserted_handler(self, data):
		print 'card has been inserted'
		self.reader.lcdSetText('Accepted', '')
		try:
			lFileID = self.reader.userSendAPDU(LOAD_FILE_ID)
			rFileID = self.reader.userSendAPDU(READ_FILE_ID)
			nim = rFileID[:-4]
			ID = nim.decode("hex")

			lFileSaldo = self.reader.userSendAPDU(LOAD_FILE_SALDO) #Untuk baca saldo
			rFileSaldo = self.reader.userSendAPDU(READ_FILE_SALDO)
			dSaldoAwal = rFileSaldo[:-4]
			SaldoAwal = int(dSaldoAwal,16)
		except:
			self.kosong()
			self.reader.lcdSetText('kartu anda', 'terbalik')
			self.gui.lNMsg.setText('[*] kartu anda terbalik')
			return

		timeOut = str(self.reader.rtcGetDatetime())
		
		#ID/Nomor_Tanggal_Jam_SaldoAwal_
		dataOut = str(ID) + "_" + timeOut.replace(' ', '_') + '_' +  str(SaldoAwal) + '_'
		self.writeFile(dataOut)

	def writeFile(self, dataOut):
		with open(self.fileSimpan, "w+") as writeToFile:
			writeToFile.write(dataOut)
		
	def writeSaldoAkhir(self, SA):
		if SA < 0:
			SA = 0
		else:
			hexsaldo = hex(SA).split('x')[-1]
			for i in range(16):
				if len(hexsaldo)<16:
					hexsaldo=str(0)+hexsaldo
				else:
					hexsaldo=hexsaldo
			hexsaldo = str(WRITE_TO_FILE_READER) + hexsaldo
			lFileSaldo = self.reader.userSendAPDU(LOAD_FILE_SALDO)
			wFileSaldo = self.reader.userSendAPDU(hexsaldo)


	def klientRunning(self):
		self.reader.eventUsercardInserted(self.card_inserted_handler)
		self.reader.eventUsercardRemoved(self.card_removed_handler)

		while True:
			ret, frame = self.cam.read()

			if not os.path.isfile(self.fileSimpan):
				self.gui.handleButtonRESET
				continue
			else:
				with open(self.fileSimpan, 'rb') as f: 
					#ID/Nomor_Tanggal_Jam_saldoAwal_
					dataOut = f.read()
				
					if len(dataOut.split('_')) == 5:
						#ID/Nomor_Tanggal_Jam_saldoAwal_ + Gate-2 + _Check-Out
						fullnameout = dataOut + self.gateName + '_Check-Out'
						
						ID = str(dataOut.split('_')[0])
						self.klient.send(ID)
						
						#ID_Tanggal_Jam_saldoAwal_Gate-1_Check-In_harga.jpg
						namaIn = self.klient.recv(1024)
						
						if namaIn.split('_')[0] != ID: #'ID anda tidak ditemukan'
							self.kosong()
							self.reader.lcdSetText(' '.join(namaIn.split(' ')[0:2]), ' '.join(namaIn.split(' ')[2:4]))
							self.gui.lNMsg.setText('[*] ' +  namaIn)
							os.remove(self.fileSimpan)
							continue
						else:
							harga = namaIn.split('.jpg')[0].split('_')[-1]

							#ID_Tanggal_Jam_saldoAwal_Gate-1_Check-In.jpg
							namaInCutHarga = namaIn.replace('_'+harga, '')
							
							imgIn = source.included.string2img(self.klient, 4096, cv2.IMREAD_COLOR)
							
							os.chdir('TempFoto/')
							
							cv2.imwrite(namaInCutHarga, imgIn)
							
							#ID/Nomor_Tanggal_Jam_saldoAwal_Gate-2_Check-Out
							
							cv2.imwrite(fullnameout +'.jpg', frame)
							
							if (os.path.isfile(namaInCutHarga) & os.path.isfile(fullnameout + '.jpg')):
								try:
									stringIO = source.included.compoundData(namaIn, fullnameout)

									stringKomplit = source.included.complithitung(stringIO)

									fullnameout += '_' + stringKomplit.split('_')[5]
									self.klient.send(fullnameout)

									stringSaldoAkhir = stringKomplit.split('_')[-2]

									if stringSaldoAkhir != 'manual':
										if int(float(stringSaldoAkhir)) < 0:
											self.reader.lcdSetText('Saldo tidak', 'Mencukupi')
										else:
											self.reader.lcdSetText('Saldo Anda: ',stringSaldoAkhir)
											self.writeSaldoAkhir(int(stringSaldoAkhir))
									self.gui.handleButtonRESET()
									self.gui.tampilanDynamic(stringKomplit) 
									self.gui.tampilanImageDynamic(imgIn, frame)

									shutil.move(namaInCutHarga, 'IN/')
									shutil.move(fullnameout + '.jpg', 'OUT/')
								except:
									os.remove('IN/' + namaInCutHarga)
									shutil.move(namaInCutHarga, 'IN/')
									shutil.move(fullnameout + '.jpg', 'OUT/')
							os.chdir('../')
							os.remove(self.fileSimpan)
					else:
						continue


if __name__ == '__main__':
	gateName = 'Gate-2'
	ipCamera = 0
	ipServer, portServer = '127.0.89.67', 1234
	rIP, rPort = '192.168.2.35', 1000
	rIPServer, rportServer = '192.168.2.5', 8010
	fileSimpan = 'TempText/keluar.txt'


	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	
	keluar = PintuKeluar()
	keluar.setup(Dialog, ipCamera, gateName, fileSimpan, ipServer, portServer, rIPServer, rportServer, rIP, rPort)

	keluar.reader.rtcSetDatetime(datetime.datetime.utcnow())

	threading.Thread(target= keluar.klientRunning).start()
	Dialog.show()
	app.exec_()
