# from colorama import Fore, Back, Style
from scripts import dir_walk_2
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5 import QtCore
from scripts.ui import file_finder
import multiprocessing
from multiprocessing import freeze_support


def OpenFile(parent, title, preferred_dir=None):
    options = QFileDialog.Options()
    options |= QFileDialog.DirectoryOnly
    if preferred_dir is None:
        preferred_dir = QUrl.fromLocalFile(os.getcwd())
    fileName = QFileDialog.getExistingDirectoryUrl(parent, caption=title, directory=preferred_dir, options=options)
    fileName: QUrl
    file_name_string = QUrl.toLocalFile(fileName)
    if file_name_string:
        return file_name_string
    else:
        print(file_name_string, "returned None")
        return None


class SearchThread(QtCore.QThread):
    values = QtCore.pyqtSignal(dict)

    def __init__(self, file_name, destination):
        super(SearchThread, self).__init__()
        self.destination = destination
        self.file_name = file_name

    def run(self) -> None:
        manager_dict = dir_walk_2.start_process(self.file_name, self.destination)  # returns a list
        # print(Fore.RED + "Returning value"+ Style.RESET_ALL)
        self.values.emit(manager_dict)


class Application(QMainWindow):
    def __init__(self):
        super().__init__()

        self.failed_label = QLabel(self)
        self.ui = file_finder.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ListWidget = QListWidget(self)
        self.ListWidget.setSpacing(5)  # gaps 5 per item
        self.ui.verticalLayout.addWidget(self.ListWidget)
        self.ui.lineEdit.setFocus()
        self.index = 2
        self.ListWidget.setHidden(True)
        self.ui.lineEdit.textEdited.connect(self.clear_n_hide)
        self.ui.lineEdit.resize(self.ui.lineEdit.baseSize())
        self.ui.lineEdit.returnPressed.connect(self.search)
        self.ui.lineEdit_2.returnPressed.connect(self.search)
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.pushButton_open.clicked.connect(self.openLoc)

    def openLoc(self):
        location = OpenFile(self, "Select Folder")
        print(location)
        if location:
            self.ui.lineEdit_2.setText(os.path.realpath(location))

    def clear_n_hide(self):
        if self.index == 1:
            self.failed_label.deleteLater()
            self.index = 2

        elif self.index == 0:
            self.ListWidget.clear()
            self.ListWidget.setHidden(True)

    def show_failed(self):
        self.failed_label = QLabel(self)
        self.ui.verticalLayout.addWidget(self.failed_label)
        self.failed_label.setStyleSheet('color : red')
        self.failed_label.setText('Search Unsuccessful!')

        self.index = 1

    def putIntoList(self, list_view):
        self.ListWidget.setHidden(False)
        self.ListWidget.clear()
        for item in list_view:
            self.ListWidget.addItem(item)

    def search(self):
        """
        Method gets called when search button pressed or Return pressed on LineEdit

        :return: None
        """
        # get the filename and destination to be searched
        self.clear_n_hide()
        file_name = self.ui.lineEdit.text()
        destination = self.ui.lineEdit_2.text()
        print(f'File:{file_name}\nDestination:{destination}')

        try:
            if len(file_name) >= 2 and len(destination) > 2:  # just a measure to ensure file name is not too short
                if os.path.exists(destination) and os.path.isdir(destination):  # check if file path exists
                    # os.chdir(destination)  # this is unnecessary
                    self.search_thread = SearchThread(file_name, destination)
                    self.search_thread.values.connect(self.search_result)
                    self.search_thread.start()
                    self.ui.statusbar.showMessage("Searching...Please Wait...")
            else:
                self.show_failed()
        except Exception as e:
            print('Error in Searching, tune file search!', e)
            self.show_failed()
            self.ui.lineEdit.clear()
            self.ui.lineEdit.setFocus()

    def search_result(self, manager_dict):
        # print(manager_dict)
        self.ui.statusbar.clearMessage()
        if 'locs' in manager_dict.keys():
            list_view = manager_dict['locs']
        else:
            list_view = []
        if len(list_view):
            self.index = 0
            self.putIntoList(list_view)
            print('\n'.join(list_view))
        else:
            self.show_failed()
            print('Nothing Found!')
        self.ui.lineEdit.clear()
        self.ui.lineEdit.setFocus()


if __name__ == '__main__':
    freeze_support()
    app = QApplication(sys.argv)
    class_instance = Application()
    class_instance.show()
    sys.exit(app.exec_())
