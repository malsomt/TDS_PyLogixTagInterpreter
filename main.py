import csv
import io
import time

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeySequence, QBrush
from PyQt5.QtWidgets import QApplication, QDialogButtonBox

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

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # Close all Open Windows before killing main App
        global windowDict
        if len(windowDict):
            for win in windowDict:
                windowDict[win].close()

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
            self.action_loadPrograms()

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
        thread = threading.Thread(target=self.action_loadAll, args=(progName,), daemon=True)
        thread.start()
        windowDict[progName].show()

    def action_loadAll(self, progName):
        # TODO: Handle the returns and search result errors better
        global windowDict
        global plc
        arrayLength_fault = 0
        arrayLength_msgs = 0
        fullTag_fault = f'Program:{progName}.MessageArrayFault'
        fullTag_msgs = f'Program:{progName}.MessageArrayOperator'

        # Get the length of the arrays from the tag info in the plc object
        for index, tag in enumerate(plc.TagList):
            if tag.TagName == fullTag_fault:
                arrayLength_fault = tag.Size
            elif tag.TagName == fullTag_msgs:
                arrayLength_msgs = tag.Size
            if arrayLength_fault != 0 and arrayLength_msgs != 0:
                break

                # TODO: Placeholder, insert exception, update for messages
        if arrayLength_fault == 0:
            print('Killed Thread')
            return 0  # Kill thread

        results_fault = plc.Read(f'Program:{progName}.MessageArrayFault[0]', arrayLength_fault)
        results_msgs = plc.Read(f'Program:{progName}.MessageArrayOperator[0]', arrayLength_msgs)
        if results_fault.Status == 'Success' and results_msgs.Status == 'Success':
            windowDict[progName].arrayLen_faults = arrayLength_fault  # ensure to set the length before the results_fault
            windowDict[progName].arrayLen_msgs = arrayLength_msgs
            # TODO: update new results property
            windowDict[progName].results_fault = results_fault
            windowDict[progName].results_msgs = results_msgs
            windowDict[progName].disableTable = False
        else:
            windowDict[progName].disableTable = True


