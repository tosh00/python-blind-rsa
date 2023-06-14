import sys
import time
from rsa import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QLineEdit, QPushButton, QPlainTextEdit

class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()


        self.setWindowTitle("Podpisujący")

        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        center_panel = QVBoxLayout()
        right_panel = QVBoxLayout()


        self.generateKeys = QPushButton('Generuj klucze')
        self.generateKeys.clicked.connect(self.getKeys)
        left_panel.addWidget(self.generateKeys)

        left_panel.addWidget(QLabel("Prywatny"))

        privateKey = QHBoxLayout()
        privateKey.addWidget(QLabel('d: '))
        self.dprivateLabel = QLabel()
        privateKey.addWidget(self.dprivateLabel )
        left_panel.addLayout(privateKey)
        privateKey = QHBoxLayout()
        privateKey.addWidget(QLabel('N: '))
        self.nprivateLabel = QLabel()
        privateKey.addWidget(self.nprivateLabel )
        left_panel.addLayout(privateKey)

        left_panel.addWidget(QLabel("Publiczny"))
        publicKey = QHBoxLayout()
        publicKey.addWidget(QLabel('e '))
        self.epublicLabel = QLabel()
        publicKey.addWidget(self.epublicLabel )
        left_panel.addLayout(publicKey)

        publicKey = QHBoxLayout()
        publicKey.addWidget(QLabel('N: '))
        self.npublicLabel = QLabel()
        publicKey.addWidget(self.npublicLabel )
        left_panel.addLayout(publicKey)

        loadMessage = QPushButton('Wczytaj wiadomość')
        loadMessage.clicked.connect(self.loadMessage)
        self.messagePath = QLineEdit('../toSign')

 

        signMessage = QPushButton('Podpisz')
        signMessage.clicked.connect(self.sign)

        left_panel.addWidget(loadMessage)
        left_panel.addWidget(self.messagePath)
        left_panel.addWidget(signMessage)




        self.message = QPlainTextEdit()
        self.message.setReadOnly(True)
        center_panel.addWidget(QLabel("Wiadomość:"))
        center_panel.addWidget(self.message)


        self.SignedMessage = QPlainTextEdit()
        self.SignedMessage.setReadOnly(True)
        right_panel.addWidget(QLabel("Podpisana:"))
        right_panel.addWidget(self.SignedMessage)

        layout.addLayout(left_panel)
        layout.addLayout(center_panel)
        layout.addLayout(right_panel)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.publicKey={}
        self.privateKey={}
        self.toSign = []
        self.loadExistedKeys()
    
    def loadExistedKeys(self):
        try:
            with open('./privatekey.txt', 'r') as file:
                content =  file.readlines()
                self.privateKey['n']=int(content[0].replace('\n', ''))
                self.privateKey['d']=int(content[1].replace('\n', ''))
    
            with open('../publickey.txt', 'r') as file:
                content =  file.readlines()
                self.publicKey['n']=int(content[0].replace('\n', ''))
                self.publicKey['e']=int(content[1].replace('\n', ''))
            self.showKeys()
        except:
            pass
    
    def getKeys(self):
        start = time.time()
        keys =generateKeys(1000)
        print("generated in: ", time.time()-start)
        self.privateKey = keys['private']
        self.publicKey = keys['public']

        self.showKeys()
        with open('./privatekey.txt', 'w') as file:
            file.write(str(self.privateKey['n']))
            file.write('\n')
            file.write(str(self.privateKey['d']))

        with open('../publickey.txt', 'w') as file:
            file.write(str(self.publicKey['n']))
            file.write('\n')
            file.write(str(self.publicKey['e']))

    def showKeys(self):

        self.nprivateLabel.setText(str(self.privateKey['n'])[0:50]+'...')
        self.dprivateLabel.setText(str(self.privateKey['d'])[0:50]+'...')
        self.npublicLabel.setText(str(self.publicKey['n'])[0:50]+'...')
        self.epublicLabel.setText(str(self.publicKey['e'])[0:50]+'...')

    def loadMessage(self):
        with open(self.messagePath.text(), 'rb') as file:
            self.messageText = bytesToInt(file.read(), lengthInBytes(self.publicKey['n'])//8 + 1)
        
        try:
            self.message.setPlainText(self.messageText.encode('utf-8'))
        except:
            t = ''
            for b in self.messageText:
                t+=str(b)+'\n\n'
            self.message.setPlainText(t )

    def sign(self):
        self.signed = generateSignature(self.messageText, self.privateKey['d'], self.privateKey['n'])
        signedToShow = ''
        for c in self.signed:
            signedToShow+=str(c)+'\n\n'
        self.SignedMessage.setPlainText(signedToShow)
        with open('../signed', 'wb') as file:
            file.write(intsToBytes(self.signed, lengthInBytes(self.publicKey['n'])//8 + 1))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()