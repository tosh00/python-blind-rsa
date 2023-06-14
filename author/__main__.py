import sys
import math
from rsa import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QLineEdit, QPushButton, QFileDialog, QPlainTextEdit

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()


        

        self.setWindowTitle("Autor")
        layout = QVBoxLayout()
        top_panel = QHBoxLayout()
        bottom_panel = QHBoxLayout()
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        more_right_panel = QVBoxLayout()
        left_reciving_panel = QVBoxLayout()
        right_reciving_panel = QVBoxLayout()
        more_right_reciving_panel = QVBoxLayout()
        more_more_right_reciving_panel = QVBoxLayout()



        getKeys = QPushButton("Pobierz klucz publiczny")
        getKeys.clicked.connect(self.loadKey)
        keyPathLayout = QHBoxLayout()
        keyPathLayout.addWidget(QLabel("Ścieżka: "))
        self.keyPath = QLineEdit("../publickey.txt")
        keyPathLayout.addWidget(self.keyPath)

        keyELayout = QHBoxLayout()
        keyELayout.addWidget(QLabel('e: '))
        self.keyEInput = QLineEdit()
        keyELayout.addWidget(self.keyEInput)

        keyNLayout = QHBoxLayout()
        keyNLayout.addWidget(QLabel('N: '))
        self.keyNInput = QLineEdit()
        keyNLayout.addWidget(self.keyNInput)

        generateR = QPushButton("Generuj losowy czynnik ślepy")
        generateR.clicked.connect(self.generateR)
        rLayout = QHBoxLayout()
        rLayout.addWidget(QLabel("t: "))
        self.rValue = QLabel("")
        rLayout.addWidget(self.rValue)


        getMessage = QPushButton("Pobierz i ukryj wiadomość z pliku")
        getMessage.clicked.connect(self.loadMessage)
        messagePathLayout = QHBoxLayout()
        messagePathLayout.addWidget(QLabel("Ścieżka: "))
        self.messagePath = QLineEdit("../file.png")
        messagePathLayout.addWidget(self.messagePath)

        shadowButton = QPushButton("Ukryj tekst i wyślij do podpisu")
        shadowButton.clicked.connect(self.shadowAndSend)
        
        left_panel.addWidget(getKeys)
        left_panel.addLayout(keyPathLayout)
        left_panel.addLayout(keyELayout)
        left_panel.addLayout(keyNLayout)
        left_panel.addWidget(generateR)
        left_panel.addLayout(rLayout)
        left_panel.addWidget(getMessage)
        left_panel.addLayout(messagePathLayout)
        left_panel.addWidget(shadowButton)
        left_panel.addStretch()
        top_panel.addLayout(left_panel)
        
        self.message = QPlainTextEdit('example')
        right_panel.addWidget(QLabel("wiadomość:"))
        right_panel.addWidget(self.message)
        top_panel.addLayout(right_panel)


        self.shadowMessage = QPlainTextEdit()
        self.shadowMessage.setReadOnly(True)
        more_right_panel.addWidget(QLabel('Ukryta wiadoność:'))
        more_right_panel.addWidget(self.shadowMessage)
        top_panel.addLayout(more_right_panel)


        getSignedMessage = QPushButton("Pobierz podpisaną wiadomość")
        getSignedMessage.clicked.connect(self.getSigned)
        messageSignedPathLayout = QHBoxLayout()
        messageSignedPathLayout.addWidget(QLabel("Ścieżka: "))
        self.signedMessagePath = QLineEdit("../signed")
        messageSignedPathLayout.addWidget(self.signedMessagePath)

        checker = QHBoxLayout()
        checkButton = QPushButton('Sprawdź podpis')
        checkButton.clicked.connect(self.check)
        self.checkLabel = QLabel('wynik')
        checker.addWidget(checkButton)
        checker.addWidget(self.checkLabel)

        unshadowSignedMessage = QPushButton("Odkryj podpisaną wiadomość")
        unshadowSignedMessage.clicked.connect(self.unshadowSignature)
        
        decryptSignedMessage = QPushButton("Odszyfruj wiadomość")
        decryptSignedMessage.clicked.connect(self.decrypt)

        messageDecryptedPathLayout = QHBoxLayout()
        messageDecryptedPathLayout.addWidget(QLabel("Ścieżka: "))
        self.decryptedMessagePath = QLineEdit("../decryptedFile.png")
        messageDecryptedPathLayout.addWidget(self.decryptedMessagePath)

        left_reciving_panel.addWidget(getSignedMessage)
        left_reciving_panel.addLayout(messageSignedPathLayout)
        left_reciving_panel.addWidget(unshadowSignedMessage)
        left_reciving_panel.addLayout(checker)
        left_reciving_panel.addWidget(decryptSignedMessage)
        left_reciving_panel.addLayout(messageDecryptedPathLayout)
        bottom_panel.addLayout(left_reciving_panel)



        self.signedShadowedMessage = QPlainTextEdit()
        self.signedShadowedMessage.setReadOnly(True)
        right_reciving_panel.addWidget(QLabel("ukryty podpis:"))
        right_reciving_panel.addWidget(self.signedShadowedMessage)
        bottom_panel.addLayout(right_reciving_panel)


        self.signedMessage = QPlainTextEdit()
        self.signedMessage.setReadOnly(True)
        more_right_reciving_panel.addWidget(QLabel("Podpis:"))
        more_right_reciving_panel.addWidget(self.signedMessage)
        bottom_panel.addLayout(more_right_reciving_panel)


        self.signedUnshadowedMessage = QPlainTextEdit()
        self.signedUnshadowedMessage.setReadOnly(True)
        more_more_right_reciving_panel.addWidget(QLabel("Wiadomość:"))
        more_more_right_reciving_panel.addWidget(self.signedUnshadowedMessage)
        bottom_panel.addLayout(more_more_right_reciving_panel)


        layout.addLayout(top_panel)
        layout.addLayout(bottom_panel)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.publicKey = {}
        self.blindFactor = 0
        self.messageArray = []


    def loadKey(self):
        try:
            with open('../publickey.txt', 'r') as file:
                [self.publicKey['n'], self.publicKey['e']] = [int(s.replace('\n', '')) for s in file.readlines()]
            self.keyNInput.setText(str(self.publicKey['n']))
            self.keyEInput.setText(str(self.publicKey['e']))
        except:
            pass

    def generateR(self):
        if(self.publicKey != {}):
            self.blindFactor = generateBlindFactor(self.publicKey['n'])
            self.rValue.setText(str(self.blindFactor)[0:50]+'...')

    def loadMessage(self):
        with open(self.messagePath.text(), 'rb') as file:
            self.messageText = file.read()
            self.messageArray = bytesToInt(self.messageText, lengthInBytes(self.publicKey['n'])//8 - 1)
            try:
                self.message.setPlainText(self.messageText.decode("utf-8") )
            except:
                t = ''
                for b in self.messageText:
                    t+=str(b)+'\n'
                self.message.setPlainText(t )
        shadowed = shadowing(self.messageArray, self.publicKey['e'], self.publicKey['n'], self.blindFactor)
        shadowedString = ''
        for c in shadowed:
            shadowedString+=str(c)+'\n\n'
        self.shadowMessage.setPlainText(shadowedString)
        with open('../toSign', 'wb') as file:
            file.write(intsToBytes(shadowed, lengthInBytes(self.publicKey['n'])//8 + 1))


    def shadowAndSend(self):
        self.messageText = bytes([ord(c) for c in self.message.toPlainText()])
        self.messageArray = bytesToInt(self.messageText, lengthInBytes(self.publicKey['n'])//8 - 1)

        shadowed = shadowing(self.messageArray, self.publicKey['e'], self.publicKey['n'], self.blindFactor)
        shadowedString = ''
        for c in shadowed:
            shadowedString+=str(c)+'\n'
        self.shadowMessage.setPlainText(shadowedString)
        
        with open('../toSign', 'wb') as file:
            file.write(intsToBytes(shadowed, lengthInBytes(self.publicKey['n'])//8 + 1))
    
    def getSigned(self):
        try:
            with open(self.signedMessagePath.text(), 'rb') as file:
                self.signedShadowed = bytesToInt(file.read(), lengthInBytes(self.publicKey['n'])//8 + 1)
            astext = ''
            for c in self.signedShadowed:
                astext+=str(c)+'\n\n'
            self.signedShadowedMessage.setPlainText(astext)
        except:
            pass

    def unshadowSignature(self):
        self.unshadowedSignature = unshadow(self.signedShadowed, self.publicKey['e'], self.publicKey['n'], self.blindFactor)
        astext = ''
        for c in self.unshadowedSignature:
            astext+=str(c)+'\n'
        self.signedMessage.setPlainText(astext)

    def decrypt(self):
        self.decrypted = intsToBytes(decryptRSAMessage(self.unshadowedSignature, self.publicKey['e'], self.publicKey['n']), lengthInBytes(self.publicKey['n'])//8 - 1)
        self.decrypted = trimDecrypted(self.decrypted)
        astext = ''
        for c in self.decrypted:
            astext+=chr(c)
        self.signedUnshadowedMessage.setPlainText(astext)
        try:
            with open(self.decryptedMessagePath.text(), 'wb') as file:
                file.write(self.decrypted)
        except:
            pass
            

    def check(self):
        res = checkSignature(self.publicKey['e'], self.publicKey['n'], self.unshadowedSignature, self.messageArray )
        if(res):
            self.checkLabel.setText('Prawdziwy')
        else:
            self.checkLabel.setText('Nie prawdziwy')

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()