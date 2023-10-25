from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QFileDialog

from ExportWindow import Ui_Export_Target


class ExportWindow(Ui_Export_Target, QtWidgets.QDialog):
    def __init__(self):
        super(ExportWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Set Export Target Path')
        self.pbn_Export.clicked.connect(self.action_export)
        self.pbn_FileExplorer.clicked.connect(self.action_fileDialog)
        self._filePath = None
        self.filePath = ''

    def action_export(self):
        # Create a custom MessageBox that locks the main thread
        # Export Message class has extended plc to json function that calls itself on execution
        # will return with a success of failure
        global plc
        progList = plc.GetProgramsList()
        msg = QtWidgets.QProgressDialog("Copying files...", "Abort Copy", 0, len(progList))
        msg.setWindowModality(Qt.WindowModal)

    def action_fileDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # Enable if you want to use pyQT5 file browser over windows
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Json Files (*.json)", options=options)
        self.filePath = fileName  # Set filepath to the line edit box

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, fp):
        # Check for empty string, insert more params later if necessary
        # Enable the Export pushbutton if valid and disable if not.
        if fp != '':
            self._filePath = fp
            self.status_filePath.setText(self._filePath)
            self.pbn_Export.setEnabled(True)
        else:
            self.pbn_Export.setEnabled(False)