from socket import *
import threading

# Nomor 1 Implementasi Pembuatan TCP Socket dan mengaitkannya ke alamat dan port tertentu
PORT = 80
SERVER = gethostbyname(gethostname())
ADDR = (SERVER, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)

def get_content(msg):
    # Nomor 2 Parsing HTTP request yang dikirimkan browser
    headers = msg.split('\n')
    filename = headers[0].split()[1]

    #Nomor 3 Mencari dan mengambil file dari file system
    #Nomor 4 Membuat HTTP response message dengan header tersendiri dengan konten file yang diminta
    if filename == '/':
        file = open("./index.html")
        content = file.read()
        response = "HTTP/1.1 200 OK\n\n" + content
    else:
        try:
            file = open(f".{filename}.html")
            content = file.read()
            response = "HTTP/1.1 200 OK\n\n" + content
        except:
            #Nomor 6 Kasus dimana file yang diminta tidak ditemukan
            response = "HTTP/1.1 404 Not Found\n\nFile Not Found!"
    return response

def handle_client(connectionSocket, adr):
    print(f"[NEW CONNECTION] {adr} connected!")
    connected = True
    while connected:
        msg = connectionSocket.recv(1024).decode()
        if msg:
            #Nomor 5 Mengirimkan response server ke browser (client)
            content = get_content(msg)
            connectionSocket.sendall(content.encode())
        connected = False
    connectionSocket.close()

#Nomor 1 Inisialisasi server socket dengan thread agar bisa multiple connection
def start():
    server.listen()
    print(f"[STARTED] Server is on {SERVER}")
    print(f"Buka browser lalu masukkan {SERVER}")
    while True:
        connectionSocket, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(connectionSocket, adr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} connections are active")

print("[STARTING] Server starting...")
start()