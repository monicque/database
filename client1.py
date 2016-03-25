from PyQt5.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
from PyQt5.QtWidgets import QTableView,QApplication
import sys

app = QApplication(sys.argv)

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("patientData.db")
db.open()

projectModel = QSqlQueryModel()
projectModel.setQuery("select * from patient",db)

projectView = QTableView()
projectView.setModel(projectModel)

projectView.show()
app.exec_()
