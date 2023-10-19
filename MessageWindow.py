# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt5_DesignFile_MessageView.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditTable(object):
    def setupUi(self, EditTable):
        EditTable.setObjectName("EditTable")
        EditTable.resize(884, 660)
        self.tab_faults = QtWidgets.QWidget()
        self.tab_faults.setObjectName("tab_faults")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_faults)
        self.gridLayout.setObjectName("gridLayout")
        self.tbl_faults = QtWidgets.QTableWidget(self.tab_faults)
        self.tbl_faults.setTabKeyNavigation(False)
        self.tbl_faults.setAlternatingRowColors(True)
        self.tbl_faults.setGridStyle(QtCore.Qt.SolidLine)
        self.tbl_faults.setWordWrap(False)
        self.tbl_faults.setObjectName("tbl_faults")
        self.tbl_faults.setColumnCount(2)
        self.tbl_faults.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_faults.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_faults.setHorizontalHeaderItem(1, item)
        self.tbl_faults.horizontalHeader().setDefaultSectionSize(120)
        self.tbl_faults.horizontalHeader().setMinimumSectionSize(50)
        self.tbl_faults.horizontalHeader().setStretchLastSection(True)
        self.tbl_faults.verticalHeader().setSortIndicatorShown(False)
        self.gridLayout.addWidget(self.tbl_faults, 1, 0, 1, 1)
        self.groupbox_Fault = QtWidgets.QGroupBox(self.tab_faults)
        self.groupbox_Fault.setTitle("")
        self.groupbox_Fault.setObjectName("groupbox_Fault")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupbox_Fault)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status_fault = QtWidgets.QLineEdit(self.groupbox_Fault)
        self.status_fault.setEnabled(False)
        self.status_fault.setObjectName("status_fault")
        self.horizontalLayout.addWidget(self.status_fault)
        self.line_2 = QtWidgets.QFrame(self.groupbox_Fault)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.chkbx_faultEdit = QtWidgets.QCheckBox(self.groupbox_Fault)
        self.chkbx_faultEdit.setToolTipDuration(-1)
        self.chkbx_faultEdit.setObjectName("chkbx_faultEdit")
        self.horizontalLayout.addWidget(self.chkbx_faultEdit)
        self.btn_msg_send = QtWidgets.QPushButton(self.groupbox_Fault)
        self.btn_msg_send.setObjectName("btn_msg_send")
        self.horizontalLayout.addWidget(self.btn_msg_send)
        self.line = QtWidgets.QFrame(self.groupbox_Fault)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.chkbx_faultSort = QtWidgets.QCheckBox(self.groupbox_Fault)
        self.chkbx_faultSort.setChecked(True)
        self.chkbx_faultSort.setObjectName("chkbx_faultSort")
        self.horizontalLayout.addWidget(self.chkbx_faultSort)
        self.btn_fault_reload = QtWidgets.QPushButton(self.groupbox_Fault)
        self.btn_fault_reload.setObjectName("btn_fault_reload")
        self.horizontalLayout.addWidget(self.btn_fault_reload)
        self.gridLayout.addWidget(self.groupbox_Fault, 0, 0, 1, 1)
        EditTable.addTab(self.tab_faults, "")
        self.tab_msgs = QtWidgets.QWidget()
        self.tab_msgs.setObjectName("tab_msgs")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_msgs)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tbl_msgs = QtWidgets.QTableWidget(self.tab_msgs)
        self.tbl_msgs.setAlternatingRowColors(True)
        self.tbl_msgs.setColumnCount(2)
        self.tbl_msgs.setObjectName("tbl_msgs")
        self.tbl_msgs.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_msgs.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_msgs.setHorizontalHeaderItem(1, item)
        self.tbl_msgs.horizontalHeader().setDefaultSectionSize(120)
        self.tbl_msgs.horizontalHeader().setMinimumSectionSize(50)
        self.tbl_msgs.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.tbl_msgs, 1, 0, 1, 1)
        self.groupbox_Message = QtWidgets.QGroupBox(self.tab_msgs)
        self.groupbox_Message.setTitle("")
        self.groupbox_Message.setObjectName("groupbox_Message")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupbox_Message)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.status_msg = QtWidgets.QLineEdit(self.groupbox_Message)
        self.status_msg.setEnabled(False)
        self.status_msg.setObjectName("status_msg")
        self.horizontalLayout_2.addWidget(self.status_msg)
        self.line_3 = QtWidgets.QFrame(self.groupbox_Message)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.line_3)
        self.chkbx_msgEdit = QtWidgets.QCheckBox(self.groupbox_Message)
        self.chkbx_msgEdit.setObjectName("chkbx_msgEdit")
        self.horizontalLayout_2.addWidget(self.chkbx_msgEdit)
        self.btn_fault_send = QtWidgets.QPushButton(self.groupbox_Message)
        self.btn_fault_send.setObjectName("btn_fault_send")
        self.horizontalLayout_2.addWidget(self.btn_fault_send)
        self.line_4 = QtWidgets.QFrame(self.groupbox_Message)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_2.addWidget(self.line_4)
        self.chckbx_msgSort = QtWidgets.QCheckBox(self.groupbox_Message)
        self.chckbx_msgSort.setChecked(True)
        self.chckbx_msgSort.setObjectName("chckbx_msgSort")
        self.horizontalLayout_2.addWidget(self.chckbx_msgSort)
        self.btn_msg_reload = QtWidgets.QPushButton(self.groupbox_Message)
        self.btn_msg_reload.setObjectName("btn_msg_reload")
        self.horizontalLayout_2.addWidget(self.btn_msg_reload)
        self.gridLayout_2.addWidget(self.groupbox_Message, 0, 0, 1, 1)
        EditTable.addTab(self.tab_msgs, "")

        self.retranslateUi(EditTable)
        EditTable.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EditTable)

    def retranslateUi(self, EditTable):
        _translate = QtCore.QCoreApplication.translate
        EditTable.setWindowTitle(_translate("EditTable", "TabWidget"))
        self.tbl_faults.setSortingEnabled(False)
        item = self.tbl_faults.horizontalHeaderItem(0)
        item.setText(_translate("EditTable", "FaultID"))
        item = self.tbl_faults.horizontalHeaderItem(1)
        item.setText(_translate("EditTable", "Message"))
        self.chkbx_faultEdit.setToolTip(_translate("EditTable", "<html><head/><body><p>If set, send command will only send the detected changes.</p></body></html>"))
        self.chkbx_faultEdit.setText(_translate("EditTable", "Edits Only"))
        self.btn_msg_send.setText(_translate("EditTable", "Send"))
        self.chkbx_faultSort.setToolTip(_translate("EditTable", "<html><head/><body><p><span style=\" font-size:9pt;\">Tags read from PLC will be sorted by &quot;Id&quot; in accending order.</span></p></body></html>"))
        self.chkbx_faultSort.setText(_translate("EditTable", "Sort Incoming"))
        self.btn_fault_reload.setText(_translate("EditTable", "Reload"))
        EditTable.setTabText(EditTable.indexOf(self.tab_faults), _translate("EditTable", "Faults"))
        item = self.tbl_msgs.horizontalHeaderItem(0)
        item.setText(_translate("EditTable", "MessageID"))
        item = self.tbl_msgs.horizontalHeaderItem(1)
        item.setText(_translate("EditTable", "Message"))
        self.chkbx_msgEdit.setText(_translate("EditTable", "Edits Only"))
        self.btn_fault_send.setText(_translate("EditTable", "Send"))
        self.chckbx_msgSort.setToolTip(_translate("EditTable", "<html><head/><body><p>Tags read from PLC will be sorted by &quot;Id&quot; in accending order.</p></body></html>"))
        self.chckbx_msgSort.setText(_translate("EditTable", "Sort Incoming"))
        self.btn_msg_reload.setText(_translate("EditTable", "Reload"))
        EditTable.setTabText(EditTable.indexOf(self.tab_msgs), _translate("EditTable", "Messages"))
