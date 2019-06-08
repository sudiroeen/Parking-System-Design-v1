from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json

class saveToJSON(object):
	def __init__(self, Dialog, fileJson):
		super(saveToJSON, self).__init__()
	  	Dialog.setObjectName("Dialog")
	  	Dialog.resize(620, 110)

	  	self.le_gate = QtWidgets.QLineEdit(Dialog)
	  	self.le_gate.setGeometry(QtCore.QRect(20, 40, 30, 25))
	  	self.le_gate.setObjectName("le_gate")

	  	self.le_IP = QtWidgets.QLineEdit(Dialog)
	  	self.le_IP.setGeometry(QtCore.QRect(55, 40, 260, 25))
	  	self.le_IP.setObjectName("le_IP")

	  	self.lWarning = QtWidgets.QLabel(Dialog)
	  	self.lWarning.setGeometry(QtCore.QRect(20, 60, 150, 25))
	  	self.lWarning.setObjectName("lWarning")
		
		self.lgate = QtWidgets.QLabel(Dialog)
	  	self.lgate.setGeometry(QtCore.QRect(20, 20, 30, 20))
	  	self.lgate.setObjectName("lgate")

	  	self.lIP = QtWidgets.QLabel(Dialog)
	  	self.lIP.setGeometry(QtCore.QRect(55, 20, 80, 20))
	  	self.lIP.setObjectName("lIP")

	  	self.pSave = QtWidgets.QPushButton(Dialog)
	  	self.pSave.setGeometry(QtCore.QRect(215, 80, 100, 25))
	  	self.pSave.setObjectName("pSave")
	  	self.pSave.clicked.connect(self.handleSave)

	  	self.pRemove = QtWidgets.QPushButton(Dialog)
	  	self.pRemove.setGeometry(QtCore.QRect(110, 80, 100, 25))
	  	self.pRemove.setObjectName("pRemove")
	  	self.pRemove.clicked.connect(self.handleRemove)

	  	self.listWidget = QtWidgets.QListWidget(Dialog)
	  	self.listWidget.setGeometry(QtCore.QRect(330, 10, 280, 100))
	  	self.listWidget.setObjectName("listWidget")
	  	self.listWidget.itemActivated.connect(self.selectedItem)

	  	self.inisial(Dialog)
	  	self.dataJson = {}
	  	QtCore.QMetaObject.connectSlotsByName(Dialog)

	  # self.lList = QtWidgets.QLabel(Dialog)
	  # self.lList.setGeometry(QtCore.QRect(330, 10, 260, 200))
	  # self.lList.setObjectName("lList")
	  # self.lList.setStyleSheet('background: white')

	  # self.verticalScrollBar = QtWidgets.QScrollBar(Dialog)
	  # self.verticalScrollBar.setGeometry(QtCore.QRect(595, 10, 20, 210))
	  # self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
	  # self.verticalScrollBar.setObjectName("verticalScrollBar")
	  # self.verticalScrollBar.sliderMoved.connect(self.lList)

	def inisial(self, Dialog):
		Dialog.setWindowTitle("List Camera")
		self.lgate.setText("No")
		self.lIP.setText("IP Camera")
		self.pSave.setText("Save")
		self.pRemove.setText("Remove")

		with open(fileJson) as lc:
			self.dataJson = json.load(lc)		

		kuncisIN = map(int, self.dataJson.keys())
		kuncisIN.sort()
		for key in kuncisIN:
			self.listWidget.addItem("[" + str(key) + "] " + str(self.dataJson[u"" + str(key)]))

	def handleSave(self):
		self.lWarning.clear()
		if self.le_IP.text() != '':
			with open(fileJson) as lc:
				self.dataJson = json.load(lc)

			self.prevDict = self.dataJson
			kuncisIN = map(int, self.dataJson.keys())
			indeks = self.le_gate.text()

			if indeks == '':
				if len(kuncisIN) !=0:
					indeks = max(kuncisIN)
					indeks += 2
				else:
					indeks = 1
				kuncisIN.append(indeks)
			else:
				indeks = int(indeks)
				if indeks not in self.dataJson.keys():
					kuncisIN.append(indeks)
				if indeks%2 == 0:
					self.lWarning.setText("<font color='red'>Check-In harus GANJIL</font>")
					return
			
			self.dataJson[u"" + str(indeks)] = self.le_IP.text()
			kuncisIN.sort()
			self.listWidget.clear()
			for key in kuncisIN:
				self.listWidget.addItem("[" + str(key) + "] " + str(self.dataJson[u"" + str(key)]))
			with open(fileJson, "w") as wj:
				try:
					json.dump(self.dataJson, wj)
				except:
					json.dump(self.prevDict, wj)
			
			self.le_IP.clear()
			self.le_gate.clear()
		else:
			pass

	def selectedItem(self):
		self.items =  self.listWidget.selectedItems()
		self.pRemove.clicked.connect(self.handleRemove)

	def handleRemove(self):
		dataItem = ''
		for i in range(len(self.items)):
			dataItem = dataItem + str(self.items[i].text())
		IndexToDelete = str(dataItem.split('[')[1].split(']')[0])

		with open(fileJson) as lc:
			self.dataJson = json.load(lc)

		self.prevDict = self.dataJson
		del self.dataJson[IndexToDelete]

		print self.dataJson
		with open(fileJson, "w") as wj:
			try:
				json.dump(self.dataJson, wj)
				self.listWidget.takeItem(self.listWidget.currentRow())
			except:
				json.dump(self.prevDict, wj)


			
