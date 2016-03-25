import sys
from PyQt5 import QtWidgets, QtGui, QtSql, QtCore, Qt

def initializeModel(model):
   model.setTable('sportsmen')
   model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
   model.select()
   model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
   model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
   model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")

def createView(title, model):
   view = QtWidgets.QTableView()
   view.setModel(model)
   view.setWindowTitle(title)
   return view

def addrow():
   print model.rowCount()
   ret = model.insertRows(model.rowCount(), 1)
   print ret

def findrow(i):
   delrow = i.row()

if __name__ == '__main__':

   app = QtWidgets.QApplication(sys.argv)
   db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName('sports.db')
   model = QtSql.QSqlTableModel()
   delrow = -1
   initializeModel(model)

   view1 = createView("Table Model (View 1)", model)
   view1.horizontalHeader().sectionResizeMode(QtWidgets.QHeaderView.Fixed)
   view1.horizontalHeader().setDefaultSectionSize(700/3)
   view1.clicked.connect(findrow)

   dlg = QtWidgets.QWidget()
   dlg.setFixedSize(700, 400)
   layout = QtWidgets.QVBoxLayout()
   layout.addWidget(view1)

   buttonlayout = QtWidgets.QHBoxLayout()

   button = QtWidgets.QPushButton("Add a row")
   button.clicked.connect(addrow)
   layout.addWidget(button)

   btn1 = QtWidgets.QPushButton("del a row")
   btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
   layout.addWidget(btn1)

   buttonlayout.addWidget(button)
   buttonlayout.addWidget(btn1)
   layout.addLayout(buttonlayout)

   dlg.setLayout(layout)
   dlg.setWindowTitle("Database Manager")
   dlg.show()
   sys.exit(app.exec_())
