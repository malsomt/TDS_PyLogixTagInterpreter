import time

from MainWindow import *

import pylogix
import threading

global thread1
global thread2


class Application(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('TDS Message Tool - v1')
        self.btn_connect.clicked.connect(self.action_connectToPLC)
        self.btn_disconnect.clicked.connect(self.action_disconnectToPLC)
        self.btn_loadPrograms.clicked.connect(self.action_loadPrograms)
        self._connected = None
        self.connected = False
        self.plc = None

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, flag):
        self._connected = flag
        self.toggleTargetSetup(not flag)
        self.group_components.setEnabled(flag)

    def action_connectToPLC(self):
        self.status_disp.setText('Attempting to connect...')

        self.plc = pylogix.PLC()
        ip = self.getMainWindowIP()
        slot = self.getMainWindowSlot()

        self.plc.IPAddress = ip
        self.plc.ProcessorSlot = slot
        self.plc.Micro800 = False
        # Lock connection button, IP and slot button interface
        self.toggleTargetSetup(False)
        # Send connections and PlC interactions to separate thread
        self.start_ConnectToPLC()

    def action_disconnectToPLC(self):
        self.status_disp.setText('Disconnected')
        self.connected = False

    def toggleTargetSetup(self, flag):
        self.ip_1.setEnabled(flag)
        self.ip_2.setEnabled(flag)
        self.ip_3.setEnabled(flag)
        self.ip_4.setEnabled(flag)
        self.ip_slot.setEnabled(flag)
        self.btn_connect.setEnabled(flag)
        self.btn_disconnect.setEnabled(not flag)

    def start_ConnectToPLC(self):
        # Define thread and start function on parallel thread
        global thread1
        try:
            thread1 = threading.Thread(target=self.connection_test)
            thread1.setDaemon(True)
            thread1.start()
        except Exception as e:
            print('unable to start connection_test, ' + str(e))

    def connection_test(self):
        plc_time = self.plc.GetPLCTime()  # Used to test connection
        if plc_time.Value is not None:
            self.status_disp.setText('Connected to PLC')
            self.connected = True

        else:
            self.status_disp.setText(plc_time.Status)
            self.connected = False

    def action_loadPrograms(self):
        #Use parallel thread for actions
        global thread2
        thread2 = threading.Thread(target=self.start_LoadPrograms)
        thread2.setDaemon(True)
        thread2.start()

    def start_LoadPrograms(self):
        # Poll PLC for a list of programs.
        # Return is List of strings in the response.Value
        # Format example is 'Program:S0_SystemControl'

        response = self.plc.GetProgramsList()
        if response.Status == 'Success':
            self.lst_components.clear()
            list.sort(response.Value)
            for p in response.Value:
                p = str.replace(p, 'Program:', '')
                item = QtWidgets.QListWidgetItem(p)
                self.lst_components.addItem(item)
        else:
            self.status_disp.setText(f'Operation Failed - {response.Status}')

    def getMainWindowIP(self):
        # return ip address formatted for pylogix PLC comms
        ip1 = str(self.ip_1.value())
        ip2 = str(self.ip_2.value())
        ip3 = str(self.ip_3.value())
        ip4 = str(self.ip_4.value())
        return ip1 + '.' + ip2 + '.' + ip3 + '.' + ip4

    def getMainWindowSlot(self):
        # return the processor slot selected from the main window
        return self.ip_slot.value()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Application()
    MainWindow.show()
    sys.exit(app.exec_())
