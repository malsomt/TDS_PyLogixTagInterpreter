import csv
import io

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeySequence, QColor
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

import messageFunctions
from MainWindow import *
from MessageWindow import *
import threading
from definitions import *
from excel_interface import ExcelInterface
from messageFunctions import loadMessages, loadFaults, sortTagList

global windowDict  # Maintain all QT window pointers in dictionary for easy commanding from outside scope
global plc  # Global plc variable created as master instance of PLC class


class Application(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('TDS Message Tool - v1')
        self.btn_connect.clicked.connect(self.action_connectToPLC)
        self.btn_disconnect.clicked.connect(self.action_disconnectToPLC)
        self.btn_loadPrograms.clicked.connect(self.action_loadPrograms)
        self.lst_components.doubleClicked.connect(self.action_editSelectProgram)
        self.btn_export.clicked.connect(self.action_export)
        self.btn_import.clicked.connect(self.action_import)
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
        # Override Export/ImportButtons for V1
        self.btn_export.setEnabled(True)
        self.btn_import.setEnabled(True)

    def action_export(self):
        global windowDict
        global plc
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # Enable if you want to use pyQT5 file browser over windows
        filePath, _ = QFileDialog.getSaveFileName(self, "Target for Tag File", "",
                                                  "Excel Files (*.xlsx)", options=options)
        if filePath != '':
            print(str(filePath))
            file = ExcelInterface(plc=plc, filepath=filePath)
            file.Export()

    def action_import(self):
        global windowDict
        global plc
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # Enable if you want to use pyQT5 file browser over windows
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Tag File", "",
                                                  "Excel Files (*.xlsx)", options=options)
        if filePath != '':
            file = ExcelInterface(plc=plc, filepath=filePath)
            file.Import()

    def action_connectToPLC(self):
        self.status_disp.setText('Attempting to connect...')
        global plc
        plc = PLCExt()
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
        plc.Close()
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
        try:
            thread = threading.Thread(target=self.connection_test, daemon=True)
            thread.start()
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
        windowDict[progName].show()


