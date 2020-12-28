import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidgetItem
from PyQt5 import uic
import sqlite3

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fill_table()
        self.run()

    def initUI(self):
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.res = self.con.execute("SELECT name from coffee").fetchall()

    def run(self):
        self.tableWidget.cellClicked.connect(self.work)

    def work(self, value):
        name = self.tableWidget.selectedItems()[0].text()
        res = self.con.execute("""SELECT * from coffee where name = "{}" """.format(name)).fetchone()
        c = 0
        descr = str()
        for i in res[4].split():
            c += len(i)
            if c > 20:
                descr += "\n"
                c = 0
            descr += " " + i
        text = "Название: " + res[1] + "\n" + res[2] + "\n" + res[3] + "\n" + "Описание: " + descr + "\n" + "Цена: " + str(res[5]) + "\n" + "Объем: " + str(res[-1])

        self.label.setText(text)

    def fill_table(self):
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.con.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())