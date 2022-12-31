import socket
import threading
import platform
import psutil


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 10005))
server.listen(5)
os = platform.system() #question the client for give his os and use this info on my loop def __data_receive_by_client

#loop for accepting client 
def connection_client():
    global client
    while True:
        print('Waiting for client connection')
        client, addr = server.accept()
        print(f'Client connected with success') 
        client.send(f'Hello !'.encode('utf-8'))
        threading.Thread(target=__data_receive_by_server, args=[client]).start()

def __data_receive_by_server(client):
    if os == 'Linux':
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'os':
                osfull = platform.platform()
                client.send(osfull.encode('utf-8'))

            elif data == 'ram':
                ram = round(psutil.virtual_memory().total/1000000000,2)
                ramused = round(psutil.virtual_memory().used/1000000000,2)
                ramusage = psutil.virtual_memory().percent
                client.send(f"You have {ram}GB of memorie, you used {ramused} GB right now, and you actual usage use {ramusage}% of you {ram} GB of memorie.".encode('utf-8'))

            elif data == 'hostname':
                hostname = platform.node()
                client.send(f"Your Hostname is :{hostname}".encode('utf-8'))

            elif data == 'ip':
                ip = socket.gethostbyname(socket.gethostname())
                client.send(f"Your ip is :{ip}".encode('utf-8'))

            elif data == 'cpu':
                #physical cores
                pysicores = psutil.cpu_count(logical=False)
                #logical cores
                logicores = psutil.cpu_count(logical=True)
                #processor type
                proc = platform.processor
                client.send(f"CPU {proc}, physical cores {pysicores}, locical cores {logicores}".encode('utf-8'))

            elif data == 'close':
                try:
                    client.close()
                    print('Client disconnected'.encode('utf-8'))
                    break
                except OSError:
                    print('Client disconnected'.encode('utf-8'))
                    break
                except ConnectionResetError:
                    print('Client disconnected'.encode('utf-8'))
                    break

            elif data == 'kill':
                client.close()
                server.close()
                break

            elif data == 'reboot':
                os.system("shutdown now -h".encode('utf-8'))
                break

    if os == 'Windows':
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'os':
                osfull = platform.platform()
                client.send(osfull.encode('utf-8'))

            if data == 'cpu':
                pysicores = psutil.cpu_count(logical=False)
                logicores = psutil.cpu_count(logical=True)
                proc = platform.processor
                client.send(f"CPU {proc}, physical cores {pysicores}, locical cores {logicores}".encode('utf-8'))

            elif data == 'ram':
                ram = round(psutil.virtual_memory().available/1000000000,2)
                ramused = round(psutil.virtual_memory().used/1000000000,2)
                ramusage = psutil.virtual_memory().percent
                client.send(f"You have {ram}GB of memorie, you used {ramused} GB right now, and you actual usage use {ramusage}% of you {ram} GB of memorie.".encode('utf-8'))

            elif data == 'hostname':
                hostname = platform.node()
                client.send(f"Your Hostname is :{hostname}".encode('utf-8'))

            elif data == 'ip':
                ip = socket.gethostbyname(socket.gethostname())
                client.send(f"Your ip is :{ip}".encode('utf-8'))
                
            elif data == 'close':
                client.close()
                print('Client disconnected')
                break

            elif data == 'kill':
                client.close()
                server.close()
                break

            elif data == 'reboot':
                os.system("shutdown -t 0 -r -f")


def send_data(client):
    while True:
        data = input('Enter command: ')
        client.send(data.encode('utf-8'))

def main():
    threading.Thread(target=connection_client, args=[]).start()

if __name__ == '__main__':
    main()
