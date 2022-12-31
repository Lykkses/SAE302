#import usefull paquages for the GUI

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import socket

#Need to import the client file for use commands
import Client as client

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Application for server monitoring")
        
        #Button connection and the list of servers

        self.connect = QPushButton("Push to add a new server")
        self.listserv = QListWidget()
        self.textservlist = QLabel("List of servers :")

        #Command for the data send by the server
        self.replyserver = QTextBrowser()
        self.replyserver.setReadOnly(True)

        #define all the input for the GUI

        self.aipinput = QLineEdit()
        self.aipinput.setPlaceholderText("Enter @IP")
        self.portinput = QLineEdit()
        self.portinput.setPlaceholderText("Enter port")
        self.commandinput = QLineEdit()
        self.commandinput.setPlaceholderText("Enter command")
        self.sendcommand = QPushButton("Send command")
        self.presavebuttontypeos = QPushButton("OS Type")
        self.presavebuttonram = QPushButton("RAM Info")
        self.presavebuttonhostname = QPushButton("Hostname")
        self.presavebuttoncpu = QPushButton("CPU")
        self.presavebuttonip = QPushButton("IP")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.disconnect = QPushButton("Disconnect")
        self.delete = QPushButton("Delete")
        self.exit = QPushButton("Exit")
        self.info = QPushButton("Info")

        #Command for receive data from the server

        self.threadreceiv = threading.Thread(target=self.__data_receive_by_server, args=(client,))

        self.exit_error = threading.Event()


        #Add Widget, and position on the application

        grid.addWidget(self.presavebuttontypeos, 0, 0, 1, 1)
        grid.addWidget(self.presavebuttonram, 1, 0, 1, 1)
        grid.addWidget(self.presavebuttonhostname, 2, 0, 1, 1)
        grid.addWidget(self.presavebuttoncpu, 3, 0, 1, 1)
        grid.addWidget(self.presavebuttonip, 4, 0, 1, 1)
        grid.addWidget(self.textservlist, 0, 1, 1, 1)
        grid.addWidget(self.info, 0, 3, 1, 1)
        grid.addWidget(self.listserv, 1, 1, 4, 3)
        grid.addWidget(self.aipinput, 5, 0, 1, 1)
        grid.addWidget(self.portinput, 5, 1, 1, 1)
        grid.addWidget(self.connect, 5, 2, 1, 1)
        grid.addWidget(self.disconnect, 5, 3, 1, 1)
        grid.addWidget(self.delete, 6, 0, 1, 1)
        grid.addWidget(self.commandinput, 7, 0, 1, 1)
        grid.addWidget(self.sendcommand, 8, 0, 1, 1) 
        grid.addWidget(self.replyserver, 6, 1, 3, 3) 
        grid.addWidget(self.exit, 9, 0  , 1, 1)

        #Create the all button on the application
        self.info.clicked.connect(self.__info)
        self.exit.clicked.connect(self.__exit)
        self.__importservfile(client)
        self.listserv.itemDoubleClicked.connect(self.__listserv)
        self.connect.clicked.connect(self.__connect)
        self.sendcommand.clicked.connect(self.__data_send_to_the_client)
        self.disconnect.clicked.connect(self.__disconnect)
        self.delete.clicked.connect(self.__delete)
        self.presavebuttontypeos.clicked.connect(self.__typeos)
        self.presavebuttonram.clicked.connect(self.__ram)
        self.presavebuttonhostname.clicked.connect(self.__hostname)
        self.presavebuttoncpu.clicked.connect(self.__cpu)
        self.presavebuttonip.clicked.connect(self.__ip)


        


        #Command for the button
    def __info(self):
        QMessageBox.information(self, "Aide", "Hello, I am a monitoring application. You can import .csv files so that you don't type all the clients you want to monitor. You can also add a server with the space dedicated to this, don't forget to do 'add a new server'. To open a client, just double click on the server in question. You can in one click know the ram, the cpu, the name of the machine, the os and the @ip.")
        pass

    def __exit(self):
        sys.exit()
        pass

    def closeEvent(self, _e: QCloseEvent): # <--- Fermeture de l'application depuis la croix Windows
        box = QMessageBox()
        box.setWindowTitle("Quitter ?")
        box.setText("Voulez vous quitter ?")
        box.addButton(QMessageBox.Yes)
        box.addButton(QMessageBox.No)

        ret = box.exec()

        if ret == QMessageBox.Yes:
            QCoreApplication.exit(0)
        else:
            _e.ignore()

    def __connect(self, client):
        if self.aipinput.text() == "" or self.portinput.text() == "":
            QMessageBox.warning(self, "Error", "Please enter IP address and port")
        else:
            self.listserv.addItem(self.aipinput.text() + ":" + self.portinput.text())
            servercsv = open("servers.csv", "a")
            servercsv.write(self.aipinput.text() + ":" + self.portinput.text() + "\n")
            servercsv.close()
            self.aipinput.setText("")
            self.portinput.setText("")

    #for adding client with a csv file       
    def __importservfile(self, client):
        servercsv = open("servers.csv", "r")
        for line in servercsv:
            self.listserv.addItem(line)
        servercsv.close()

    #function for delete file on the csv   
    def __delete(self):
        if self.listserv.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            self.listserv.takeItem(self.listserv.currentRow())
            servercsv = open("servers.csv", "w")
            for i in range(self.listserv.count()):
                servercsv.write(self.listserv.item(i).text() + "\n")
            servercsv.close()

         
    def __listserv(self, client):
        if self.listserv.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            try:
                ip = self.listserv.currentItem().text().split(":")[0]
                port = int(self.listserv.currentItem().text().split(":")[1])
                self.client.connect((ip, port))
                QMessageBox.information(self, "Success", "Connected to server")
                self.threadreceiv.start()
                return self.client 
            except:
                QMessageBox.warning(self, "Error", "Connection failed")

    def __disconnect(self):
        if self.listserv.currentItem() == None:
            QMessageBox.warning(self, "Error", "Select a server")
        try:
            self.client.send("close".encode('utf-8'))
            self.client.close()
            self.exit_error.set()
            print ("good")
            QMessageBox.information(self, "Success", "Disconnected from server")
            self.replyserver.clear()
        except:
            QMessageBox.warning(self, "Error", "Disconnection failed")

    def __data_receive_by_server(self, client):
        while True:
            if self.exit_error.is_set():
                print ("exit")
                break
            try:
                data = self.client.recv(1024)
                self.replyserver.append(data.decode('utf-8'))
                self.replyserver.update()
            except:
                pass
    
    #fonction for sending data to the client
    def __data_send_to_the_client(self, client):
        if self.commandinput.text() == "clear":
            self.replyserver.clear()
            self.commandinput.setText("")
        elif self.commandinput.text() == "":
            QMessageBox.warning(self, "Error", "Please enter a command")
        elif self.listserv.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            self.client.send(self.commandinput.text().encode('utf-8'))
            self.commandinput.setText("")

    #fonction CPU, RAM, IP, HOSTNAME
    def __typeos(self):
        self.commandinput.setText("os")
        self.__data_send_to_the_client(client)

    def __ram(self):
        self.commandinput.setText("ram")
        self.__data_send_to_the_client(client)
        
    def __hostname(self):
        self.commandinput.setText("hostname")
        self.__data_send_to_the_client(client)

    def __cpu(self):
        self.commandinput.setText("cpu")
        self.__data_send_to_the_client(client)

    def __ip(self):
        self.commandinput.setText("ip")
        self.__data_send_to_the_client(client)   
        
        
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
   
  

if __name__ == '__main__':
    main()       



