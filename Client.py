import socket

class chatClient:
    def __init__(self, host='127.0.0.1', port=8080): # init client with host and port of chatServer
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
        connectionSocket.connect((host, port))  # cnnect to server
        print("Connected to the chat server.")

if __name__ == "__main__":
    client = chatClient()  # make client instance