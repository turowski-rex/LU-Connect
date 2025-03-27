import socket

class chatClient:
    def __init__(self, host='127.0.0.1', port=8080): # init client with host and port of chatServer
        self.host = host
        self.port = port

        self.connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
        self.connectionSocket.connect((self.host, self.port))  # cnnect to server
        print("Connected to the chat server.")
        self.sendMessages()

    def sendMessages(self):
        # Ref: https://www.geeksforgeeks.org/simple-chat-room-using-python/
        # continuously send messages to server
        while True:
            message = input()  #user input
            try:
                self.connectionSocket.send(message.encode())  # send message to server
            except Exception as e:
                print(f"Error sending message: {e}") # error handling
                break

if __name__ == "__main__":
    client = chatClient()  # make client instance