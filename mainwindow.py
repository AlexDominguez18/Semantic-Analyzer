from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap

from ui_mainwindow import Ui_MainWindow
from lexical_analyzer import LexicalAnalyzer
from syntactic_analyzer import SyntacticAnalyzer

ERROR = 1
ACCEPTED = 2

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntactic_analyzer = SyntacticAnalyzer()
        self.ui.setupUi(self)

        #Slots
        self.ui.analyzePB.clicked.connect(self.analyze_btn_clicked)
        self.ui.clearPB.clicked.connect(self.clear_all_areas)
    
    @pyqtSlot()
    def analyze_btn_clicked(self):
        codeText = self.ui.codeTextEdit.toPlainText()
        if (len(codeText)):
            self.lexical_analyzer.analyze(codeText)
            code = self.lexical_analyzer.get_results()
            self.show_table_results(code)
            self.lexical_analyzer.clear()
            accepted, root = self.syntactic_analyzer.is_accepted(code)
            if accepted:
                self.show_message("¡Sintácticamente válido!", "", ACCEPTED)
            else:
                self.show_message("¡Sintácticamente inválido!", "Error", ERROR)
            #Semantic analyzer
            root.validate_semantic()
            self.show_symbol_table(root.table)
            self.show_semantic_errors(root.errors)
            root.table = []
            root.errors = []      
        else:
            self.show_message("El área de texto está vacía.", "Error", ERROR)

    @pyqtSlot()
    def clear_all_areas(self):
        self.ui.codeTextEdit.clear()
        self.ui.assemblyTextEdit.clear()
        self.ui.resultsTB.clearContents()
        self.ui.resultsTB.setRowCount(0)
        self.ui.tableSymbol.clearContents()
        self.ui.tableSymbol.setRowCount(0)
        self.ui.errors.text = ""
    
    #Functions

    def show_semantic_errors(self, errors):
        str = '********Errores********\n'
        for e in errors:
            str += "- " + e + "\n"
        self.ui.errors.appendPlainText(str)

    def show_symbol_table(self, table):
        rows = 0
        self.ui.tableSymbol.clearContents()
        self.ui.tableSymbol.setRowCount(rows)

        for item in table:
            self.ui.tableSymbol.insertRow(self.ui.tableSymbol.rowCount())
            self.ui.tableSymbol.setItem(rows, 0, QTableWidgetItem(str(item['id'])))
            self.ui.tableSymbol.setItem(rows, 1, QTableWidgetItem(str(item['type'])))
            self.ui.tableSymbol.setItem(rows, 2, QTableWidgetItem(str(item['ambit'])))
            self.ui.tableSymbol.setItem(rows, 3, QTableWidgetItem(str(item['params'])))
            rows += 1

    def show_table_results(self, results):
        rows = 0
        self.ui.resultsTB.clearContents()
        self.ui.resultsTB.setRowCount(rows)

        for item in results:
            self.ui.resultsTB.insertRow(self.ui.resultsTB.rowCount())
            self.ui.resultsTB.setItem(rows, 0, QTableWidgetItem(str(item['token'])))
            self.ui.resultsTB.setItem(rows, 1, QTableWidgetItem(str(item['lexeme'])))
            self.ui.resultsTB.setItem(rows, 2, QTableWidgetItem(str(item['number'])))
            rows += 1
    
    def show_message(self, message, title, type):
        modal = QMessageBox()
        if type == ERROR:
            icon = QPixmap('img/wrong.jpg')
        elif type == ACCEPTED:
            icon = QPixmap('img/right.jpg')
        icon2 = icon.scaled(64, 64, Qt.KeepAspectRatio)
        modal.setIconPixmap(icon2)
        modal.setWindowTitle(title)
        modal.setText(message)
        modal.exec()
