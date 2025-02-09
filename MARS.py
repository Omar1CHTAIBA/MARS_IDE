import sys
import os
from pathlib import Path
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QTreeView, QTabWidget, \
    QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from Lexer import Lexers


class MARS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.initMARSSettings()
        self.initMARSMenu()
        self.initMARSUI()

    def initMARSSettings(self):
        self.setWindowTitle('MARS')
        self.setGeometry(100, 100, 1500, 800)

    def initMARSUI(self):
        main_layout = QVBoxLayout()

        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        self.tree.clicked.connect(self.tree_view_clicked)
        self.tree.setHeaderHidden(True)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)

        # self.editor = Lexers().MainLexer()
        self.preview = QWebEngineView()
        # self.preview.setHidden(True)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.tab_view)
        # splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([200, 700, 500])

        main_layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def initMARSMenu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        file_menu.addSeparator()

        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        file_menu.addSeparator()

        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        edit_menu = menu_bar.addMenu("Editor")

        self.open_preview = edit_menu.addAction("Open Preview")
        self.open_preview.setShortcut("Ctrl+Shift+B")
        self.open_preview.triggered.connect(self.preview_toggle)

        self.hide_tree = edit_menu.addAction("Hide Tree")
        self.hide_tree.setShortcut("Ctrl+B")
        self.hide_tree.triggered.connect(self.tree_toggle)

        run_action = edit_menu.addAction("Run Preview")
        run_action.setShortcut("Shift+F10")
        run_action.triggered.connect(self.run)

    def is_binary(self, path):
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)

    def set_new_tab(self, path, is_new_file=False):
        self.editor = Lexers().MainLexer()
        if is_new_file:
            self.tab_view.addTab(editor, "untitled")
            self.setWindowTitle("untitled - Mars")
            self.statusBar().showMessage("Opened untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return
        if not path.is_file():
            return
        if not is_new_file and self.is_binary(path):
            self.statusBar().showMessage("Cannot open binary file", 1500)
            return

        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return

        self.tab_view.addTab(self.editor, path.name)
        self.editor.setText(path.read_text())
        self.setWindowTitle(path.name)
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 1500)

    def tree_view_clicked(self, index):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)

    def close_tab(self, index):
        self.tab_view.removeTab(index)

    def new_file(self):
        self.set_new_tab(None, True)

    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()

        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)

    def save_as(self):
        editor = self.tab_view.currentWidget()
        if editor is None:
            return

        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path

    def open_file(self):
        new_file, _ = QFileDialog.getOpenFileName(self,
                                                  "Pick A File", "", "All Files (*);;Python Files (*.py)",
                                                  )
        if new_file == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)

    def open_folder(self):
        new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "")
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def tree_toggle(self):
        if self.tree.isVisible():
            self.tree.hide()
            self.hide_tree.setText("Show Tree")
        else:
            self.tree.show()
            self.hide_tree.setText("Hide Tree")

    def preview_toggle(self):
        if self.preview.isHidden():
            self.preview.show()  # open
            self.open_preview.setText("Close Preview")
        else:
            self.preview.hide()  # close
            self.open_preview.setText("Open Preview")

    def run(self):
        html_content = self.editor.text()
        if html_content:
            self.preview.setHtml(html_content, baseUrl=QUrl.fromLocalFile(os.getcwd() + '/'))
        else:
            print("''!''__The file is empty__''!''")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MARS()
    editor.show()
    sys.exit(app.exec())