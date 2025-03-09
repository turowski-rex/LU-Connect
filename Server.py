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
                serverSocket.send("Welcome to the chat server!".encode())
            # create a new thread to handle each client request
            threading.Thread(target=self.handleRequest, args=(connectionSocket, addr)).start()

"""
    def handleRequest(self, connectionSocket):
        try:
            # 1. Receive request message from the client
            message = connectionSocket.recv(MAX_DATA_RECV).decode()

            # 2. Extract the path of the requested object from the message (second part of the HTTP header)
            filename = message.split()[1]

            # 3. Read the corresponding file from disk
            with open(filename[1:], 'r') as f:  # Skip the leading '/'
                content = f.read()

            # 4. Create the HTTP response
            response = 'HTTP/1.1 200 OK\r\n\r\n'
            response += content

            # 5. Send the content of the file to the socket
            connectionSocket.send(response.encode())

        except IOError:
            # Handle file not found error
            error_response = "HTTP/1.1 404 Not Found\r\n\r\n"
            error_response += "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
            connectionSocket.send(error_response.encode())

        except Exception as e:
            print(f"Error handling request: {e}")

        finally:
            # Close the connection socket
            connectionSocket.close()"
            """

if __name__ =="__main__":
    server = chatServer()
    server.__init__()