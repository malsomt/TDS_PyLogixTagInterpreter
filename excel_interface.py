import pylogix
from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QFileDialog
import ExportWindow
import xlsxwriter

import messageFunctions


class ExcelInterface:
    """
    Interface class contains functions to interface between the PLC object and the output file.
    """

    def __init__(self, plc=None, filepath=''):
        file = xlsxwriter.Workbook('Insert name')
        assert isinstance(plc, pylogix.PLC)
        self.plc = plc  # pointer to plc object
        self._filePath = ''
        self.workbook = None
        self.filePath = filepath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, path):
        # TODO check for valid filepath/ folder structure
        self._filePath = path

    def Export(self):
        # Create Workbook
        self.workbook = xlsxwriter.Workbook(self._filePath)
        sheetNames = self.findPrograms()
        # create sheet names
        for sheetName in sheetNames:
            progName = str.replace(sheetName, 'Program:', '')
            self.workbook.add_worksheet(progName)
            faultTags = messageFunctions.loadFaults(self.plc, progName)
            messageTags = messageFunctions.loadMessages(self.plc, progName)
            # TODO - Continue building out excel spreadsheet

    def findPrograms(self):
        """
        Returns a list of Programs Names that contain valid message fault and operator tags.
        :return: List[str]
        """
        programList = []
        attempts = 2
        while attempts > 0:
            # Get The list of programs from the PLC
            ret = self.plc.GetProgramsList()
            attempts -= 1
            # check return for success
            if ret.Status == 'Success':
                programList = ret.Value
                break  # exit while
            else:
                if attempts == 0:
                    # TODO: Look into returning a Message Message Dialog box
                    return -1  # Failed by communication

        # Look for 'MessageArrayFault' and MessageArrayOperator and remove programs without those tags
        filteredProgList = []
        for prog in programList:
            target1 = prog + '.MessageArrayFault'
            target2 = prog + '.MessageArrayOperator'
            for tag in self.plc.TagList:
                if tag.TagName == target1 or tag.TagName == target2:
                    filteredProgList.append(prog)
                    break
        if len(programList) != len(filteredProgList):
            print(f'Programs List was reduced from {len(programList)} to {len(filteredProgList)}')
        # Filter the 'Program:' from the front of the names to use as sheet names
        print(filteredProgList)
        return filteredProgList

    def Import(self):
        pass

# class ExportImportWindow(ExportWindow.Ui_Export_Target, QtWidgets.QDialog):
#     def __init__(self, plc):
#         super(ExportImportWindow, self).__init__()
#         self.setupUi(self)
#         self.setWindowTitle('Set Export Target Path')
#         self.pbn_Export.clicked.connect(self.action_export)
#         self.pbn_FileExplorer.clicked.connect(self.action_fileDialog)
#         self._filePath = None
#         self.filePath = ''
#         self.plc = plc
#
#     def action_export(self):
#         # Create a custom MessageBox that locks the main thread
#         # Export Message class has extended plc to json function that calls itself on execution
#         # will return with a success of failure
#         progList = self.plc.GetProgramsList()
#         print(progList)
#         # exportFile = ExcelInterface(plc)
#         # msg = QtWidgets.QProgressDialog("Copying files...", "Abort Copy", 0, len(progList))
#         # msg.setWindowModality(Qt.WindowModal)
#
#     def action_fileDialog(self):
#         options = QFileDialog.Options()
#         # options |= QFileDialog.DontUseNativeDialog # Enable if you want to use pyQT5 file browser over windows
#         fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
#                                                   "Excel Files (*.xlxs)", options=options)
#         self.filePath = fileName  # Set filepath to the line edit box
#
#     @property
#     def filePath(self):
#         return self._filePath
#
#     @filePath.setter
#     def filePath(self, fp):
#         # Check for empty string, insert more params later if necessary
#         # Enable the Export pushbutton if valid and disable if not.
#         if fp != '':
#             self._filePath = fp
#             self.status_filePath.setText(self._filePath)
#             self.pbn_Export.setEnabled(True)
#         else:
#             self.pbn_Export.setEnabled(False)
