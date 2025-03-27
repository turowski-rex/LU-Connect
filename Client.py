import socket
import threading
import winsound


class chatClient:
    def __init__(self, host='127.0.0.1', port=8080): # init client with host and port of chatServer
        self.host = host
        self.port = port
        self.notification = True #by default

        self.connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
        self.connectionSocket.connect((self.host, self.port))  # cnnect to server
        print("Connected to the chat server.")

        threading.Thread(target=self.receiveMessages).start() # start thread to receive
        self.sendMessages()

    def sendMessages(self):
        # Ref: https://www.geeksforgeeks.org/simple-chat-room-using-python/
        # continuously send messages to server
        while True:
            message = input()  #user input
            
            if message == "#mute":
                self.notification = False
                print("Muted notifications.")

            elif message == "#unmute":
                self.notification = True
                print("Unmuted notifications.")

            else:
                try:
                    self.connectionSocket.send(message.encode())  # send message to server
                except Exception as e:
                    print(f"Error sending message: {e}") # error handling
                    break

    def receiveMessages(self):
        # Continuously receive messages from the server
        while True:
            try:
                message = self.connectionSocket.recv(1024).decode()  # Receive a message from the server
                if not message:
                    break  # If the message is empty, the server has disconnected
                print(message)  # Print the received message

                if self.notification:
                    self.playNotification()

            except Exception as e:
                print(f"Error receiving message: {e}")  # error handling
                break
        
    def playNotification(self):
        # Ref: https://www.geeksforgeeks.org/python-winsound-module/
        # Using winsound instead of playsound, because no additional file and path needed
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        


if __name__ == "__main__":
    client = chatClient()  # make client instance