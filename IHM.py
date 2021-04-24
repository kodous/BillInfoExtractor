import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from pdfextractor import *


def createComboBox(box):
    box.addItem('Numéro Facture')
    box.addItem('Nom du client')
    box.addItem('Libélé Désignation')
    box.addItem('Prix HT')
    box.addItem('TVA')
    box.addItem('Prix TTC')
    box.addItem('Date')


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.combo_7 = QtWidgets.QComboBox(self)
        self.combo_6 = QtWidgets.QComboBox(self)
        self.combo_5 = QtWidgets.QComboBox(self)
        self.combo_4 = QtWidgets.QComboBox(self)
        self.combo_3 = QtWidgets.QComboBox(self)
        self.combo_2 = QtWidgets.QComboBox()
        self.combo_1 = QtWidgets.QComboBox()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('Extraction Facture')
        self.hbox = QtWidgets.QHBoxLayout()
        self.home()

    def home(self):
        vbox = QtWidgets.QVBoxLayout()
        # vbox.addStretch(1)
        btn_import = QtWidgets.QPushButton('Import PDF')
        # btn_import.move(100, 100)
        btn_import.clicked.connect(self.openFiles)
        vbox.addWidget(btn_import)
        vbox.addLayout(self.hbox)
        self.setLayout(vbox)
        self.orderFields()
        self.show()

    def openFiles(self):
        names = QtWidgets.QFileDialog.getOpenFileNames(self, 'import file', 'PDF (*.pdf)')
        dicts = []
        items = [self.combo_1.currentText(), self.combo_2.currentText(), self.combo_3.currentText(),
                 self.combo_4.currentText(), self.combo_5.currentText(), self.combo_6.currentText(),
                 self.combo_7.currentText()]
        items_set = set(items)
        if len(items) != len(items_set):
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle('Error')
            label = QtWidgets.QLabel('Il y a un champ séléctionné deux fois dans les menus déroulants', dialog)
            dialog.exec_()
            return
        for name in names[0]:
            try:
                dicts.append(extractInfo(name))
            except Exception as e:
                dialog = QtWidgets.QDialog(self)
                dialog.setWindowTitle('Error')
                label = QtWidgets.QLabel('une erreur est survenue avec le fichier: ' + name, dialog)
                print(str(e))
                dialog.exec_()

        writeToCSV(dicts, items)
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Info')
        label = QtWidgets.QLabel('Done!', dialog)
        dialog.exec_()

    def orderFields(self):
        lbl_1 = QtWidgets.QLabel('1', self)
        createComboBox(self.combo_1)
        self.combo_1.setCurrentText('Numéro Facture')
        lbl_2 = QtWidgets.QLabel('2', self)
        createComboBox(self.combo_2)
        self.combo_2.setCurrentText('Nom du client')
        lbl_3 = QtWidgets.QLabel('3', self)
        createComboBox(self.combo_3)
        self.combo_3.setCurrentText('Libélé Désignation')
        lbl_4 = QtWidgets.QLabel('4', self)
        createComboBox(self.combo_4)
        self.combo_4.setCurrentText('Prix HT')
        lbl_5 = QtWidgets.QLabel('5', self)
        createComboBox(self.combo_5)
        self.combo_5.setCurrentText('TVA')
        lbl_6 = QtWidgets.QLabel('6', self)
        createComboBox(self.combo_6)
        self.combo_6.setCurrentText('Prix TTC')
        lbl_7 = QtWidgets.QLabel('7', self)
        createComboBox(self.combo_7)
        self.combo_7.setCurrentText('Date')

        self.hbox.addStretch(1)
        self.hbox.addWidget(lbl_1)
        self.hbox.addWidget(self.combo_1)
        self.hbox.addWidget(lbl_2)
        self.hbox.addWidget(self.combo_2)
        self.hbox.addWidget(lbl_3)
        self.hbox.addWidget(self.combo_3)
        self.hbox.addWidget(lbl_4)
        self.hbox.addWidget(self.combo_4)
        self.hbox.addWidget(lbl_5)
        self.hbox.addWidget(self.combo_5)
        self.hbox.addWidget(lbl_6)
        self.hbox.addWidget(self.combo_6)
        self.hbox.addWidget(lbl_7)
        self.hbox.addWidget(self.combo_7)


def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
