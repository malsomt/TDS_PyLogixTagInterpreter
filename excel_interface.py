import pylogix
from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox
import ExportWindow
import xlsxwriter
from xlsxwriter import exceptions

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
        try:
            # Create Workbook
            self.workbook = xlsxwriter.Workbook(self._filePath)
            sheetNames = self.findPrograms()
            # create sheet names
            for sheetName in sheetNames:  # Loop Programs as sheets
                progName = str.replace(sheetName, 'Program:', '')
                worksheet = self.workbook.add_worksheet(progName)
                bold = self.workbook.add_format({'bold': True})  # create bold formatting
                wrap = self.workbook.add_format({'text_wrap': True})
                faultTags = messageFunctions.loadFaults(self.plc, progName)
                messageTags = messageFunctions.loadMessages(self.plc, progName)
                # set column width
                worksheet.set_column(0, 0, 10)  # Format ID Columns
                worksheet.set_column(4, 4, 10)  # Format ID Columns
                worksheet.set_column(1, 2, 40)  # Format Text Columns
                worksheet.set_column(5, 6, 40)  # Format Text Columns
                worksheet.set_column(3, 3, 15)  # Format Divider
                # Build out Headers
                worksheet.write('A1', 'Fault ID', bold)
                worksheet.write('B1', 'Text', bold)
                worksheet.write('C1', 'AltText', bold)
                # Skip Column D For readability
                worksheet.write('E1', 'Message ID', bold)
                worksheet.write('F1', 'Text', bold)
                worksheet.write('G1', 'AltText', bold)
                # enumerate and write out tag data for Faults
                for index, tag in enumerate(faultTags):
                    index = index + 2  # Avoid overwriting the Headers
                    id = worksheet.write(f'A{index}', tag.Id, wrap)
                    text = worksheet.write(f'B{index}', tag.Text, wrap)
                    altText = worksheet.write(f'C{index}', tag.AltText, wrap)
                    if id or text or altText:
                        raise exceptions.XlsxWriterException(f'Writer Fault Status: Id:{id}, Text:{text}, AltText:{altText}')
                # enumerate this for messages since they may have different lengths
                for index, tag in enumerate(messageTags):
                    index = index + 2  # Avoid overwriting the Headers
                    id = worksheet.write(f'E{index}', tag.Id, wrap)
                    text = worksheet.write(f'F{index}', tag.Text, wrap)
                    altText = worksheet.write(f'G{index}', tag.AltText, wrap)
                    if id or text or altText:
                        raise exceptions.XlsxWriterException(f'Writer Message Status: Id:{id}, Text:{text}, AltText:{altText}')

            self.workbook.close()
        except exceptions.FileCreateError:
            msg = QMessageBox(QMessageBox.Warning, 'File Create Error',
                              'XlSX writer cannot edit file.\n'
                              'Ensure the file is not open by another process and try again.',
                              QMessageBox.Ok)

            msg.exec()

        except exceptions.XlsxWriterException:
            msg = QMessageBox(QMessageBox.Warning, 'Errors Detected',
                              'XLSX writer returned an error during the write process.\n '
                              'The output file may not be accurate.',
                              QMessageBox.Ok)
            msg.exec()
        else:
            msg = QMessageBox(QMessageBox.Information, 'Complete', 'Tag Export Complete.', QMessageBox.Ok)
            msg.exec()

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
