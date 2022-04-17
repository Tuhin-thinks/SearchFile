import subprocess
import sys
import typing

from PyQt5 import QtWidgets, QtCore, QtGui


class SearchResultView(QtWidgets.QListView):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        self.__links_list = []
        self.__model = QtGui.QStandardItemModel()
        self.setModel(self.__model)

    def repopulate_model(self, data: typing.List[str], links: typing.List[str]):
        self.__links_list = links
        self.__model.clear()
        for item in data:
            self.__model.appendRow(QtGui.QStandardItem(item))

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QtWidgets.QMenu(self)
        menu.addAction("Copy Path", self.__copy_selected)
        menu.addAction("Open in Files", self.__open_selected)
        menu.exec_(event.globalPos())

    def __copy_selected(self) -> None:
        selected_indexes = self.selectedIndexes()
        if len(selected_indexes) == 0:
            return
        selected_index = selected_indexes[0]
        selected_link = self.__links_list[selected_index.row()]
        QtWidgets.QApplication.clipboard().setText(selected_link)

        # todo: show message that, link has been copied

    def __open_selected(self) -> None:
        selected_indexes = self.selectedIndexes()
        if len(selected_indexes) == 0:
            return
        selected_index = selected_indexes[0]
        selected_link = self.__links_list[selected_index.row()]
        if sys.platform == "win32":
            QtCore.QProcess.startDetached("explorer.exe", ["/select", selected_link])
        else:
            # get default file manager
            default_filemanager = subprocess.check_output("xdg-mime query default"
                                                          " inode/directory".split(' ')).decode('utf-8').strip()
            # if, default file manager is nemo.desktop then, command is 'nemo'
            file_manager_command = default_filemanager.rsplit('.', 1)[0]
            QtCore.QProcess.startDetached(file_manager_command, [selected_link])

    def clear(self) -> None:
        self.__model.clear()
