#!/usr/bin/python3
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QWidget, QApplication, QMainWindow, QLabel, QGroupBox, QSpinBox, QPushButton, QGridLayout
from sys import exit,argv
from os import popen, system
home=popen("echo $HOME").read().strip()
class MainWin(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.show()
        self.central=Central()
        self.setCentralWidget(self.central)
        self.setFixedWidth(300)
class Central(QWidget):
    def __init__(self):
        super(Central,self).__init__()
        self.layout=QGridLayout(self)
        self.dayTime=QGroupBox("Day Time",self)
        self.dayTimeLay=QGridLayout(self.dayTime)
        self.ldMetacity=QLabel("Metacity",self)
        self.ldControls=QLabel("Controls",self)
        self.ldDesktop=QLabel("Desktop",self)
        self.edMetacity=QLineEdit(self)
        self.edControls=QLineEdit(self)
        self.edDesktop=QLineEdit(self)
        self.bdTry=QPushButton("Apply To See",self)
        self.bdTry.clicked.connect(lambda:self.applyToSee(0))
        self.dayTimeLay.addWidget(self.ldMetacity)
        self.dayTimeLay.addWidget(self.edMetacity,0,1,1,2)
        self.dayTimeLay.addWidget(self.ldControls)
        self.dayTimeLay.addWidget(self.edControls,1,1,1,2)
        self.dayTimeLay.addWidget(self.ldDesktop)
        self.dayTimeLay.addWidget(self.edDesktop,2,1,1,2)
        self.dayTimeLay.addWidget(self.bdTry,3,1)
        self.nightTime=QGroupBox("Night Time",self)
        self.nightTimeLay=QGridLayout(self.nightTime)
        self.lnMetacity=QLabel("Metacity",self)
        self.lnControls=QLabel("Controls",self)
        self.lnDesktop=QLabel("Desktop",self)
        self.enMetacity=QLineEdit(self)
        self.enControls=QLineEdit(self)
        self.enDesktop=QLineEdit(self)
        self.bnTry=QPushButton("Apply To See",self)
        self.bnTry.clicked.connect(lambda:self.applyToSee(1))
        self.nightTimeLay.addWidget(self.lnMetacity)
        self.nightTimeLay.addWidget(self.enMetacity,0,1,1,2)
        self.nightTimeLay.addWidget(self.lnControls)
        self.nightTimeLay.addWidget(self.enControls,1,1,1,2)
        self.nightTimeLay.addWidget(self.lnDesktop)
        self.nightTimeLay.addWidget(self.enDesktop,2,1,1,2)
        self.nightTimeLay.addWidget(self.bnTry,3,1)
        self.times=QGroupBox("Time Interval",self)
        self.timesLay=QGridLayout(self.times)
        self.lDay=QLabel("Day Time (H)",self)
        self.lNight=QLabel("Night Time (H)",self)
        self.sDay=QSpinBox(self)
        self.sNight=QSpinBox(self)
        self.sDay.setRange(0,12)
        self.sDay.setValue(7)
        self.sNight.setRange(12,24)
        self.sNight.setValue(19)
        self.bSave=QPushButton("Save Settings",self)
        self.bSave.clicked.connect(self.saveSettings)
        self.timesLay.addWidget(self.lDay)
        self.timesLay.addWidget(self.sDay,0,1,1,2)
        self.timesLay.addWidget(self.lNight)
        self.timesLay.addWidget(self.sNight,1,1,1,2)
        self.timesLay.addWidget(self.bSave,2,1)
        self.enable=QGroupBox("Enable/Disable",self)
        self.enableLay=QGridLayout(self.enable)
        self.bEnable=QPushButton("Enable")
        self.bDisable=QPushButton("Disable")
        self.lRestart=QLabel("Changes will be apply after restart.")
        self.bEnable.clicked.connect(self.enableApp)
        self.bDisable.clicked.connect(self.disableApp)
        self.enableLay.addWidget(self.bEnable)
        self.enableLay.addWidget(self.bDisable,0,1)
        self.enableLay.addWidget(self.lRestart,1,0,1,2)
        self.layout.addWidget(self.dayTime)
        self.layout.addWidget(self.nightTime)
        self.layout.addWidget(self.times)
        self.layout.addWidget(self.enable)
    def saveSettings(self): system(f"""echo "{self.enMetacity.text()}
{self.enControls.text()}
{self.enDesktop.text()}
{self.edMetacity.text()}
{self.edControls.text()}
{self.edDesktop.text()}
{self.sDay.text()}
{self.sNight.text()}" > {home}/.autoThemer/themes.ini""")
    def applyToSee(self,time):
        if time==0:
            if self.edMetacity.text()!="": system(f"gsettings set org.cinnamon.desktop.wm.preferences theme '{self.edMetacity.text()}'")
            if self.edControls.text()!="": system(f"gsettings set org.cinnamon.desktop.interface gtk-theme '{self.edControls.text()}'")
            if self.edDesktop.text()!="": system(f"gsettings set org.cinnamon.theme name '{self.edDesktop.text()}'")
        else:
            if self.enMetacity.text()!="": system(f"gsettings set org.cinnamon.desktop.wm.preferences theme '{self.enMetacity.text()}'")
            if self.enControls.text()!="": system(f"gsettings set org.cinnamon.desktop.interface gtk-theme '{self.enControls.text()}'")
            if self.enDesktop.text()!="": system(f"gsettings set org.cinnamon.theme name '{self.enDesktop.text()}'")
        QMessageBox.information(self,"Success","Changes applied. If you notice a bug press Ctrl+Alt+Esc to reload Cinnamon.")
    def enableApp(self):
        system(f"mkdir -p {home}/.autoThemer/")
        system(f"""echo '#!/usr/bin/python3
from os import system
from time import sleep
from datetime import datetime as dt
with open("{home}/themes.ini","r") as file:
    data=file.readlines()
    for i in range(len(data)): data[i]=data[i].replace("\\\\n","")
    data[6]=int(data[6])
    data[7]=int(data[7])
while True:
    now=dt.now().hour
    if now>data[6] and now<data[7]:
        if data[0]!="": system(f"gsettings set org.cinnamon.desktop.wm.preferences theme "+data[3])
        if data[1]!="": system(f"gsettings set org.cinnamon.desktop.interface gtk-theme "+data[4])
        if data[2]!="": system(f"gsettings set org.cinnamon.theme name "+data[5])
        sleep(600)
    else: 
        if data[0]!="": system("gsettings set org.cinnamon.desktop.wm.preferences theme "+data[0])
        if data[1]!="": system("gsettings set org.cinnamon.desktop.interface gtk-theme "+data[1])
        if data[2]!="": system("gsettings set org.cinnamon.theme name "+data[2])
        sleep(600)' > {home}/.autoThemer/autoThemer.py""")
        system(f"mkdir -p {home}/.config/autostart")
        system(f"""echo '[Desktop Entry]
Name=autoThemer
Exec=bash -c "cd {home}/.autoThemer/ && ./autoThemer.py"
Comment=Auto Theme Changer
Terminal=false
Icon=gtk-theme-config
Type=Application' > {home}/.config/autostart/autoThemer.desktop """)
        print(f"""echo '[Desktop Entry]
Name=autoThemer
Exec=bash -c "cd {home}/.autoThemer/ && ./autoThemer.py"
Comment=Auto Theme Changer
Terminal=false
Icon=gtk-theme-config
Type=Application' > {home}/.config/autostart/autoThemer.desktop """)
        system(f"chmod +x {home}/.config/autostart/autoThemer.desktop")
        QMessageBox.information(self,"Enabled","AutoThemer will start after re-login.")
    def disableApp(self):
        system(f"rm {home}/.config/autostart/autoThemer.desktop")
        QMessageBox.information(self,"Disabled","To close AutoThemer, re-login. Program will not start unless you enable it.")
app=QApplication(argv)
main=MainWin()
main.setWindowTitle("AutoThemer")
exit(app.exec_())