if __name__ == "__main__":

	fileJson = "jsonCamera/listCamera.json"

	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()

	gui = saveToJSON(Dialog, fileJson)
	Dialog.show()
	app.exec_()


########### FIX TROUBLE SHOOTING QTreeWidget ####################
# from PyQt5 import QtCore, QtGui, QtWidgets
# import sys
# import json

# class saveToJSON(object):
# 	def __init__(self, Dialog, fileJson):
# 		super(saveToJSON, self).__init__()
# 	  	Dialog.setObjectName("Dialog")
# 	  	Dialog.resize(620, 110)

# 	  	self.le_gate = QtWidgets.QLineEdit(Dialog)
# 	  	self.le_gate.setGeometry(QtCore.QRect(20, 40, 30, 25))
# 	  	self.le_gate.setObjectName("le_gate")

# 	  	self.le_IP = QtWidgets.QLineEdit(Dialog)
# 	  	self.le_IP.setGeometry(QtCore.QRect(55, 40, 260, 25))
# 	  	self.le_IP.setObjectName("le_IP")

# 	  	self.lWarning = QtWidgets.QLabel(Dialog)
# 	  	self.lWarning.setGeometry(QtCore.QRect(20, 60, 150, 25))
# 	  	self.lWarning.setObjectName("lWarning")
		
# 		self.lgate = QtWidgets.QLabel(Dialog)
# 	  	self.lgate.setGeometry(QtCore.QRect(20, 20, 30, 20))
# 	  	self.lgate.setObjectName("lgate")

# 	  	self.lIP = QtWidgets.QLabel(Dialog)
# 	  	self.lIP.setGeometry(QtCore.QRect(55, 20, 80, 20))
# 	  	self.lIP.setObjectName("lIP")

# 	  	self.pSave = QtWidgets.QPushButton(Dialog)
# 	  	self.pSave.setGeometry(QtCore.QRect(215, 80, 100, 25))
# 	  	self.pSave.setObjectName("pSave")
# 	  	self.pSave.clicked.connect(self.handleSave)

# 	  	self.pRemove = QtWidgets.QPushButton(Dialog)
# 	  	self.pRemove.setGeometry(QtCore.QRect(110, 80, 100, 25))
# 	  	self.pRemove.setObjectName("pRemove")
# 	  	self.pRemove.clicked.connect(self.handleRemove)

# 	  	self.listWidget = QtWidgets.QTreeWidget(Dialog)
# 	  	self.listWidget.setGeometry(QtCore.QRect(330, 10, 280, 95))
# 	  	self.listWidget.setObjectName("listWidget")
# 	  	self.listWidget.header().hide()
# 	  	# self.listWidget.itemActivated.connect(self.selectedItem)

# 	  	self.inisial(Dialog)
# 	  	self.dataJson = {}
# 	  	QtCore.QMetaObject.connectSlotsByName(Dialog)

# 	  # self.lList = QtWidgets.QLabel(Dialog)
# 	  # self.lList.setGeometry(QtCore.QRect(330, 10, 260, 200))
# 	  # self.lList.setObjectName("lList")
# 	  # self.lList.setStyleSheet('background: white')

