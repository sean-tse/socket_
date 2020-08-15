import socket
import threading
import time

HEADER = 64 # first message length
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(f"|Server IP| {SERVER}")
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
MAX_CONNECTIONS = 2

DISCONNECT_MESSAGE = "||DISCONNECT||"
SHUTDOWN = "||||||"

stop_threads = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # connection Family (internet), type of connection
server.bind(ADDR)

conn_list = [] # List of all active connections
num_msgs = 0 # total number of messages received

# Sends a single message to a connection
def send(msg, conn):
    message = msg.encode(FORMAT) # the content we want to send
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT) # the first msg we send to prepare server
    send_length += b' ' * (HEADER - len(send_length)) # pads until the proper length
    
    conn.send(send_length)
    conn.send(message)

# Sends a message to all clients
def send_all(msg):
    for conn in conn_list:
        send(msg, conn)

# Receives a message from a client
def receive_one(conn):
    global num_msgs
    msg_length = conn.recv(HEADER).decode(FORMAT) # 
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        num_msgs += 1
        return msg
    return None


# Handles a single client
def handle_client(conn, addr):
    global stop_threads
    print(f"|New Client| at {addr}")
    connected = True
    while connected and not stop_threads:
        msg = receive_one(conn)
        if msg:
            # Special messages
            if msg == DISCONNECT_MESSAGE:
                global conn_list
                print(f"|Disconnect| from {addr}")
                connected = False
                conn_list.remove(conn)
            if msg == SHUTDOWN:
                #server.shutdown(socket.SHUT_RDWR)
                server.close()
                print("|SHUTDOWN|")
                stop_threads = True
                exit(0)

            # handles content of message
            print(f"|Message Received| {msg} from {addr}")
            #send(f"{msg} received", conn)
            send_all(msg+"  received")

    conn.close()


def start():
    server.listen() # listen for new connections
    global conn_list
    while not stop_threads and len(conn_list) < MAX_CONNECTIONS:
        (conn, addr) = server.accept() # awaits incoming new connection, and stores new connection socket and address
        conn_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr)).start() # creates a new thread to handle the client

        print(f"|Active connections|: {threading.active_count() -1}")
        print(conn_list)

## broadcasts to all connected clients regularly
# to use: thread = threading.Thread(target=count_sheep).start()
def count_infinite():
    num = 0
    while True:
        yield num
        num += 1

def count_sheep():
    for i in count_infinite():
        print(f"conn list: {conn_list}")
        print(f"{i} sheep sleeping peacefully")
        for conn in conn_list:
            send(f"{i} sheep sleeping peacefully", conn)
        time.sleep(3)
    

def next_turn():
    i = num_msgs % 2
    conn = conn_list[i]
    send("YOUR TURN", conn)

def game():
    # Sends a message to first player
    send("FIRST MESSAGE AYY",conn_list[0])

def main():
    try:
        print("|Server| is starting")
        start()
        # two players connected now
        game()
        print("debug 5")
    except:
        exit()



main()
