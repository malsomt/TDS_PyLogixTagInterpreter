import time

from MainWindow import *
from MessageWindow import *
import pylogix
import threading
from definitions import *

global thread1
global thread2
global windowDict
global plc


class Application(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('TDS Message Tool - v1')
        self.btn_connect.clicked.connect(self.action_connectToPLC)
        self.btn_disconnect.clicked.connect(self.action_disconnectToPLC)
        self.btn_loadPrograms.clicked.connect(self.action_loadPrograms)
        self.lst_components.doubleClicked.connect(self.action_editSelectProgram)
        self._connected = None
        self.connected = False

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
        global plc
        plc = pylogix.PLC()
        ip = self.getMainWindowIP()
        slot = self.getMainWindowSlot()

        plc.IPAddress = ip
        plc.ProcessorSlot = slot
        plc.Micro800 = False
        # Lock connection button, IP and slot button interface
        self.toggleTargetSetup(False)
        # Send connections and PlC interactions to separate thread
        self.start_ConnectToPLC()

    def action_disconnectToPLC(self):
        self.status_disp.setText('Disconnected')
        self.lst_components.clear()
        self.connected = False
        global windowDict
        global plc
        windowDict = {}  # clear window dictionary
        plc = None  # Clear plc tag

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
        global plc
        plc_time = plc.GetPLCTime()  # Used to test connection
        if plc_time.Value is not None:
            plc.GetTagList()
            self.status_disp.setText('Connected to PLC')
            self.connected = True

        else:
            self.status_disp.setText(plc_time.Status)
            self.connected = False

    def action_loadPrograms(self):
        # Use parallel thread for actions
        global thread2
        thread2 = threading.Thread(target=self.start_LoadPrograms)
        thread2.setDaemon(True)
        thread2.start()

    def start_LoadPrograms(self):
        # Poll PLC for a list of programs.
        # Return is List of strings in the response.Value
        # Format example is 'Program:S0_SystemControl'
        global plc
        response = plc.GetProgramsList()
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

    def action_editSelectProgram(self):
        # Open an instance of the tag editor table.
        # Give i the name of the program we are editing
        # Use the program name to place the window object into a global dictionary.
        global windowDict
        progName = self.lst_components.selectedItems()[0].text()

        editWindow = EditWindow()
        editWindow.setWindowTitle(progName)
        windowDict[progName] = editWindow
        windowDict[progName].show()
        thread = threading.Thread(target=self.action_load, args=(progName,), daemon=True)
        thread.start()

    def action_load(self, progName):
        # TODO: Handle the returns and search result errors better
        global windowDict
        global plc
        fullTag = f'Program:{progName}.MessageArrayFault'
        for index, tag in enumerate(plc.TagList):
            if tag.TagName == fullTag:
                arrayLength = tag.Size
                # DEBUG # print(f'Found {tag.TagName} == {fullTag} == {arrayLength}')
                break

        results = plc.Read(f'Program:{progName}.MessageArrayFault[0]', arrayLength)
        if results.Status == 'Success':
            windowDict[progName].arrayLen = arrayLength  # ensure to set the length before the results
            windowDict[progName].results = results
            windowDict[progName].disableTable = False
        else:
            windowDict[progName].disableTable = True


class EditWindow(Ui_EditTable, QtWidgets.QTabWidget):
    def __init__(self):
        super(EditWindow, self).__init__()
        self.setupUi(self)
        self.arrayLen = 0
        self._faultTags = []
        self._results = None
        self._disable_Table = None
        self.disable_Table = True

    @property
    def faultTags(self):
        return self._faultTags

    @faultTags.setter
    def faultTags(self, tags):
        self._faultTags = tags

    @property
    def results(self):
        return self._faultTags

    @results.setter
    def results(self, result):
        self._results = result
        # attempt to parse out results
        self.parse_results()

    def parse_results(self):
        for i in range(self.arrayLen):
            arr_lwr = i*180
            arr_upr = arr_lwr + 180
            self._faultTags.append(GeneralMessage(self._results.Value[arr_lwr:arr_upr]))
            #print(f'arr_lwr={arr_lwr}  arr_upr={arr_upr}')
        print(self._faultTags)

    @property
    def disableTable(self):
        return self._disable_Table

    @disableTable.setter
    def disableTable(self, flag):
        self._disable_Table = flag
        self.tbl_faults.setEnabled = not flag
        self.tbl_msg.setEnabled = not flag


if __name__ == "__main__":
    import sys

    windowDict = {}
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Application()
    MainWindow.show()
    sys.exit(app.exec_())
