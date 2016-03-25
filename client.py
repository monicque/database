#author asla
#license Public Domain

import MySQLdb
import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtSql import *

class Client(PyQt5.QtWidgets.QWidget):
    #one message box at a time
    messageboxErr = None
    #buttons
    connectHost = None
    connectUser = None
    connectPass = None
    connectButton = None
    quitButton = None

    HostLabel = None
    UserLabel = None
    PassLabel = None

    #add a new item to a table
    newItemAdd = None
    deltuple = None

    #toolbar layout horizontal
    hbox = None

    #list of database tables vertical
    vbox = None

    #table grid
    tableview = None
    tablemodel = None
    tableItems = [] # list of items in a database
    dbTables = [] # list of tables in database

    #cursor and database
    db = None
    cursor = None

    #are we connected
    dbconnection = False
    tableselected = False

    view = None

    def __init__(self):
        super(Client, self).__init__()

        self.InitUI()

    def InitUI(self):
        #set up all the UI except grid and hide those that should not be seen
        self.hbox = PyQt5.QtWidgets.QHBoxLayout(self)
        self.vbox = PyQt5.QtWidgets.QVBoxLayout()

        self.connectHost = PyQt5.QtWidgets.QLineEdit(self)
        self.connectUser = PyQt5.QtWidgets.QLineEdit(self)
        self.connectPass = PyQt5.QtWidgets.QLineEdit(self)

        #message box
        self.messageboxErr = PyQt5.QtWidgets.QMessageBox(self)

        self.HostLabel = PyQt5.QtWidgets.QLabel(self)
        self.HostLabel.setText("Host")
        self.UserLabel = PyQt5.QtWidgets.QLabel(self)
        self.UserLabel.setText("UserName")
        self.PassLabel = PyQt5.QtWidgets.QLabel(self)
        self.PassLabel.setText("Password")

        self.HostLabel.setBuddy(self.connectHost)
        self.UserLabel.setBuddy(self.connectUser)
        self.PassLabel.setBuddy(self.connectPass)

        self.connectButton = PyQt5.QtWidgets.QPushButton(self)
        self.connectButton.setText("Connect")

        #insert button
        self.newItemAdd = PyQt5.QtWidgets.QPushButton()
        self.newItemAdd.setText("Insert Row")
        self.newItemAdd.hide()

        #delete a row
        self.deltuple = PyQt5.QtWidgets.QPushButton()
        self.deltuple.setText("Delete Row")
        self.deltuple.hide()

        #Quit
        self.quitButton = PyQt5.QtWidgets.QPushButton()
        self.quitButton.setText("Quit")
        self.quitButton.setGeometry(self.width() - 180 , self.height() - 12, 32, 32)
        self.quitButton.hide()


        #position the layout at the top of the window
        self.table = PyQt5.QtWidgets.QTableView(self)
        self.tablemodel = PyQt5.QtSql.QSqlTableModel(self)
        self.tablemodel.setHeaderData(0, Qt.Horizontal, 'First Name')
        self.tablemodel.setHeaderData(1, Qt.Horizontal, 'Last Name')
        self.tablemodel.setHeaderData(2, Qt.Horizontal, 'Course')
        self.tablemodel.setHeaderData(3, Qt.Horizontal, 'Year')
        self.tablemodel.setHeaderData(4, Qt.Horizontal, 'Fee Balance')

        self.table.setModel(self.tablemodel)
        self.table.setFixedSize(600, 600)
        self.table.hide()

        self.hbox.addWidget(self.table)
        self.hbox.addWidget(self.HostLabel)
        self.hbox.addWidget(self.connectHost)
        self.hbox.addWidget(self.UserLabel)
        self.hbox.addWidget(self.connectUser)
        self.hbox.addWidget(self.PassLabel)
        self.hbox.addWidget(self.connectPass)
        self.hbox.addWidget(self.connectButton)

        self.vbox.addWidget(self.newItemAdd)
        self.vbox.addWidget(self.deltuple)
        self.vbox.addWidget(self.quitButton)

        self.hbox.addLayout(self.vbox)

        #set up slots
        self.connectButton.clicked.connect(self.Connect)
        self.newItemAdd.clicked.connect(self.Insert)

        self.view = QTableView()

        #set up layout
        #self.setLayout(self.hbox)
        self.setGeometry(800, 700, 700, 700)
        #self.setSizePolicy(PyQt5.QtGui.QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setWindowTitle("MySQL Server Client")
        self.show()

    def Connect(self):
        if self.dbconnection == False:
            host = self.connectHost.text()
            username = self.connectUser.text()
            userpass = self.connectPass.text()
            try:
                self.db = QSqlDatabase.addDatabase("QSQLITE")
                self.db.setHostName(host)
                self.db.setPassword(userpass)
                self.db.setUserName(username)
                self.db.setDatabaseName('sports')
                if(self.db.open() == True):
                    self.dbconnection = True
                    self.HostLabel.hide()
                    self.connectHost.hide()
                    self.UserLabel.hide()
                    self.connectUser.hide()
                    self.PassLabel.hide()
                    self.connectPass.hide()
                    self.connectButton.hide()
                    self.table.show()
                    self.newItemAdd.show()
                    self.deltuple.show()
                    self.view.setModel(self.table)
            except MySQLdb.Error as e:
                self.messageboxErr.setText(str(e))
                self.messageboxErr.exec_()
                return
                #message box with error
        else:
            #check if table is available and whether values have been changed
            #if yes, update database with the changes
            try:
                self.Update()
                #execute command to save current data state
                self.cursor.execute(sql)
                self.cursor.close()
                self.db.close()
                self.dbconnection = False
                self.connectButton.setText("Connect")
                self.db.commit()
                self.dbconnection = True
                self.HostLabel.show()
                self.connectHost.show()
                self.UserLabel.show()
                self.connectUser.show()
                self.PassLabel.show()
                self.connectPass.show()
                self.connectButton.show()
                self.table.hide()
                self.newItemAdd.hide()
                self.deltuple.show()
            except MySQLdb.Error as e:
                self.messageboxErr.setText(str(e))
                self.messageboxErr.exec_()
                return
                #messagebox with error

    def Insert(self, name, reg_no, course, year, fee_balance):
        #insert into database
        #we don't know how many items to expect,... so we use a list
        self.cursor.execute()

    def Save(self):
        try:
            #dummy
            self.UpdateUI()
        except MySQLdb.Error as e:
            self.messageboxErr.setText(str(e))
            self.messageboxErr.exec_()

    def Query(self):
        #called when user clicks on table on the sidebar
        #used to list items in a table
        #get the names of the columns
        try:
            sql = "SHOW COLUMNS FROM "+ self.tablename.text()
            columns = cursor.execute(sql)
            #for each item list all it's contents
            self.tableItems = cursor.execute("FROM TABLE SELECT *")
        except MySQLdb.Error as e:
            self.messageboxErr.setText(str(e))
            self.messageboxErr.exec_()

        finally:
            self.UpdateUI()


if __name__ == '__main__':

    app = PyQt5.QtWidgets.QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
