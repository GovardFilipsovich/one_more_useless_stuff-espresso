import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidgetItem, QDialog
from PyQt5 import uic
import sqlite3
from MainUi import Ui_widget
from addEditCoffeeForm import Ui_Form


class Form(QDialog, Ui_Form):
    def __init__(self, parent=None, mod=0):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.par = parent
        self.Enter.clicked.connect(self.enter)
        if mod != 0:
            self.name.setText(self.par.res[1])
            self.level.setText(self.par.res[2])
            self.grinding.setText(self.par.res[3])
            self.descr.setText(self.par.res[4])
            self.cost.setText(str(self.par.res[5]))
            self.volume.setText(str(self.par.res[6]))

    def enter(self):
        self.close()

    def closeEvent(self, event):
        try:
            self.par.add_or_change = (self.name.text(), self.level.text(), self.grinding.text(), self.descr.text(), int(self.cost.text()), int(self.volume.text()))
        except ValueError:
            self.par.add_or_change = -1


class Example(QWidget, Ui_widget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupUi(self)
        self.fill_table()
        self.add_or_change = -1
        self.res = -1
        self.run()

    def initUI(self):
        self.con = sqlite3.connect("coffee.sqlite")
        

    def run(self):
        self.tableWidget.cellClicked.connect(self.work)
        self.add.clicked.connect(self.add_launch_form)
        self.change.clicked.connect(self.change_launch_form)
        

    def add_launch_form(self):
        form = Form(self)
        form.exec()
        if self.add_or_change != -1:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO coffee(name, level_of_roasting, grinding, description_of_taste, cost, volume) VALUES("{}", "{}", "{}", "{}", {}, {})""".format(*self.add_or_change))
            self.con.commit()
            self.fill_table()

    def change_launch_form(self):
        form = Form(self, 1)
        form.exec()
        if self.res == -1:
            print("Error: choose coffee")
        elif self.add_or_change != -1:
            cur = self.con.cursor()
            cur.execute("""UPDATE coffee set name = "{}", level_of_roasting = "{}", grinding = "{}", description_of_taste = "{}", cost = {}, volume = {} where name = "{}" """.format(*self.add_or_change, self.name))
            self.con.commit()
            self.fill_table()

        

    def work(self, value):
        self.name = self.tableWidget.selectedItems()[0].text()
        self.res = self.con.execute("""SELECT * from coffee where name = "{}" """.format(self.name)).fetchone()
        c = 0
        descr = str()
        for i in self.res[4].split():
            c += len(i)
            if c > 20:
                descr += "\n"
                c = 0
            descr += " " + i
        text = "Название: " + self.res[1] + "\n" + self.res[2] + "\n" + self.res[3] + "\n" + "Описание: " + descr + "\n" + "Цена: " + str(self.res[5]) + "\n" + "Объем: " + str(self.res[-1])

        self.label.setText(text)

    def fill_table(self):
        res = self.con.execute("SELECT name from coffee").fetchall()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
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