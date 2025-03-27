import socket
import threading

class chatServer:
    '''WebServer architecture adapted from Networks and Systems module 
    coursework material, including socket and request programming'''
    def __init__(self, host = '127.0.0.1', port = 8080, maxConnect = 3): # init. the server with local host and default port, and max. number of connected ppl. for semaphore
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket + bind copied
        serverSocket.bind((host, port))

        semaphore = threading.Semaphore(maxConnect) # semaphore limits connected threads to 3
        clients = [] # connected clients
        waitQueue = [] # clients waiting in queue
        
        serverSocket.listen(100) # listening to connections

        print(f"Chat Server started on {host}:{port}. Max connections: {maxConnect}")

        ''' UNIT TEST #1 = check if server runs from terminal
            Success - expected output printed:
            Chat Server started on 127.0.0.1:8080. Max connections: 3
        '''

        while True:
            # Accept incoming connections
            connectionSocket, addr = serverSocket.accept() # new client connection
            print(f"Connection established with {addr}")
            if len(clients) >= maxConnect:
                # if the maximum number of connections is reached, ->
                waitQueue.append((connectionSocket, addr))  # -> add client to the wait queue
                print(f"Connection limit reached. {addr} added to waiting queue.")
                connectionSocket.send("Server is full. You are in the waiting queue.".encode())  # notify the client

            else:
                # if there is room for more connections, allow the client to connect
                semaphore.acquire()  # .acquire the semaphore (decrement the connection counter - to prevent race conditions)
                clients.append((serverSocket, addr))  # client added to the active list
                print(f"Connection accepted. Active connections: {len(clients)}")
                serverSocket.send("Welcome to the chat server!".encode()) # .encode for error handling
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

            except Exception as e:
                print(f"Error handling request {addr}: {e}") # error handling
                break
                
        # client disconnected
        print(f"Client {addr} disconnected.")
        self.clients.remove((connectionSocket, addr))  # Remove the client from the active clients list
        self.semaphore.release()  # Release the semaphore (increment the connection counter)
        connectionSocket.close()  # Close the client socket
  
if __name__ =="__main__":
    server = chatServer()
    server.__init__()