# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt5_DesignFile.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 460)
        MainWindow.setMinimumSize(QtCore.QSize(460, 460))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(450, 430))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 90))
        self.groupBox.setMaximumSize(QtCore.QSize(440, 90))
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.ip_1 = QtWidgets.QSpinBox(self.groupBox)
        self.ip_1.setMaximum(255)
        self.ip_1.setProperty("value", 192)
        self.ip_1.setObjectName("ip_1")
        self.gridLayout_3.addWidget(self.ip_1, 0, 1, 1, 2)
        self.ip_2 = QtWidgets.QSpinBox(self.groupBox)
        self.ip_2.setMaximum(255)
        self.ip_2.setProperty("value", 168)
        self.ip_2.setObjectName("ip_2")
        self.gridLayout_3.addWidget(self.ip_2, 0, 3, 1, 1)
        self.ip_3 = QtWidgets.QSpinBox(self.groupBox)
        self.ip_3.setMaximum(255)
        self.ip_3.setProperty("value", 1)
        self.ip_3.setObjectName("ip_3")
        self.gridLayout_3.addWidget(self.ip_3, 0, 4, 1, 1)
        self.ip_4 = QtWidgets.QSpinBox(self.groupBox)
        self.ip_4.setMaximum(255)
        self.ip_4.setProperty("value", 1)
        self.ip_4.setObjectName("ip_4")
        self.gridLayout_3.addWidget(self.ip_4, 0, 5, 1, 1)
        self.lbl_slot = QtWidgets.QLabel(self.groupBox)
        self.lbl_slot.setObjectName("lbl_slot")
        self.gridLayout_3.addWidget(self.lbl_slot, 0, 6, 1, 1)
        self.ip_slot = QtWidgets.QSpinBox(self.groupBox)
        self.ip_slot.setObjectName("ip_slot")
        self.gridLayout_3.addWidget(self.ip_slot, 0, 7, 1, 1)
        self.btn_connect = QtWidgets.QPushButton(self.groupBox)
        self.btn_connect.setDefault(False)
        self.btn_connect.setObjectName("btn_connect")
        self.gridLayout_3.addWidget(self.btn_connect, 0, 8, 1, 1)
        self.btn_disconnect = QtWidgets.QPushButton(self.groupBox)
        self.btn_disconnect.setEnabled(False)
        self.btn_disconnect.setDefault(False)
        self.btn_disconnect.setObjectName("btn_disconnect")
        self.gridLayout_3.addWidget(self.btn_disconnect, 1, 8, 1, 1)
        self.lbl_status = QtWidgets.QLabel(self.groupBox)
        self.lbl_status.setObjectName("lbl_status")
        self.gridLayout_3.addWidget(self.lbl_status, 1, 0, 1, 1)
        self.status_disp = QtWidgets.QLineEdit(self.groupBox)
        self.status_disp.setEnabled(False)
        self.status_disp.setReadOnly(True)
        self.status_disp.setPlaceholderText("")
        self.status_disp.setObjectName("status_disp")
        self.gridLayout_3.addWidget(self.status_disp, 1, 1, 1, 7)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.group_components = QtWidgets.QGroupBox(self.centralwidget)
        self.group_components.setEnabled(False)
        self.group_components.setObjectName("group_components")
        self.gridLayout = QtWidgets.QGridLayout(self.group_components)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(self.group_components)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 2, 1, 1)
        self.btn_loadPrograms = QtWidgets.QPushButton(self.group_components)
        self.btn_loadPrograms.setObjectName("btn_loadPrograms")
        self.gridLayout.addWidget(self.btn_loadPrograms, 0, 2, 1, 1)
        self.lst_components = QtWidgets.QListWidget(self.group_components)
        self.lst_components.setWordWrap(True)
        self.lst_components.setObjectName("lst_components")
        self.gridLayout.addWidget(self.lst_components, 0, 1, 5, 1)
        self.btn_export = QtWidgets.QPushButton(self.group_components)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_export.sizePolicy().hasHeightForWidth())
        self.btn_export.setSizePolicy(sizePolicy)
        self.btn_export.setObjectName("btn_export")
        self.gridLayout.addWidget(self.btn_export, 2, 2, 1, 1)
        self.btn_import = QtWidgets.QPushButton(self.group_components)
        self.btn_import.setObjectName("btn_import")
        self.gridLayout.addWidget(self.btn_import, 3, 2, 1, 1)
        self.gridLayout_2.addWidget(self.group_components, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 460, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setToolTip("")
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionFile = QtWidgets.QAction(MainWindow)
        self.actionFile.setObjectName("actionFile")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionClose)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "PLC"))
        self.label_3.setText(_translate("MainWindow", "IP:"))
        self.lbl_slot.setText(_translate("MainWindow", "Slot:"))
        self.btn_connect.setText(_translate("MainWindow", "Connect"))
        self.btn_disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.lbl_status.setText(_translate("MainWindow", "Status:"))
        self.group_components.setTitle(_translate("MainWindow", "Components"))
        self.btn_loadPrograms.setText(_translate("MainWindow", "Reload"))
        self.btn_export.setText(_translate("MainWindow", "Export Tags..."))
        self.btn_import.setText(_translate("MainWindow", "Import Tags..."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFile.setText(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New..."))
        self.actionNew.setToolTip(_translate("MainWindow", "Create a new file"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionClose.setText(_translate("MainWindow", "Exit"))