# 	  # self.verticalScrollBar = QtWidgets.QScrollBar(Dialog)
# 	  # self.verticalScrollBar.setGeometry(QtCore.QRect(595, 10, 20, 210))
# 	  # self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
# 	  # self.verticalScrollBar.setObjectName("verticalScrollBar")
# 	  # self.verticalScrollBar.sliderMoved.connect(self.lList)

# 	def inisial(self, Dialog):
# 		Dialog.setWindowTitle("List Camera")
# 		self.lgate.setText("No")
# 		self.lIP.setText("IP Camera")
# 		self.pSave.setText("Save")
# 		self.pRemove.setText("Remove")

# 		with open(fileJson) as lc:
# 			self.dataJson = json.load(lc)		

# 		kuncisIN = map(int, self.dataJson.keys())
# 		kuncisIN.sort()
# 		for key in kuncisIN:
# 			item  = QtWidgets.QTreeWidgetItem()
# 			item.setText(0, "[" + str(key) + "] " + str(self.dataJson[u"" + str(key)]))
# 			self.listWidget.addTopLevelItem(item)

# 	def handleSave(self):
# 		self.lWarning.clear()
# 		if self.le_IP.text() != '':
# 			with open(fileJson) as lc:
# 				self.dataJson = json.load(lc)

# 			self.prevDict = self.dataJson
# 			kuncisIN = map(int, self.dataJson.keys())
# 			indeks = self.le_gate.text()

# 			if indeks == '':
# 				if len(kuncisIN) !=0:
# 					indeks = max(kuncisIN)
# 					indeks += 2
# 				else:
# 					indeks = 1
# 				kuncisIN.append(indeks)
# 			else:
# 				indeks = int(indeks)
# 				if indeks not in self.dataJson.keys():
# 					kuncisIN.append(indeks)
# 				if indeks%2 == 0:
# 					self.lWarning.setText("<font color='red'>Check-In harus GANJIL</font>")
# 					return
			
# 			self.dataJson[u"" + str(indeks)] = self.le_IP.text()
# 			kuncisIN.sort()
# 			self.listWidget.clear()

# 			for key in kuncisIN:
# 				item = QtWidgets.QTreeWidgetItem()
# 				item.setText(0, "[" + str(key) + "] " + str(self.dataJson[u"" + str(key)]))
# 				self.listWidget.addTopLevelItem(item)
# 			with open(fileJson, "w") as wj:
# 				try:
# 					json.dump(self.dataJson, wj)
# 				except:
# 					json.dump(self.prevDict, wj)
			
# 			self.le_IP.clear()
# 			self.le_gate.clear()
# 		else:
# 			pass

# 	# def selectedItem(self):
# 	# 	self.items =  self.listWidget.selectedItems()
# 	# 	self.pRemove.clicked.connect(self.handleRemove)

# 	def handleRemove(self):
# 		select_item = self.listWidget.selectedItems()
		
# 		if not select_item:
# 			return

# 		item = select_item[0]
# 		itemIndex = self.listWidget.indexOfTopLevelItem(item)
# 		self.listWidget.takeTopLevelItem(itemIndex)
# 		# print select_item[0].text(0)
# 		# dataItem = ''
# 		# for item in select_item:
# 		# 	itemIndex = self.listWidget.indexOfTopLevelItem(item)
# 		# 	# print item.text(itemIndex)
# 		# 	dataItem += str(item.text(itemIndex))
# 		# 	self.listWidget.takeTopLevelItem(itemIndex)

# 		itemText = item.text(0)
# 		IndexToDeleteInJSON = str(itemText.split('[')[1].split(']')[0])

# 		with open(fileJson) as lc:
# 			self.dataJson = json.load(lc)

# 		self.prevDict = self.dataJson
# 		del self.dataJson[IndexToDeleteInJSON]

# 		with open(fileJson, "w") as wj:
# 			try:
# 				json.dump(self.dataJson, wj)
# 			except:
# 				json.dump(self.prevDict, wj)


			
# if __name__ == "__main__":

# 	fileJson = "jsonCamera/listCamera.json"

# 	app = QtWidgets.QApplication(sys.argv)
# 	Dialog = QtWidgets.QDialog()

# 	gui = saveToJSON(Dialog, fileJson)
# 	Dialog.show()
# 	app.exec_()
