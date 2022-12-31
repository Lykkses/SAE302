import os 
import socket
import threading

def main():
    #Created one client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 10000))
    print(f"Client connected to server. Client is connected to {client.getpeername()}")

    #loop to send data to server
    flag = True
    while flag:
        message = input("Enter you message for the server: ")
        client.send(message.encode())
        
        if message == "disconnect":
            flag = False
        else:
            data = client.recv(1024).decode()
            print(data)

        if message == "kill":
            flag= False
        else:
            data = client.recv(1024).decode()
            print(data)
        
        if message == "reset":
            flag = False
        else:
            data = client.recv(1024).decode()
            print(data)

        if message == "OS":
            data = client.recv(1024).decode()
            print(data)
        else:
            print("Command not found")
        
        if message == "ram":
            data = client.recv(1024).decode()
            print(data)
        else:
            print("Command not found")
        
        if message =='name':
            data = client.recv(1024).decode()
            print(data)
        else:
            print("Command not found")
        
        
      
        
            
        


if __name__ == "__main__":
    main()