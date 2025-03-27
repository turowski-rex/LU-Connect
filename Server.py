import socket
import threading
import datetime

class chatServer:
    '''WebServer architecture adapted from Networks and Systems module 
    coursework material, including socket and request programming'''
    def __init__(self, host = '127.0.0.1', port = 8080, maxConnect = 3): # init. the server with local host and default port, and max. number of connected ppl. for semaphore
        self.host = host
        self.port = port
        self.maxConnect = maxConnect

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket + bind copied
        self.serverSocket.bind((self.host, self.port))

        self.semaphore = threading.Semaphore(maxConnect) # semaphore limits connected threads to 3
        self.clients = [] # connected clients
        self.waitQueue = [] # clients waiting in queue
        
        self.serverSocket.listen(100) # listening to connections

        print(f"Chat Server started on {self.host}:{self.port}. Max connections: {self.maxConnect}")

        ''' UNIT TEST #1 = check if server runs from terminal
            Success - expected output printed:
            Chat Server started on 127.0.0.1:8080. Max connections: 3
        '''
# Seperated server-runnig functions from __init__
# Ref: https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client

    def runServer(self):
        while True:
            # Accept incoming connections
            connectionSocket, addr = self.serverSocket.accept() # new client connection
            print(f"Connection established with {addr}")

            if len(self.clients) >= self.maxConnect:
                # if the maximum number of connections is reached, ->
                self.waitQueue.append((connectionSocket, addr))  # -> add client to the wait queue
                print(f"Connection limit reached. {addr} added to waiting queue.")
                connectionSocket.send("Server is full. You are in the waiting queue.".encode())  # notify the client

            else:
                # if there is room for more connections, allow the client to connect
                self.semaphore.acquire()  # .acquire the semaphore (decrement the connection counter - to prevent race conditions)
                self.clients.append((connectionSocket, addr))  # client added to the active list
                print(f"Connection accepted. Active connections: {len(self.clients)}")
                connectionSocket.send("Welcome to the chat server!".encode()) # .encode for error handling
                # create a new thread to handle each client request
                threading.Thread(target=self.handleRequest, args=(connectionSocket, addr)).start()
        '''UNIT TEST #2 = checking connection of client to server
        Part success, part fail - connection achieved but server crashed immediately'''

# Need to handle request for server not to crash
    def handleRequest(self, connectionSocket, addr):
        # Ref: https://www.geeksforgeeks.org/simple-chat-room-using-python/
        while True:
            try:
                message = connectionSocket.recv(1024).decode() # recv message from client (1Kb)
                if not message:
                    break  # if message is empty, the client has disconnected
                print(f"Received from {addr}: {message}")
                self.broadcast(f"{addr}: {message}", connectionSocket)# broadcasting mesage to all cients

            except Exception as e:
                print(f"Error handling request {addr}: {e}") # error handling
                break
                
        # client disconnected
        print(f"Client {addr} disconnected.")
        self.clients.remove((connectionSocket, addr))# remove client from the active clients list
        self.semaphore.release()  # Release semaphore (increment the connection counter)
        self.checkQueue()         # check if clients are in queue
        connectionSocket.close()  # Close client socket

        '''Test #3
        Does not work without queue'''

    def checkQueue(self):
        # Check queue and allow next client to connect if there is room
        if self.waitQueue:
            connectionSocket, addr = self.waitQueue.pop(0)  # pop client form queue into the server
            self.semaphore.acquire()                        # accquire the semaphore (decrement connection count)
            self.clients.append((connectionSocket, addr))   # add client to active clients list
            print(f"Client {addr} moved from waiting queue to active connections.")
            connectionSocket.send("Welcome to the chat server!".encode())
            threading.Thread(target=self.handleRequest, args=(connectionSocket, addr)).start() # Start new thread to handle client

            '''Test #4 
            Connection and sending message to server works'''

    def broadcast(self, message, senderSocket):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for client, _ in self.clients:   # broadcast to all clients except sender

            if client != senderSocket:  # Do not send the message back to the sender
                try:
                    client.send(f"[{timestamp}] {message}".encode())  # Send message to clients
                except Exception as e:
                    print(f"Error broadcasting message: {e}") #error handling

            '''Test #5
            Sending messages doesn't work
            
            Test #6 
            Just had to swap lines in Client = works'''
  

if __name__ =="__main__":
    server = chatServer()
    server.runServer()