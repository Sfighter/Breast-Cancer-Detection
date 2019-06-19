import sys
from PyQt4 import QtGui, QtCore
import os
from db import QDBObj
from  CancerInterface import Ui_MainWindow
from aqua.qsshelper import QSSHelper
import pickle


class Window(QtGui.QMainWindow ,Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(2000, 700)
        self.setWindowTitle("Breast Cancer Prediction")
        self.setWindowIcon(QtGui.QIcon('myoIconn.png'))
        self.setupUi(self)
        self.font()
        self.qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        self.setStyleSheet(self.qss)
        self.model = pickle.load( open( "breastcancer.model", "rb" ) )
        self.result_btn.clicked.connect(self.validate)
        self.reset_btn.clicked.connect(self.clear)
        self.out_btn.clicked.connect(self.firstPage)
        self.in_btn.clicked.connect(self.secondPage)
        self.stackedWidget.setCurrentWidget(self.login_pg)
        self.mysqlObj = QDBObj(_user='root', _password='12345', _database='breastCancer')
        #self.mysqlObj = QDBObj(_user='root', _password='27137', _database='testdb'
        if (not self.mysqlObj.status):
            self.custumErrorMsg("dataBase connection error !",
                                "the app can't find the database make sure you are connected to sql server")


        self.show()


    def validate(self):
        radius = self.radius_txt.text()
        if len(radius) > 0:
            try:
                radius = float(radius)
            except:
                msg = QtGui.QMessageBox.about(self, "Error", "Only Numbers",QtGui.QMessageBox.Ok)

        texture = (self.text_txt.text())
        if len(texture) > 0:
            texture = float(texture)


        perimeter = (self.perim_txt.text())
        if len(perimeter) > 0:
            perimeter = float(perimeter)

        area = (self.area_txt.text())
        if len(area) > 0:
            area = float(area)

        smoothness = (self.smooth_txt.text())
        if len(smoothness) > 0:
            smoothness = float(smoothness)

        compactness = (self.compac_txt.text())
        if len(compactness) > 0:
            compactness = float(compactness)

        concavity = (self.concv_txt.text())
        if len(concavity) > 0:
            concavity = float(concavity)

        concavePoint = (self.conPoi_txt.text())
        if len(concavePoint) > 0:
            concavePoint = float(concavePoint)

        symmetry = (self.symmetry_ttxt.text())
        if len(symmetry) > 0:
            symmetry = float(symmetry)

        fractal = (self.frac_txt.text())
        if len(fractal) > 0:
            fractal = float(fractal)

        feature = [ radius,            texture,
                perimeter,  area,
               smoothness,        compactness,
                concavity,     concavePoint,
                 symmetry,  fractal]
        x = self.model.predict(feature)
        if 1 in x:
            self.result_lbl.setText("Cancer is Malignant")
        else:
            self.result_lbl.setText("Cancer is Benign")

    def clear(self):
        self.radius_txt.clear()
        self.text_txt.clear()
        self.perim_txt.clear()
        self.area_txt.clear()
        self.smooth_txt.clear()
        self.conPoi_txt.clear()
        self.concv_txt.clear()
        self.frac_txt.clear()
        self.compac_txt.clear()
        self.symmetry_ttxt.clear()
        self.result_lbl.setText("Result appears here..")


    def custumErrorMsg(self, magTitle, msgBody):
        errormsg = QtGui.QMessageBox()
        errormsg.warning(self, magTitle, msgBody.decode("utf-8"))
        errormsg.setFixedSize(500, 200)

    def firstPage(self):
        self.stackedWidget.setCurrentWidget(self.login_pg)
        self.passtxt.clear()
        self.usertxt.clear()

    def secondPage(self):
        user = str(self.usertxt.text())
        if len(user) > 0:
            self.mysqlObj.sqlCursor.execute("SELECT dr_password FROM breastCancer.Login where dr_userName = '{}'".format(str(user)))
            passes = self.mysqlObj.sqlCursor.fetchone()
            password = str(self.passtxt.text())
            if passes:
                if password in str(passes[0]):
                    self.stackedWidget.setCurrentWidget(self.infoPage)
        else:
            msg = QtGui.QMessageBox.warning(self, "Warning Meassage", "Please enter Username and Password", QtGui.QMessageBox.Ok)



def Main():
    app = QtGui.QApplication(sys.argv)
    temp = Window()
    app.exec_()
if __name__ == "__main__":
    Main()
