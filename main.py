from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QLineEdit, QStatusBar
from PyQt5.QtWidgets import QFileDialog
import sys, os
from PyQt5.QtGui import QPixmap, QTransform, QIcon

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.img_paths = []
        self.img_id = 0
        self.onShowAngle = 0
        self.initUI()
    def initUI(self):
        # button and action
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.okButtonClicked)
        exitButton = QPushButton("Exit")
        exitButton.clicked.connect(self.exitButtonClicked)
        openButton = QPushButton("Open")
        openButton.clicked.connect(self.openButtonClicked)
        nextButton = QPushButton("Next")
        nextButton.clicked.connect(self.nextButtonClicked)
        backButton = QPushButton("Back")
        backButton.clicked.connect(self.backButtonClicked)
        spinButon = QPushButton("Spin")
        spinButon.clicked.connect(self.spinButtonClicked)

        # content
        # picture show
        self.imgArea = QLabel()
        self.imgArea.setScaledContents(True)
        img = QPixmap('./main.jpg')
        self.imgArea.setPixmap(img)

        # text input
        self.textLine = QLineEdit()

        # label info
        self.info_path = QLabel()
        self.info_path.setMinimumWidth(300)
        self.info_angle = QLabel()
        self.info_angle.setMinimumWidth(100)
        infoBar = QStatusBar()
        infoBar.addWidget(self.info_path)
        infoBar.addWidget(self.info_angle)
        infoBar.setFixedHeight(20)

        # arrangement
        hbox = QHBoxLayout()
        hbox.addWidget(openButton)
        hbox.addWidget(nextButton)
        hbox.addWidget(backButton)
        hbox.addWidget(spinButon)
        hbox.addWidget(self.textLine)
        hbox.addWidget(okButton)
        hbox.addWidget(exitButton)
        hbox.setStretchFactor(openButton, 1)
        hbox.setStretchFactor(nextButton, 1)
        hbox.setStretchFactor(backButton, 1)
        hbox.setStretchFactor(spinButon, 1)
        hbox.setStretchFactor(self.textLine, 4)
        hbox.setStretchFactor(okButton, 1)
        hbox.setStretchFactor(exitButton, 1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.imgArea)
        vbox.addLayout(hbox)
        vbox.addWidget(infoBar)
        vbox.setStretchFactor(self.imgArea, 3)
        vbox.setStretchFactor(hbox, 1)
        vbox.setStretchFactor(infoBar, 1)

        # window size and location
        # window icon
        self.setWindowIcon(QIcon('./icon.png'))
        self.setLayout(vbox)
        # self.setGeometry(300, 300, 800, 100)
        self.setFixedSize(800, 300)
        self.setWindowTitle("LableImage")
        self.show()
    
    def okButtonClicked(self):
        if self.textLine.text() != "":
            print(self.textLine.text())
            labelPath = os.path.splitext(self.img_paths[self.img_id])[0] + ".txt"
            with open(labelPath, "w") as f:
                f.write(self.textLine.text())
            self.nextButtonClicked()
            self.textLine.setText("")
    
    def exitButtonClicked(self):
        sys.exit()
    
    def openButtonClicked(self):
        dirPath = QFileDialog.getExistingDirectory(self, "ChooseDirctory", "./", QFileDialog.ShowDirsOnly)
        pathList = os.listdir(dirPath)
        self.img_paths = []
        self.img_id = 0
        self.onShowAngle = 0
        for path in pathList:
            ext = os.path.splitext(path)[1]
            ext = ext.lower()
            if ext == ".jpg" or ext == ".png":
                self.img_paths.append(dirPath + "/" + path)
        if self.img_id < len(self.img_paths):
            self.releaseInfo(self.img_paths[self.img_id], str(self.onShowAngle))
            self.imgArea.setPixmap(QPixmap(self.img_paths[self.img_id]))
    
    def nextButtonClicked(self):
        if self.img_id + 1 < len(self.img_paths):
            self.img_id += 1
            self.onShowAngle = 0
            self.releaseInfo(self.img_paths[self.img_id], str(self.onShowAngle))
            self.imgArea.setPixmap(QPixmap(self.img_paths[self.img_id]))
        else:
            pass
    
    def backButtonClicked(self):
        if self.img_id > 0:
            self.img_id -= 1
            self.onShowAngle = 0
            self.releaseInfo(self.img_paths[self.img_id], str(self.onShowAngle))
            self.imgArea.setPixmap(QPixmap(self.img_paths[self.img_id]))
        else:
            pass

    def spinButtonClicked(self):
        self.onShowAngle = (self.onShowAngle + 90) % 360
        self.releaseInfo(None, str(self.onShowAngle))
        mat = QTransform()
        mat.rotate(self.onShowAngle)
        img = QPixmap(self.img_paths[self.img_id])
        img = img.transformed(mat)
        self.imgArea.setPixmap(img)
    
    def releaseInfo(self, path, angle):
        if path != None:
            self.info_path.setText(path)
        if angle != None:
            self.info_angle.setText(angle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    sys.exit(app.exec_())