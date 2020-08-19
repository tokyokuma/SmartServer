#!/usr/bin/env python
# coding: utf-8

import sys
import time
import os
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QCoreApplication

conn=None
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag=0
        #Text
        self.chatTextField=QLineEdit(self)
        self.chatTextField.resize(480,100)
        self.chatTextField.move(10,350)
        #Send button
        self.btnSend=QPushButton("Send",self)
        self.btnSend.resize(480,30)
        self.btnSendFont=self.btnSend.font()
        self.btnSendFont.setPointSize(15)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10,460)
        self.btnSend.setStyleSheet("background-color: #F7CE16")
        self.btnSend.clicked.connect(self.send)
        #Layout
        self.chatBody=(self)
        splitter=QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400,100])

        splitter2=QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200,10])

        self.chatBody.addWidget(splitter2)

        #set icon
        path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), '../img/PyServer_icon.png')
        app.setWindowIcon(QIcon(path))

        self.setWindowTitle("ServerGui")
        self.resize(500, 500)

    def send(self):
        text=self.chatTextField.text()
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:>80}'.format(text)
        self.chat.append(textFormatted)
        global conn
        conn.send(text.encode("utf-8"))
        self.chatTextField.setText("")

class ServerThread(Thread):
    def __init__(self,window): 
        Thread.__init__(self) 
        self.window=window

    def run(self): 
        TCP_IP = '0.0.0.0' 
        TCP_PORT = 80 
        BUFFER_SIZE = 20  
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        tcpServer.bind((TCP_IP, TCP_PORT)) 
        threads = [] 
        
        tcpServer.listen(4) 
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...") 
            global conn
            (conn, (ip,port)) = tcpServer.accept() 
            newthread = ClientThread(ip,port,window) 
            newthread.start() 
            threads.append(newthread) 
        
 
        for t in threads: 
            t.join() 

class ClientThread(Thread): 
 
    def __init__(self,ip,port,window): 
        Thread.__init__(self) 
        self.window=window
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port)) 
 
    def run(self): 
        while True :         
            #(conn, (self.ip,self.port)) = serverThread.tcpServer.accept() 
            global conn
            data = conn.recv(2048) 
            window.chat.append(data.decode("utf-8"))
            print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = Window()
    serverThread=ServerThread(window)
    serverThread.start()
    window.exec()
    
    sys.exit(app.exec_())