class EditWindow(Ui_EditTable, QtWidgets.QTabWidget):
    def __init__(self):
        super(EditWindow, self).__init__()
        self.setupUi(self)
        self.ignoreChangeEvent = False
        self.arrayLen_faults = 0
        self.arrayLen_msgs = 0
        self._faultTags = []
        self._messageTags = []
        self._results_fault = None
        self._results_msgs = None
        self._disable_Table = None
        self.disable_Table = True
        self.tbl_faults.itemChanged.connect(self.action_itemEdited_fault)
        self.tbl_msgs.itemChanged.connect(self.action_itemEdited_msg)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        modifiers = QApplication.keyboardModifiers()
        if event.type() == QEvent.KeyPress and event.matches(QKeySequence.Copy):
            self.copy_selection()
            return True
        elif event.type() == QEvent.KeyPress and event.matches(QKeySequence.Paste):
            self.paste_selection()
            return True
        return super(EditWindow, self).eventFilter(source, event)

    def copy_selection(self):
        if self.currentIndex() == 0:
            activeTable = self.tbl_faults
        elif self.currentIndex() == 1:
            activeTable = self.tbl_msgs
        else:
            return
        selection = activeTable.selectedIndexes()
        if selection:
            all_rows = []
            all_columns = []
            for index in selection:
                if not index.row() in all_rows:
                    all_rows.append(index.row())
                if not index.column() in all_columns:
                    all_columns.append(index.column())
            visible_rows = [row for row in all_rows if not activeTable.isRowHidden(row)]
            visible_columns = [col for col in all_columns if not activeTable.isColumnHidden(col)]

            table = [[""] * len(visible_columns) for _ in range(len(visible_rows))]
            for index in selection:
                if index.row() in visible_rows and index.column() in visible_columns:
                    selection_row = visible_rows.index(index.row())
                    selection_column = visible_columns.index(index.column())
                    table[selection_row][selection_column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter="\t").writerows(table)
            QApplication.clipboard().setText(stream.getvalue())

    def paste_selection(self):
        try:
            if self.currentIndex() == 0:
                activeTable = self.tbl_faults
            elif self.currentIndex() == 1:
                activeTable = self.tbl_msgs
            else:
                return
            selection = activeTable.selectedIndexes()
            if selection:
                model = activeTable.model()
                buffer = QApplication.clipboard().text()
                all_rows = []
                all_columns = []
                for index in selection:
                    if not index.row() in all_rows:
                        all_rows.append(index.row())
                    if not index.column() in all_columns:
                        all_columns.append(index.column())
                reader = csv.reader(io.StringIO(buffer), delimiter="\t")
                arr = [[cell for cell in row] for row in reader]
                print(arr)
                if len(arr) > 0:
                    nrows = len(arr)
                    ncols = len(arr[0])
                    if len(all_rows) == 1 and len(all_columns) == 1:
                        # Only the top-left cell is highlighted.
                        for i in range(nrows):
                            insert_rows = [all_rows[0]]
                            row = insert_rows[0]
                            while len(insert_rows) < nrows:
                                row += 1
                                if not activeTable.isRowHidden(row):
                                    insert_rows.append(row)
                        for j in range(ncols):
                            insert_columns = [all_columns[0]]
                            col = insert_columns[0]
                            while len(insert_columns) < ncols:
                                col += 1
                                if not activeTable.isColumnHidden(col):
                                    insert_columns.append(col)
                        for i, insert_row in enumerate(insert_rows):
                            for j, insert_column in enumerate(insert_columns):
                                cell = arr[i][j]
                                model.setData(model.index(insert_row, insert_column), cell)
                    else:
                        # Assume the selection size matches the clipboard data size.
                        for index in selection:
                            selection_row = all_rows.index(index.row())
                            selection_column = all_columns.index(index.column())
                            model.setData(model.index(index.row(), index.column()), arr[selection_row][selection_column])
            return
        except IndexError:
            # Ignore Index Error , re-create by selecting more cells than clipboard has available.
            pass

    def parse_results(self, type):
        if type == 'faults':
            for i in range(self.arrayLen_faults):
                arr_lwr = i * 180
                arr_upr = arr_lwr + 180
                self._faultTags.append(GeneralMessageExt(self._results_fault.Value[arr_lwr:arr_upr]))
        elif type == 'messages':
            for i in range(self.arrayLen_msgs):
                arr_lwr = i * 180
                arr_upr = arr_lwr + 180
                self._messageTags.append(GeneralMessageExt(self._results_msgs.Value[arr_lwr:arr_upr]))
        self.display_results_fault()
        self.display_results_msgs()

    def display_results_fault(self):
        self.ignoreChangeEvent = True
        self.tbl_faults.setRowCount(self.arrayLen_faults)
        for row, tag in enumerate(self._faultTags):
            self.tbl_faults.setItem(row, 0, QtWidgets.QTableWidgetItem(str(tag.Id)))
            self.tbl_faults.setItem(row, 1, QtWidgets.QTableWidgetItem(tag.Text))
        self.tbl_faults.update()
        self.ignoreChangeEvent = False

    def display_results_msgs(self):
        self.ignoreChangeEvent = True
        self.tbl_msgs.setRowCount(self.arrayLen_msgs)
        for row, tag in enumerate(self._messageTags):
            self.tbl_msgs.setItem(row, 0, QtWidgets.QTableWidgetItem(str(tag.Id)))
            self.tbl_msgs.setItem(row, 1, QtWidgets.QTableWidgetItem(tag.Text))
        self.tbl_msgs.update()
        self.ignoreChangeEvent = False

    def action_itemEdited_fault(self, item):
        assert isinstance(item, QtWidgets.QTableWidgetItem)
        if self.ignoreChangeEvent:  # ignore action when populating table
            return
        # row should align with the list index of tags
        if item.column() == 0:  # Aligns with .Id
            try:
                self.faultTags[item.row()].newId = int(item.text())
            except ValueError:
                item.setText(str(self.faultTags[item.row()].newId))
                print(f'Attempted to set Id to non-INTEGER value.')
        elif item.column() == 1:  # Aligns with .Text
            try:
                self.faultTags[item.row()].newText = item.text()
            except Exception:
                print("No Idea what happened...don't try whatever you did again.\nThat's One...")
        print(f'Flag has been set to {self.faultTags[item.row()].edits}')
        if self.faultTags[item.row()].edits:
            # TODO: Look into the QBrush class and set up a background color
            pass

    def action_itemEdited_msg(self):
        pass

    @property
    def faultTags(self):
        return self._faultTags

    @faultTags.setter
    def faultTags(self, tags):
        self._faultTags = tags

    @property
    def results_fault(self):
        return self._results_fault

    @results_fault.setter
    def results_fault(self, result):
        self._results_fault = result
        # attempt to parse out results
        self.parse_results('faults')

    @property
    def results_msgs(self):
        return self._results_msgs

    @results_msgs.setter
    def results_msgs(self, result):
        self._results_msgs = result
        # attempt to parse out results
        self.parse_results('messages')

    @property
    def disableTable(self):
        return self._disable_Table

    @disableTable.setter
    def disableTable(self, flag):
        self._disable_Table = flag
        self.tbl_faults.setEnabled = not flag
        self.tbl_msgs.setEnabled = not flag


if __name__ == "__main__":
    import sys

    windowDict = {}
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Application()
    MainWindow.show()
    sys.exit(app.exec_())
