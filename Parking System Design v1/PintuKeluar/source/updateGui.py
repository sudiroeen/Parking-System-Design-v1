from PyQt5 import QtCore, QtGui, QtWidgets
from xirkaReader import *
import included
import time

class GUIParkirLuar(object):
    #statePlate = False
    def __init__(self, Dialog, reader, fileSimpan):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setObjectName("Dialog")
        Dialog.resize(820, 620)
        Dialog.setWindowTitle(_translate("Dialog", 'GATE-2 [Check-Out]'))
        
        self.TextMsg = ''
        self.SAkhir = 0
        self.simpanSaldo = 0
        self.reader = reader
        self.fileSimpan = fileSimpan
        self.LED_GREEN  = 0x02
        self.LED_RED    = 0x01
        self.LED_OFF    = 0x00
        self.harga = ''

        ##################### PushButton #########################
        #
        self.pCheck = QtWidgets.QPushButton(Dialog)
        self.pCheck.setGeometry(QtCore.QRect(230,200, 50, 25))
        self.pCheck.setObjectName('pCheck')
        self.pCheck.clicked.connect(self.handleCheck)

        self.pReset = QtWidgets.QPushButton(Dialog)
        self.pReset.setGeometry(QtCore.QRect(140, 900, 110, 60))
        self.pReset.setObjectName("pReset")
        self.pReset.clicked.connect(self.handleButtonRESET)

        self.pPreviouse = QtWidgets.QPushButton(Dialog)
        self.pPreviouse.setGeometry(QtCore.QRect(20, 900, 110, 60))
        self.pPreviouse.setObjectName("pPreviouse")
        self.pPreviouse.clicked.connect(self.handleButtonPreviouse)

        self.pBuka = QtWidgets.QPushButton(Dialog)
        self.pBuka.setGeometry(QtCore.QRect(140, 810, 110, 60))
        self.pBuka.setObjectName("pBuka")
        self.pBuka.clicked.connect(self.handleBuka)

        self.pSilang = QtWidgets.QPushButton(Dialog)
        self.pSilang.setGeometry(QtCore.QRect(20, 810, 110, 60))
        self.pSilang.setObjectName("pSilang")
        self.pSilang.clicked.connect(self.plateTidakSesuai)

        self.pApply = QtWidgets.QPushButton(Dialog)
        self.pApply.setGeometry(QtCore.QRect(210,310,100,25))
        self.pApply.setObjectName("pApply")
        self.pApply.clicked.connect(self.handleApply)

        self.pPrint = QtWidgets.QPushButton(Dialog)
        self.pPrint.setGeometry(QtCore.QRect(200,720,100,25))
        self.pPrint.setObjectName("pPrint")
        self.pPrint.clicked.connect(self.handlePrint)        
        ##################### lJudul #########################
        #
        self.fJudul = QtWidgets.QLabel(Dialog)
        self.fJudul.setGeometry(QtCore.QRect(595, 8, 125, 35))

        self.lJudul = QtWidgets.QLabel(Dialog)
        self.lJudul.setGeometry(QtCore.QRect(600, 10, 115, 30))
        self.lJudul.setObjectName("lJudul")
        ##################### Image In #########################
        #
        self.limgMasuk = QtWidgets.QLabel(Dialog)
        self.limgMasuk.setGeometry(QtCore.QRect(340, 45, 70, 30))
        self.limgMasuk.setObjectName("limgMasuk")

        self.lNImgMasuk = QtWidgets.QLabel(Dialog)
        self.lNImgMasuk.setGeometry(QtCore.QRect(340, 75, 630, 430))
        self.lNImgMasuk.setObjectName("lNImgMasuk")
        ##################### Image Out #########################
        #    
        self.limgKeluar = QtWidgets.QLabel(Dialog)
        self.limgKeluar.setGeometry(QtCore.QRect(340, 520, 70, 30))
        self.limgKeluar.setObjectName("limgKeluar")

        self.lNImgKeluar = QtWidgets.QLabel(Dialog)
        self.lNImgKeluar.setGeometry(QtCore.QRect(340, 550, 630, 430))
        self.lNImgKeluar.setObjectName("lNImgKeluar")
        ##################### Message #########################
        #
        self.lMessage = QtWidgets.QLabel(Dialog)
        self.lMessage.setGeometry(QtCore.QRect(20, 10, 55, 30))
        self.lMessage.setObjectName("lMessage")

        self.lNMsg = QtWidgets.QLabel(Dialog)#, alignment= QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lNMsg.setGeometry(QtCore.QRect(20, 41, 270, 110))
        self.lNMsg.setObjectName("lNMsg")
        ##################### Pembayaran Manual ####################
        #
        self.pManual = QtWidgets.QLabel(Dialog)
        self.pManual.setGeometry(QtCore.QRect(80, 165, 130, 30))
        self.pManual.setObjectName("pManual")
        ##################### Nomor #########################
        #
        self.lNomor = QtWidgets.QLabel(Dialog)
        self.lNomor.setGeometry(QtCore.QRect(20, 200, 80, 20))
        self.lNomor.setObjectName("lNomor")

        self.lTitikNomor = QtWidgets.QLabel(Dialog)
        self.lTitikNomor.setGeometry(QtCore.QRect(102, 200, 3, 20))
        self.lTitikNomor.setObjectName("lTitikNomor")

        # EditeLine
        self.elNomor = QtWidgets.QLineEdit(Dialog)
        self.elNomor.setGeometry(QtCore.QRect(106, 200, 90, 25))
        self.elNomor.setObjectName("elNomor")
        ##################### Uang #########################
        #
        self.lUang = QtWidgets.QLabel(Dialog)
        self.lUang.setGeometry(QtCore.QRect(20, 230, 80, 20))
        self.lUang.setObjectName("lUang")

        self.lTitikUang = QtWidgets.QLabel(Dialog)
        self.lTitikUang.setGeometry(QtCore.QRect(102, 230, 3, 20))
        self.lTitikUang.setObjectName("lTitikUang")

        # EditeLine
        self.elUang = QtWidgets.QLineEdit(Dialog)
        self.elUang.setGeometry(QtCore.QRect(106, 230, 90, 25))
        self.elUang.setObjectName("elUang")
        ##################### Kembalian #######################
        #
        self.lKembalian = QtWidgets.QLabel(Dialog)
        self.lKembalian.setGeometry(QtCore.QRect(20, 260, 80, 20))
        self.lKembalian.setObjectName("lKembalian")

        self.lTitikKembalian = QtWidgets.QLabel(Dialog)
        self.lTitikKembalian.setGeometry(QtCore.QRect(102, 260, 3, 20))
        self.lTitikKembalian.setObjectName("lTitikKembalian")

        self.lNKembalian = QtWidgets.QLabel(Dialog)
        self.lNKembalian.setGeometry(QtCore.QRect(106, 260, 90, 20))
        self.lNKembalian.setObjectName("lNKembalian")

        #CheckBox
        self.cbSave = QtWidgets.QCheckBox(Dialog)
        self.cbSave.setGeometry(QtCore.QRect(100,290,100,20))
        self.cbSave.setObjectName("cbSave")
        ##################### ID #######################
        #
        self.lID = QtWidgets.QLabel(Dialog)
        self.lID.setGeometry(QtCore.QRect(20, 350, 70, 20))
        self.lID.setObjectName("lID")

        self.lNID = QtWidgets.QLabel(Dialog)
        self.lNID.setGeometry(QtCore.QRect(20, 370, 170, 25))
        self.lNID.setObjectName("lNID")
        ##################### Check-In #######################
        #
        self.lCheckIn = QtWidgets.QLabel(Dialog)
        self.lCheckIn.setGeometry(QtCore.QRect(20, 400, 100, 20))
        self.lCheckIn.setObjectName("lID")

        self.lNCheckIn = QtWidgets.QLabel(Dialog)
        self.lNCheckIn.setGeometry(QtCore.QRect(20, 420, 170, 25))
        self.lNCheckIn.setObjectName("lNID")
        ##################### Time Out #######################
        #
        self.lTimeOut = QtWidgets.QLabel(Dialog)
        self.lTimeOut.setGeometry(QtCore.QRect(20, 450, 70, 20))
        self.lTimeOut.setObjectName("ltout")

        self.lNTimeOut = QtWidgets.QLabel(Dialog)
        self.lNTimeOut.setGeometry(QtCore.QRect(20, 470, 170, 25))
        self.lNTimeOut.setObjectName("lNTimeOut")
        ##################### Time In #######################
        #
        self.lTimeIn = QtWidgets.QLabel(Dialog)
        self.lTimeIn.setGeometry(QtCore.QRect(20, 500, 70, 20))
        self.lTimeIn.setObjectName("lTimeIn")

        self.lNTimeIn = QtWidgets.QLabel(Dialog)
        self.lNTimeIn.setGeometry(QtCore.QRect(20, 520, 170, 25))
        self.lNTimeIn.setObjectName("lNTimeIn")
        ##################### Time Total #######################
        #
        self.lTimeTotal = QtWidgets.QLabel(Dialog)
        self.lTimeTotal.setGeometry(QtCore.QRect(20, 550, 70, 20))
        self.lTimeTotal.setObjectName("lTimeTotal")

        self.lNTimeTotal = QtWidgets.QLabel(Dialog)
        self.lNTimeTotal.setGeometry(QtCore.QRect(20, 570, 170, 25))
        self.lNTimeTotal.setObjectName("lNTimeTotal")
        ##################### Biaya #######################
        #
        self.lBiaya = QtWidgets.QLabel(Dialog)
        self.lBiaya.setGeometry(QtCore.QRect(20, 600, 70, 20))
        self.lBiaya.setObjectName("lBiaya")

        self.lNBiaya = QtWidgets.QLabel(Dialog)
        self.lNBiaya.setGeometry(QtCore.QRect(20, 620, 170, 25))
        self.lNBiaya.setObjectName("lNBiaya")

        self.lPerJam = QtWidgets.QLabel(Dialog)
        self.lPerJam.setGeometry(QtCore.QRect(200, 625, 80, 20))
        self.lPerJam.setObjectName("lPerJam")
        ##################### Saldo Awal #######################
        #
        self.lSAwal = QtWidgets.QLabel(Dialog)
        self.lSAwal.setGeometry(QtCore.QRect(20, 650, 70, 20))
        self.lSAwal.setObjectName("lSAwal")

        self.lNSAwal = QtWidgets.QLabel(Dialog)
        self.lNSAwal.setGeometry(QtCore.QRect(20, 670, 170, 25))
        self.lNSAwal.setObjectName("lNSAwal")
        ##################### Saldo Akhir #######################
        #
        self.lSAkhir = QtWidgets.QLabel(Dialog)
        self.lSAkhir.setGeometry(QtCore.QRect(20, 700, 70, 20))
        self.lSAkhir.setObjectName("lSAkhir")

        self.lNSAkhir = QtWidgets.QLabel(Dialog)
        self.lNSAkhir.setGeometry(QtCore.QRect(20, 720, 170, 25))
        self.lNSAkhir.setObjectName("lNSAkhir")


        self.setBackGround()
        self.tampilanStatic()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def tampilanStatic(self):
        _translate = QtCore.QCoreApplication.translate
        
        self.lJudul.setText(_translate("Dialog", "GATE-2 [Check Out]"))
        self.pReset.setText(_translate("Dialog", "Reset"))
        self.pManual.setText(_translate("Dialog", "[Pembayaran Manual]"))

        self.pBuka.setIcon(QtGui.QIcon(QtGui.QPixmap("iconGUI/check-mark.jpg")))
        self.pBuka.setIconSize(QtCore.QSize(self.pBuka.width()-1,self.pBuka.height()-4))

        self.pSilang.setIcon(QtGui.QIcon(QtGui.QPixmap("iconGUI/tanda-silang.jpg")))
        self.pSilang.setIconSize(QtCore.QSize(self.pSilang.width()-1,self.pSilang.height()-4))

        self.pPreviouse.setIcon(QtGui.QIcon(QtGui.QPixmap("iconGUI/leftArrow.png")))
        self.pPreviouse.setIconSize(QtCore.QSize(self.pPreviouse.width()-1,self.pPreviouse.height()-4))        

        self.cbSave.setText(_translate("Dialog", "save as saldo"))

        self.limgMasuk.setText(_translate("Dialog", "Saat Masuk"))
        self.limgKeluar.setText(_translate("Dialog", "Saat Keluar"))
        self.lID.setText(_translate("Dialog", "ID/Nomor"))
        self.lCheckIn.setText(_translate("Dialog", "Gate Check-In"))
        self.lTimeOut.setText(_translate("Dialog", "Time Out"))
        self.lBiaya.setText(_translate("Dialog", "Biaya"))
        self.lTimeIn.setText(_translate("Dialog", "Time In"))
        self.lMessage.setText(_translate("Dialog", "Message:"))
        self.lTimeTotal.setText(_translate("Dialog","Time total"))
        self.lNomor.setText(_translate("Dialog", "Nomor"))
        self.lUang.setText(_translate("Dialog", "Uang"))
        self.lTitikUang.setText(_translate("Dialog", ":"))
        self.lTitikKembalian.setText(_translate("Dialog", ":"))
        self.lTitikNomor.setText(_translate("Dialog", ":"))
        self.lKembalian.setText(_translate("Dialog", "Kembalian"))
        self.pApply.setText(_translate("Dialog", "Apply"))
        self.pPrint.setText(_translate("Dialog", "Print"))
        self.pCheck.setText(_translate("Dialog", "Check"))
        self.lSAwal.setText(_translate("Dialog", "Saldo Awal"))
        self.lSAkhir.setText(_translate("Dialog", "Saldo Akhir"))


    def tampilanDynamic(self, arrayData):
        _translate = QtCore.QCoreApplication.translate

        #ID, GateCheckIn, TImeOut, TimeIn, TimeTotal, Biaya, SaldoAwal, SaldoAkhir, harga
        ID, GateCheckIn, TimeOut, TimeIn, TimeTotal, self.Biaya, SaldoAwal, self.SaldoAkhir, self.harga = arrayData.split('_')

        self.lPerJam.setText(_translate("Dialog", "Rp." + self.harga + "/jam"))
        self.lNMsg.setText(_translate("Dialog", ""))
        self.lNID.setText(_translate("Dialog", ID))
        self.lNTimeOut.setText(_translate("Dialog", included.tampilCantik(TimeOut)))
        self.lNTimeIn.setText(_translate("Dialog", included.tampilCantik(TimeIn)))
        self.lNTimeTotal.setText(_translate("Dialog", str(TimeTotal)))
        self.lNBiaya.setText(_translate("Dialog", str(self.Biaya)))
        self.lNCheckIn.setText(_translate("Dialog", GateCheckIn))
        self.lNKembalian.setText(_translate("Dialog", ''))
        self.lNSAwal.setText(_translate("Dialog", SaldoAwal))
        self.lNSAkhir.setText(_translate("Dialog", str(self.SaldoAkhir)))
        
        if self.SaldoAkhir != 'manual':
            if float(self.SaldoAkhir) < 0.0:
                self.TextMsg += '[*] Saldo tidak cukup'
                self.lNMsg.setText(self.TextMsg)
        
    def tampilanImageDynamic(self, imgIn, imgOut):# Dialog, imgIn, imgOut):
        hin, win, cin = imgIn.shape
        inBytesPerLine = cin*win
        qImgIn = QtGui.QImage(imgIn.data, win, hin, inBytesPerLine, QtGui.QImage.Format_RGB888)
        InCvtToPixmap = QtGui.QPixmap.fromImage(qImgIn)

        hout, wout, cout = imgOut.shape
        outBytesPerLine = cout*wout
        qImgOut = QtGui.QImage(imgOut.data, wout, hout, outBytesPerLine, QtGui.QImage.Format_RGB888)
        OutCvtToPixmap = QtGui.QPixmap.fromImage(qImgOut)
        self.lNImgMasuk.setPixmap(InCvtToPixmap)
        self.lNImgKeluar.setPixmap(OutCvtToPixmap)

    # warna background
    def setBackGround(self):#, Dialog):
        self.fJudul.setStyleSheet('background-color: rgb(0,255,0)')
        self.lNImgMasuk.setStyleSheet('background: white')
        self.lNImgKeluar.setStyleSheet('background: white')
        self.lNMsg.setStyleSheet('background: white')
        self.lNID.setStyleSheet('background: #D9C560')
        self.lNCheckIn.setStyleSheet('background: #D9C560')
        self.lNTimeOut.setStyleSheet('background: #D9C560')
        self.lNTimeIn.setStyleSheet('background: #D9C560')
        self.lNTimeTotal.setStyleSheet('background: #D9C560')
        self.lNBiaya.setStyleSheet('background: #D9C560')
        self.lNKembalian.setStyleSheet('background: white')

        self.pReset.setStyleSheet('background: white')
        self.pBuka.setStyleSheet('background: white')
        self.pSilang.setStyleSheet('background: white')
        self.pPreviouse.setStyleSheet('background: white')

        self.lNSAwal.setStyleSheet('background: #D9C560')
        self.lNSAkhir.setStyleSheet('background: #D9C560')

    def handleButtonRESET(self):
        self.lNMsg.clear()
        self.lNID.clear()
        self.lNTimeOut.clear()
        self.lNTimeIn.clear()
        self.lNTimeTotal.clear()
        self.lNBiaya.clear()
        self.lNCheckIn.clear()
        self.lNKembalian.clear()
        self.lNSAwal.clear()
        self.lNSAkhir.clear()
        self.lNImgMasuk.clear()
        self.lNImgKeluar.clear()
        self.TextMsg = ''
        self.elUang.clear()
        self.elNomor.clear()
        self.cbSave.setChecked(False)
        self.cbSave.setEnabled(True)
        self.stateMotor = False
        self.reader.setLed(self.LED_OFF)
        self.lPerJam.setText("Rp." + self.harga + "/jam")
        

    def handleApply(self):
        try:
            uang = int(self.elUang.text())
            if self.SaldoAkhir != 'manual':
                self.SAkhir = int(self.SaldoAkhir) + uang
                if self.SAkhir < uang:
                    self.susuk = self.SAkhir
                else:
                    self.susuk = 0
                self.lNSAkhir.setText(str(self.SAkhir))
                if self.cbSave.isChecked():
                    if self.SAkhir >= 0:
                        self.simpanSaldo = self.SAkhir
                        self.saveAsSaldo(self.simpanSaldo)
                    else:
                        self.lNMsg.setText('saldo tidak boleh negatif')
            else:
                self.susuk = uang - int(self.Biaya)
                self.reader.lcdSetText('Kembalian:', str(self.susuk))

            self.lNKembalian.setText(str(self.susuk))
            self.lNMsg.setText('')
            
        except:
            self.lNMsg.setText('kolom Uang harus diisi')


    def plateTidakSesuai(self):
        self.TextMsg += '\n[*] Plat TIDAK SESUAI'
        self.lNMsg.setText(self.TextMsg)
        self.TextMsg = self.TextMsg.split('\n')[0]
        self.reader.setLed(self.LED_RED)
        self.reader.lcdSetText('Plate anda', 'Tidak sesuai')
        

    def handleBuka(self):
        self.lNMsg.setText('[*] Success')
        self.reader.lcdSetText('Success', '')
        self.reader.setLed(self.LED_GREEN)
        time.sleep(3)
        self.reader.setLed(self.LED_OFF)

    def handleButtonPreviouse(self):
        pass

    def handlePrint(self):
        pass

    def handleCheck(self):
        self.cbSave.setEnabled(False)
        Nomor = self.elNomor.text()

        try:
            if Nomor == '':
                self.lNMsg.setText('[*] kolom Nomor harus diisi')
            else:
                tanggalJam = str(self.reader.rtcGetDatetime())
                detik = str(time.time())
                #ID/Nomor_Tanggal_Jam_jumlahdetik_saldoAwal_
                timeOut = str(time.time())
                dataOut = Nomor + '_' + tanggalJam.replace(' ', '_') + '_' + timeOut + '_manual_'
                self.writeFile(dataOut)
        except:
            self.lNMsg.setText('[*] ID Tidak ditemukan')

    def writeFile(self, dataOut):
        parkdata = open(self.fileSimpan, "w+")
        parkdata.write(dataOut)
        parkdata.close()

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
            hexsaldo = str('00D0000008') + hexsaldo
            lFileSaldo = self.reader.userSendAPDU('00A40000023001')
            wFileSaldo = self.reader.userSendAPDU(hexsaldo)

    def saveAsSaldo(self, akhirsaldo):
        self.writeSaldoAkhir(akhirsaldo)
        print 'value has been saved as saldo'