class EditWindow(Ui_EditTable, QtWidgets.QTabWidget):
    def __init__(self):
        super(EditWindow, self).__init__()
        self.setupUi(self)
        self.ignoreChangeEvent = False
        self._faultTags = []
        self._messageTags = []
        self.tbl_faults.itemChanged.connect(self.action_itemEdited_fault)
        self.tbl_msgs.itemChanged.connect(self.action_itemEdited_msg)
        self.installEventFilter(self)
        self.btn_fault_reload.clicked.connect(self.action_reload_faults)
        self.btn_msg_reload.clicked.connect(self.action_reload_msgs)
        self.btn_fault_send.clicked.connect(self.action_send_msgs)
        self.btn_msg_send.clicked.connect(self.action_send_faults)
        self.chkbx_faultSortIn.stateChanged.connect(self.action_faultSortInCheckboxChanged)
        self.chkbx_msgSortIn.stateChanged.connect(self.action_msgSortInCheckboxChanged)
        self.tbl_faults.setColumnWidth(1, 700)
        self.tbl_msgs.setColumnWidth(1, 700)

    def action_faultSortInCheckboxChanged(self):
        self.action_reload_faults()

    def action_msgSortInCheckboxChanged(self):
        self.action_reload_msgs()

    def show(self):  # Extend Base Class show()
        global plc
        super(EditWindow, self).show()
        progName = self.windowTitle()
        self.faultTags = loadFaults(plc, progName)
        self.messageTags = loadMessages(plc, progName)
        if self.faultTags is not None and self.messageTags is not None:
            self.display_results_fault()
            self.display_results_msgs()
        else:
            mbx = QMessageBox(QMessageBox.Information, 'Message Error',
                              'Unable to find tags "MessageArrayFault" or "MessageArrayOperator" '
                              'in this component program.',
                              QMessageBox.Ok)
            mbx.exec()
            self.close()  # Kill window

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
                            model.setData(model.index(index.row(), index.column()),
                                          arr[selection_row][selection_column])
            return
        except IndexError:
            # Ignore Index Error , you can re-create by selecting more cells than clipboard has available.
            pass

    def display_results_fault(self):
        self.ignoreChangeEvent = True
        self.tbl_faults.clearContents()
        self.tbl_faults.setRowCount(len(self.faultTags))
        if self.chkbx_faultSortIn.isChecked():
            self.faultTags = sortTagList(self.faultTags)  # Sort the fault tags
        for row, tag in enumerate(self.faultTags):
            self.tbl_faults.setItem(row, 0, QtWidgets.QTableWidgetItem(str(tag.Id)))
            self.tbl_faults.setItem(row, 1, QtWidgets.QTableWidgetItem(tag.Text))
            self.tbl_faults.setItem(row, 2, QtWidgets.QTableWidgetItem(tag.AltText))
        self.tbl_faults.update()
        self.ignoreChangeEvent = False
        update = f'Loaded {self.tbl_faults.rowCount()} messages from PLC'
        self.lcd_faults.display(len(self.faultTags))
        self.status_fault.setText(self.prepend_DateTime(update))

    def display_results_msgs(self):
        self.ignoreChangeEvent = True
        self.tbl_msgs.clearContents()
        self.tbl_msgs.setRowCount(len(self.messageTags))
        if self.chkbx_msgSortIn.isChecked():
            self.messageTags = sortTagList(self.messageTags)  # Sort the msg tags
        for row, tag in enumerate(self._messageTags):
            self.tbl_msgs.setItem(row, 0, QtWidgets.QTableWidgetItem(str(tag.Id)))
            self.tbl_msgs.setItem(row, 1, QtWidgets.QTableWidgetItem(tag.Text))
            self.tbl_msgs.setItem(row, 2, QtWidgets.QTableWidgetItem(tag.AltText))
        self.tbl_msgs.update()
        self.ignoreChangeEvent = False
        update = f'Loaded {self.tbl_msgs.rowCount()} messages from PLC'
        self.lcd_msg.display(len(self.messageTags))
        self.status_msg.setText(self.prepend_DateTime(update))

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
            self.faultTags[item.row()].newText = item.text()

        elif item.column() == 2:  # Aligns with .AltText
            self.faultTags[item.row()].newAltText = item.text()

        if self.faultTags[item.row()].edits:
            item.setBackground(QColor(255, 255, 150))
            # print(item.background().color().getRgb())
        else:
            if item.row() % 2 == 0:  # White to match alternating default color
                item.setBackground(QColor(255, 255, 255))
            else:  # Slight Gray to Match Alternating default color
                item.setBackground(QColor(245, 245, 245))

    def action_itemEdited_msg(self, item):
        assert isinstance(item, QtWidgets.QTableWidgetItem)
        if self.ignoreChangeEvent:  # ignore action when populating table
            return
        # row should align with the list index of tags
        if item.column() == 0:  # Aligns with .Id
            try:
                self.messageTags[item.row()].newId = int(item.text())
            except ValueError:
                item.setText(str(self.messageTags[item.row()].newId))
                print(f'Attempted to set Id to non-INTEGER value.')
        elif item.column() == 1:  # Aligns with .Text
            self.messageTags[item.row()].newText = item.text()

        elif item.column() == 2:  # Aligns with .AltText
            self.messageTags[item.row()].newAltText = item.text()

        if self.messageTags[item.row()].edits:
            item.setBackground(QColor(255, 255, 150))
            # print(item.background().color().getRgb())
        else:
            if item.row() % 2 == 0:  # White to match alternating default color
                item.setBackground(QColor(255, 255, 255))
            else:  # Slight Gray to Match Alternating default color
                item.setBackground(QColor(245, 245, 245))

    def prepend_DateTime(self, text):
        from datetime import datetime
        dt = datetime.now()
        out = f'{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}:{dt.second}'
        return out + ' ' + text

    def action_reload_faults(self):
        global plc
        self.status_fault.setText('Loading Tags from PLC...')
        progName = self.windowTitle()
        self.faultTags = loadFaults(plc, progName)
        self.display_results_fault()

    def action_reload_msgs(self):
        global plc
        self.status_msg.setText('Loading Tags from PLC...')
        progName = self.windowTitle()
        self.messageTags = loadMessages(plc, progName)

    def action_send_faults(self):
        """
        Action changed to send every tag every time.
        Sending Edits only feature has been removed
        """
        global plc
        progName = self.windowTitle()
        if self.chkbx_faultSortOut.isChecked():
            changeList = sortTagList(self.faultTags)
        else:
            changeList = self.faultTags

        if len(changeList):
            messageFunctions.send_faults(plc=plc, progName=progName, tagList=changeList)

    def action_send_msgs(self):
        """
        Replication of action_send_faults.
        """
        global plc
        progName = self.windowTitle()
        if self.chkbx_msgSortOut.isChecked():
            changeList = sortTagList(self.messageTags)
        else:
            changeList = self.messageTags

        if len(changeList):
            messageFunctions.send_messages(plc=plc, progName=progName, tagList=changeList)

    @property
    def faultTags(self):
        return self._faultTags

    @faultTags.setter
    def faultTags(self, tags):
        self._faultTags = tags

    @property
    def messageTags(self):
        return self._messageTags

    @messageTags.setter
    def messageTags(self, tags):
        self._messageTags = tags


if __name__ == "__main__":
    import sys

    windowDict = {}
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Application()
    MainWindow.show()
    sys.exit(app.exec_())
